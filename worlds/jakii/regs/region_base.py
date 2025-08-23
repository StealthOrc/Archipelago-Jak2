from typing import Iterable
from ..game_id import jak2_name
from BaseClasses import MultiWorld, Region
from ..locs import mission_locations as missions
from ..locations import (JakIILocation, all_locations_table)
from worlds.generic.Rules import CollectionRule


class JakIIRegion(Region):
    """
    Holds information such as name, level name, etc.
    """

    game = jak2_name
    location_count: int = 0

    def __init__(self, name: str, player: int, multiworld: MultiWorld):
        super().__init__(name, player, multiworld)

    def add_jak_mission(self, loc_id: int, name: str, access_rule: CollectionRule | None = None) -> None:
        """
        Helper function to add Locations. Not to be used directly.
        """
        location = JakIILocation(self.player, name, loc_id, self)
        if access_rule:
            location.access_rule = lambda state: access_rule(state, self.player)
        self.locations.append(location)
        self.location_count += 1