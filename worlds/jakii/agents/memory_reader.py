import logging
import struct
from typing import ByteString, Callable
import pymem
from pymem import pattern
from pymem.exception import ProcessNotFound, ProcessError, MemoryReadError, WinAPIError
from dataclasses import dataclass

# Handle both relative and absolute imports for flexibility
try:
    from ..locs.mission_locations import main_mission_table, side_mission_table
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from locs.mission_locations import main_mission_table, side_mission_table


logger = logging.getLogger("Jak2MemoryReader")


# Some helpful constants.
sizeof_uint64 = 8
sizeof_uint32 = 4
sizeof_uint8 = 1

# *****************************************************************************
# **** This number must match (-> *ap-info-jak2* version) in ap-struct.gc! ****
# *****************************************************************************
expected_memory_version = 1


# Memory structure layout for Jak 2 Archipelago integration
# Must match ap-info-jak2 structure in ap-struct-h.gc
@dataclass
class OffsetFactory:
    current_offset: int = 0

    def define(self, size: int, length: int = 1) -> int:
        # Align current_offset to the current size first
        bytes_to_alignment = self.current_offset % size
        if bytes_to_alignment != 0:
            self.current_offset += (size - bytes_to_alignment)

        # Increment current_offset so the next definition can be made
        offset_to_use = self.current_offset
        self.current_offset += (size * length)
        return offset_to_use


# Start defining important memory address offsets here. They must be in the same order, have the same sizes, and have
# the same lengths, as defined in `ap-info-jak2`.
offsets = OffsetFactory()

# Memory version
memory_version_offset = offsets.define(sizeof_uint32)

# Mission information
next_mission_index_offset = offsets.define(sizeof_uint64)
next_side_mission_index_offset = offsets.define(sizeof_uint64)
missions_checked_offset = offsets.define(sizeof_uint32, 70)  # 65 main missions + buffer
side_missions_checked_offset = offsets.define(sizeof_uint32, 24)  # 33 side missions + buffer

# End marker
end_marker_offset = offsets.define(sizeof_uint8, 4)


