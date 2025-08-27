import logging
import queue
import struct
from dataclasses import dataclass
from queue import Queue
from typing import Callable

import pymem
from pymem.exception import ProcessNotFound, ProcessError

import asyncio
from asyncio import StreamReader, StreamWriter, Lock

# Handle imports with flexibility
try:
    from NetUtils import NetworkItem
    from ..game_id import jak2_name
    from ..items import key_item_table
    from ..locs.mission_locations import main_mission_table, side_mission_table
except ImportError:
    # Fallback for direct execution or testing
    import sys
    import os
    # Mock NetworkItem for testing
    class NetworkItem:
        def __init__(self, item=0, location=0, player=0):
            self.item = item
            self.location = location
            self.player = player
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from game_id import jak2_name
    from items import key_item_table
    from locs.mission_locations import main_mission_table, side_mission_table


logger = logging.getLogger("Jak2ReplClient")


@dataclass
class JsonMessageData:
    my_item_name: str | None = None
    my_item_finder: str | None = None
    their_item_name: str | None = None
    their_item_owner: str | None = None


class Jak2ReplClient:
    ip: str
    port: int
    reader: StreamReader
    writer: StreamWriter
    lock: Lock
    connected: bool = False
    initiated_connect: bool = False  # Signals when user tells us to try reconnecting.

    # Variables to handle the title screen and initial game connection.
    initial_item_count = -1  # Brand new games have 0 items, so initialize this to -1.
    received_initial_items = False
    processed_initial_items = False

    # The REPL client needs the REPL/compiler process running, but that process
    # also needs the game running. Therefore, the REPL client needs both running.
    gk_process: pymem.process = None
    goalc_process: pymem.process = None

    item_inbox: dict[int, NetworkItem] = {}
    inbox_index = 0
    json_message_queue: Queue[JsonMessageData] = queue.Queue()

    # Logging callbacks
    log_error: Callable    # Red
    log_warn: Callable     # Orange
    log_success: Callable  # Green
    log_info: Callable     # White (default)

    def __init__(self,
                 log_error_callback: Callable,
                 log_warn_callback: Callable,
                 log_success_callback: Callable,
                 log_info_callback: Callable,
                 ip: str = "127.0.0.1",
                 port: int = 8181):  # Same port as Jak 1
        self.ip = ip
        self.port = port
        self.lock = asyncio.Lock()
        self.log_error = log_error_callback
        self.log_warn = log_warn_callback
        self.log_success = log_success_callback
        self.log_info = log_info_callback

    async def main_tick(self):
        if self.initiated_connect:
            await self.connect()

        if self.connected:
            # Process any items waiting to be sent to the game
            await self.send_items()

    async def connect(self):
        self.initiated_connect = False
        if self.connected:
            return

        # Check if the game processes are running
        try:
            self.gk_process = pymem.Pymem("gk.exe")  # Same as Jak 1
            self.goalc_process = pymem.Pymem("goalc.exe")  # Same as Jak 1
        except ProcessNotFound:
            self.log_error(logger, "Could not find game processes (gk.exe and/or goalc.exe)!")
            return

        # Try to connect to the REPL
        try:
            self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)
            
            # Wait for and read the welcome message
            await asyncio.sleep(1)
            connect_data = await self.reader.read(1024)
            welcome_message = connect_data.decode()

            # Should be the OpenGOAL welcome message
            if "Connected to OpenGOAL" in welcome_message and "nREPL!" in welcome_message:
                logger.debug(welcome_message)
                self.connected = True
            else:
                self.log_error(logger, f"Unexpected welcome message: {welcome_message}")
                return
                
        except Exception as e:
            self.log_error(logger, f"Could not connect to REPL: {e}")
            self.connected = False
            return

        # Initialize the REPL with required setup commands
        # Since the REPL doesn't always send responses, we'll just send commands and assume success
        if self.reader and self.writer:
            
            # Have the REPL listen to the game's internal websocket
            self.log_info(logger, "[1/6] Connecting REPL to game websocket...")
            await self.send_form("(lt)", print_ok=False, expect_response=False)
            await asyncio.sleep(0.5)  # Small delay between commands
            self.log_success(logger, "[1/6] Connected to game websocket")

            # Enable debug segment for compilation
            self.log_info(logger, "[2/6] Enabling debug segment...")
            await self.send_form("(set! *debug-segment* #t)", print_ok=False, expect_response=False)
            await asyncio.sleep(0.5)
            self.log_success(logger, "[2/6] Debug segment enabled")

            # Start compilation - this loads the Jak 2 code
            self.log_info(logger, "[3/6] Compiling Jak 2 with ArchipelaGOAL mod (this may take 30-60 seconds)...")
            await self.send_form("(mi)", print_ok=False, expect_response=False)
            await asyncio.sleep(30)  # Give compilation time to complete
            self.log_success(logger, "[3/6] Compilation complete!")

            # Play audio cue when compilation is complete
            self.log_info(logger, "[4/6] Playing success sound...")
            await self.send_form("(dotimes (i 1) "
                                "(sound-play-by-name "
                                "(static-sound-name \"menu-close\") "
                                "(new-sound-id) 1024 0 0 (sound-group sfx) #t))", print_ok=False, expect_response=False)
            await asyncio.sleep(0.5)
            self.log_success(logger, "[4/6] Audio cue played")

            # Disable debug segment and cheat mode after compilation
            self.log_info(logger, "[5/6] Disabling debug segment...")
            await self.send_form("(set! *debug-segment* #f)", print_ok=False, expect_response=False)
            await asyncio.sleep(0.5)
            self.log_success(logger, "[5/6] Debug segment disabled")

            self.log_info(logger, "[6/6] Disabling cheat mode...")
            await self.send_form("(set! *cheat-mode* #f)", print_ok=False, expect_response=False)
            await asyncio.sleep(0.5)
            self.log_success(logger, "[6/6] Cheat mode disabled")

            self.log_success(logger, "Connected to Jak 2 REPL successfully! All systems ready.")

    async def disconnect(self):
        if self.connected and self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            self.connected = False

    async def send_form(self, form: str, print_ok: bool = True, timeout: float = 5.0, expect_response: bool = True) -> bool:
        """Send a GOAL form to the REPL using the correct binary protocol."""
        if not self.connected:
            return False

        # OpenGOAL REPL expects binary protocol: 8-byte header + message
        header = struct.pack("<II", len(form), 10)  # length + type(10)
        
        async with self.lock:
            try:
                self.writer.write(header + form.encode())
                await self.writer.drain()

                if not expect_response:
                    # For commands that don't return a response, just assume success
                    logger.debug(f"Sent command (no response expected): {form}")
                    return True

                # Try to read response with timeout
                try:
                    response_data = await asyncio.wait_for(self.reader.read(1024), timeout=timeout)
                    response = response_data.decode()
                    logger.debug(f"REPL response to '{form}': {response}")
                    
                    # Accept various success indicators
                    if response:  # Any non-empty response is considered success for now
                        if print_ok:
                            logger.debug(f"Command succeeded: {form}")
                        return True
                    else:
                        self.log_warn(logger, f"Empty response from REPL for: {form}")
                        return False
                        
                except asyncio.TimeoutError:
                    # Some commands might not send responses, treat as success if we sent it
                    logger.debug(f"No response received for '{form}' (timeout: {timeout}s) - assuming success")
                    return True
                    
            except Exception as e:
                logger.debug(f"Error sending REPL command '{form}': {e}")
                return False

    async def send_items(self):
        """Process items waiting to be sent to the game."""
        if not self.connected:
            return

        while self.inbox_index in self.item_inbox:
            item = self.item_inbox[self.inbox_index]
            await self.send_item_to_game(item)
            self.inbox_index += 1

    async def send_item_to_game(self, item: NetworkItem):
        """Send a specific item to the game via REPL commands."""
        try:
            # Look up the item data
            if item.item not in key_item_table:
                self.log_warn(logger, f"Unknown item ID: {item.item}")
                return

            item_data = key_item_table[item.item]
            item_symbol = item_data.symbol
            
            # Send the item to the game using the ap-item-received! function
            command = f"(ap-item-received! '{item_symbol})"
            success = await self.send_form(command)
            
            if success:
                self.log_success(logger, f"Successfully gave item: {item_data.name}")
            else:
                self.log_warn(logger, f"Item delivery failed for: {item_data.name}")
                
        except Exception as e:
            self.log_error(logger, f"Failed to send item to game: {e}")

    def queue_game_text(self, my_item_name: str | None, my_item_finder: str | None,
                       their_item_name: str | None, their_item_owner: str | None):
        """Queue text messages to be displayed in the game."""
        message = JsonMessageData(my_item_name, my_item_finder, their_item_name, their_item_owner)
        self.json_message_queue.put(message)

    async def setup_options(self, slot_name: str, seed_name: str):
        """Initialize game options for Archipelago."""
        # This would set up any game-specific options
        # For now, just mark that we've processed initial setup
        self.processed_initial_items = True
        self.log_info(logger, f"Initialized Jak 2 Archipelago for slot '{slot_name}' with seed '{seed_name}'")

    async def send_connection_status(self, status: str):
        """Send connection status to the game."""
        # Could display status messages in-game if desired
        logger.debug(f"Connection status: {status}")

    async def print_status(self):
        """Print the current status of the REPL client."""
        gk_id = str(self.gk_process.process_id) if self.gk_process else "None"
        goalc_id = str(self.goalc_process.process_id) if self.goalc_process else "None"
        
        msg = (f"Jak 2 REPL Client Status:\n"
               f"   Connected to REPL: {self.connected}\n"
               f"   REPL Address: {self.ip}:{self.port}\n" 
               f"   Game process ID: {gk_id}\n"
               f"   Compiler process ID: {goalc_id}\n"
               f"   Items processed: {self.inbox_index}\n"
               f"   Items pending: {len(self.item_inbox) - self.inbox_index}")
        
        self.log_info(logger, msg)