class Jak2MemoryReader:
    gk_process: pymem.process = None
    goal_address: int = None
    connected = False
    initiated_connect = False

    # Track completed missions
    location_outbox: list[int] = []
    outbox_index: int = 0
    
    # Track game completion
    finished_game = False

    # Callbacks for communicating with the main client
    inform_checked_location: Callable
    inform_finished_game: Callable
    log_error: Callable
    log_warn: Callable
    log_success: Callable
    log_info: Callable

    def __init__(self,
                 location_check_callback: Callable,
                 finish_game_callback: Callable,
                 log_error_callback: Callable,
                 log_warn_callback: Callable,
                 log_success_callback: Callable,
                 log_info_callback: Callable,
                 marker: ByteString = b'ArChIpElAgO_JaK2\x00'):
        self.marker = marker

        self.inform_checked_location = location_check_callback
        self.inform_finished_game = finish_game_callback

        self.log_error = log_error_callback
        self.log_warn = log_warn_callback
        self.log_success = log_success_callback
        self.log_info = log_info_callback

    async def main_tick(self):
        if self.initiated_connect:
            await self.connect()
            self.initiated_connect = False

        if self.connected:
            try:
                self.gk_process.read_bool(self.gk_process.base_address)  # Ping to see if it's alive.
            except (ProcessError, MemoryReadError, WinAPIError):
                msg = (f"Error reading game memory! (Did the game crash?)\n"
                       f"Please close all open windows and reopen the Jak II Client "
                       f"from the Archipelago Launcher.\n"
                       f"If the game and compiler do not restart automatically, please follow these steps:\n"
                       f"   Run the OpenGOAL Launcher, click Jak II > Features > Mods > ArchipelaGOAL.\n"
                       f"   Then click Advanced > Play in Debug Mode.\n"
                       f"   Then click Advanced > Open REPL.\n"
                       f"   Then close and reopen the Jak II Client from the Archipelago Launcher.")
                self.log_error(logger, msg)
                self.connected = False
        else:
            return

        if self.connected:
            # Read the memory address to check the state of the game.
            self.read_memory()

            # Handle completed missions
            if len(self.location_outbox) > self.outbox_index:
                self.inform_checked_location(self.location_outbox)
                self.outbox_index += 1

            # Check for game completion (final boss defeated)
            if self.finished_game:
                self.inform_finished_game()

    async def connect(self):
        try:
            self.gk_process = pymem.Pymem("gk.exe")  # The GOAL Kernel - same as Jak 1
            logger.debug("Found the gk process: " + str(self.gk_process.process_id))
        except ProcessNotFound:
            self.log_error(logger, "Could not find the game process.")
            self.connected = False
            return

        # Look for the Archipelago marker in the first loaded module
        modules = list(self.gk_process.list_modules())
        marker_address = pattern.pattern_scan_module(self.gk_process.process_handle, modules[0], self.marker)
        if marker_address:
            # At this address is another address that contains the struct we're looking for
            # Add marker length + 4 bytes padding, then read the 8-byte pointer
            goal_pointer = marker_address + len(self.marker) + 4
            self.goal_address = int.from_bytes(self.gk_process.read_bytes(goal_pointer, sizeof_uint64),
                                               byteorder="little",
                                               signed=False)
            logger.debug("Found the Jak 2 archipelago memory address: " + str(self.goal_address))
            await self.verify_memory_version()
        else:
            self.log_error(logger, "Could not find the Jak 2 Archipelago marker address!")
            self.connected = False

    async def verify_memory_version(self):
        if self.goal_address is None:
            self.log_error(logger, "Could not find the Jak 2 Archipelago memory address!")
            self.connected = False
            return

        memory_version: int | None = None
        try:
            memory_version = self.read_goal_address(memory_version_offset, sizeof_uint32)
            if memory_version == expected_memory_version:
                self.log_success(logger, "The Jak 2 Memory Reader is ready!")
                self.connected = True
            else:
                raise MemoryReadError(memory_version_offset, sizeof_uint32)
        except (ProcessError, MemoryReadError, WinAPIError):
            if memory_version is None:
                msg = (f"Could not find a version number in the OpenGOAL memory structure!\n"
                       f"   Expected Version: {str(expected_memory_version)}\n"
                       f"   Found Version: {str(memory_version)}\n"
                       f"Please follow these steps:\n"
                       f"   If the game is running, try entering '/memr connect' in the client.\n"
                       f"   You should see 'The Jak 2 Memory Reader is ready!'\n"
                       f"   If that did not work, or the game is not running, run the OpenGOAL Launcher.\n"
                       f"   Click Jak II > Features > Mods > ArchipelaGOAL.\n"
                       f"   Then click Advanced > Play in Debug Mode.\n"
                       f"   Try entering '/memr connect' in the client again.")
            else:
                msg = (f"The OpenGOAL memory structure is incompatible with the current Archipelago client!\n"
                       f"   Expected Version: {str(expected_memory_version)}\n"
                       f"   Found Version: {str(memory_version)}\n"
                       f"Please follow these steps:\n"
                       f"   Run the OpenGOAL Launcher, click Jak II > Features > Mods > ArchipelaGOAL.\n"
                       f"   Click Update (if one is available).\n"
                       f"   Click Advanced > Compile. When this is done, click Continue.\n"
                       f"   Click Versions and verify the latest version is marked 'Active'.\n"
                       f"   Close all launchers, games, clients, and console windows, then restart Archipelago.")
            self.log_error(logger, msg)
            self.connected = False

    async def print_status(self):
        proc_id = str(self.gk_process.process_id) if self.gk_process else "None"
        last_loc = str(self.location_outbox[self.outbox_index - 1] if self.outbox_index else "None")
        msg = (f"Jak 2 Memory Reader Status:\n"
               f"   Game process ID: {proc_id}\n"
               f"   Game state memory address: {str(self.goal_address)}\n"
               f"   Last location checked: {last_loc}")
        await self.verify_memory_version()
        self.log_info(logger, msg)

    def read_memory(self) -> list[int]:
        try:
            # Read mission completion indices
            next_mission_idx = self.read_goal_address(next_mission_index_offset, sizeof_uint64)
            next_side_mission_idx = self.read_goal_address(next_side_mission_index_offset, sizeof_uint64)

            # Read completed main missions
            for i in range(int(next_mission_idx)):
                mission_id = self.read_goal_address(missions_checked_offset + (i * sizeof_uint32), sizeof_uint32)
                if mission_id not in self.location_outbox:
                    # Convert mission ID to location ID based on our tables
                    if mission_id in main_mission_table:
                        location_id = mission_id  # Mission ID directly maps to location ID
                        self.location_outbox.append(location_id)
                        logger.debug(f"Main mission {mission_id} completed: {main_mission_table[mission_id].name}")

            # Read completed side missions  
            for i in range(int(next_side_mission_idx)):
                side_mission_id = self.read_goal_address(side_missions_checked_offset + (i * sizeof_uint32), sizeof_uint32)
                if side_mission_id not in self.location_outbox:
                    # Convert side mission ID to location ID based on our tables
                    if side_mission_id in side_mission_table:
                        location_id = side_mission_id + 100  # Offset matches locations.py
                        self.location_outbox.append(location_id)
                        logger.debug(f"Side mission {side_mission_id} completed: {side_mission_table[side_mission_id].name}")

            # Check if final boss is defeated (mission 65 - "Destroy Metal Kor at Nest")
            if 65 in [mission_id for i in range(int(next_mission_idx)) 
                     for mission_id in [self.read_goal_address(missions_checked_offset + (i * sizeof_uint32), sizeof_uint32)]]:
                self.finished_game = True

        except (ProcessError, MemoryReadError, WinAPIError) as e:
            logger.debug(f"Memory read error: {e}")
            return []

        return self.location_outbox

    def read_goal_address(self, offset: int, size: int) -> int:
        """Helper function to read from the GOAL memory structure at the given offset."""
        try:
            read_bytes = self.gk_process.read_bytes(self.goal_address + offset, size)
            if size == sizeof_uint64:
                return struct.unpack("<Q", read_bytes)[0]  # Little-endian uint64
            elif size == sizeof_uint32:
                return struct.unpack("<I", read_bytes)[0]  # Little-endian uint32
            elif size == sizeof_uint8:
                return struct.unpack("<B", read_bytes)[0]  # uint8
            else:
                raise ValueError(f"Unsupported size for reading: {size}")
        except (ProcessError, MemoryReadError, WinAPIError) as e:
            logger.debug(f"Failed to read {size} bytes at offset {offset}: {e}")
            raise e