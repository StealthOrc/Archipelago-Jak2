from typing import Callable

from worlds.jakii.rules import (slums_to_port,
                                slums_to_stadium,
                                slums_to_market,
                                port_to_stadium,
                                port_to_market,
                                market_to_stadium,
                                slums_to_landing,
                                slums_to_nest,
                                any_gun)



class Jak2MissionData:
    id: int
    name: str
    rule: Callable

    def __init__(self, mission_id: int, name: str, rule: Callable | None = None):
        self.mission_id = mission_id
        self.name = name
        if rule:
            self.rule = rule
        else:
            self.rule = lambda state, player: True

class Jak2SideMissionData:
    id: int
    name: str
    rule: Callable

    def __init__(self, mission_id: int, name: str, rule: Callable | None = None):
        self.mission_id = mission_id
        self.name = name
        if rule:
            self.rule = rule
        else:
            self.rule = lambda state, player: True

# Names for Missions are taken directly from the game
main_mission_table = {
    # Act 1
    1: Jak2MissionData(mission_id=1, name="Escape From Prison"),
    2: Jak2MissionData(mission_id=2, name="Protect Kor and Kid", rule=lambda state, player:
    (state.has("Dark Jak"), player)),
    3: Jak2MissionData(mission_id=3, name="Retrieve Banner from Dead Town"),
    4: Jak2MissionData(mission_id=4, name="Find Pumping Station Valve"),
    5: Jak2MissionData(mission_id=5, name="Blow up Ammo at Fortress"),
    6: Jak2MissionData(mission_id=6, name="Make delivery to Hip Hog Saloon", rule=lambda state, player:
                        state.has_any(("Red Security Pass", "Yellow Security Pass"), player)),
    7: Jak2MissionData(mission_id=7, name="Beat Scatter Gun Course", rule=lambda state, player:
                        slums_to_port(state, player) and state.has("Scatter Gun", player)),
    8: Jak2MissionData(mission_id=8, name="Protect Sig at Pumping Station", rule=lambda state, player:
                        slums_to_port(state, player) and any_gun(state, player)),
    9: Jak2MissionData(mission_id=9, name="Destroy Turrets in Sewers", rule=lambda state, player:
                        slums_to_port(state, player) and any_gun(state, player)),
    10: Jak2MissionData(mission_id=10, name="Rescue Vin at Strip Mine", rule=lambda state, player:
                        slums_to_port(state, player) and any_gun(state, player)),
    11: Jak2MissionData(mission_id=11, name="Find Pumping Station Patrol", rule=lambda state, player:
                        any_gun(state, player)),
    12: Jak2MissionData(mission_id=12, name="Find Lens in Mountain Temple", rule=lambda state, player:
                        slums_to_market(state, player)
                        and state.has_any(("Scatter Gun", "Blaster", "Vulcan Fury"), player)),
    13: Jak2MissionData(mission_id=13, name="Find Gear in Mountain Temple", rule=lambda state, player:
                        slums_to_market(state, player)
                        and state.has_any(("Scatter Gun", "Blaster", "Vulcan Fury"), player)),
    14: Jak2MissionData(mission_id=14, name="Find Shard in Mountain Temple", rule=lambda state, player:
                        slums_to_market(state, player)
                        and state.has_any(("Scatter Gun", "Blaster", "Vulcan Fury"), player)),
    15: Jak2MissionData(mission_id=15, name="Beat Time to Race Garage", rule=lambda state, player:
                        state.has_all(("Red Security Pass", "Green Security Pass"), player)
                        or state.has("Yellow Security Pass", player)),
    16: Jak2MissionData(mission_id=16, name="Win JET-Board Stadium Challenge", rule=lambda state, player:
                        slums_to_market(state, player)),
    17: Jak2MissionData(mission_id=17, name="Collect Money for Krew", rule=lambda state, player:
                        slums_to_port(state, player)),
    18: Jak2MissionData(mission_id=18, name="Beat Blaster Gun Course", rule=lambda state, player:
                        slums_to_port(state, player) and state.has("Blaster", player)),
    19: Jak2MissionData(mission_id=19, name="Destroy Eggs at Drill Platform", rule=lambda state, player:
                        slums_to_port(state, player) and any_gun(state, player) and state.has("Gunpod", player)),
    20: Jak2MissionData(mission_id=20, name="Turn on 5 Power Switches", rule=lambda state, player:
                        slums_to_port(state, player)),
    21: Jak2MissionData(mission_id=21, name="Ride Elevator up to Palace", rule=lambda state, player:
                        any_gun(state, player)
                        and slums_to_stadium(state, player)),
    22: Jak2MissionData(mission_id=22, name="Defeat Baron at Palace", rule = lambda state, player:
                        any_gun(state, player)
                        and slums_to_stadium(state, player)),
    # Act 2 (Palace Baron Fight Complete)
    23: Jak2MissionData(mission_id=23, name="Shuttle Underground Fighters"),
    24: Jak2MissionData(mission_id=24, name="Protect Site in Dead Town", rule=lambda state, player:
                        any_gun(state, player)),
    25: Jak2MissionData(mission_id=25, name="Catch Scouts in Haven Forest", rule=lambda state, player:
                        slums_to_market(state, player)
                        and state.has("JET-Board", player)),
    26: Jak2MissionData(mission_id=26, name="Escort Kid to Power Station", rule=lambda state, player:
                        state.has("Red Security Pass", player)),
    27: Jak2MissionData(mission_id=27, name="Destroy Equipment at Dig", rule=lambda state, player:
                        slums_to_port(state, player)
                        and state.has("JET-Board", player)),
    28: Jak2MissionData(mission_id=28, name="Blow up Strip Mine Eco Wells", rule=lambda state, player:
                        slums_to_port(state, player)
                        and state.has("JET-Board", player)),
    29: Jak2MissionData(mission_id=29, name="Destroy Ship at Drill Platform", rule=lambda state, player:
                        slums_to_port(state, player)
                        and state.has("Gunpod", player)),
    30: Jak2MissionData(mission_id=30, name="Destroy Cargo in Port", rule=lambda state, player:
                        slums_to_port(state, player)
                        and state.has("JET-Board", player)),
    31: Jak2MissionData(mission_id=31, name="Rescue Lurkers for Brutter #1", rule=lambda state, player:
                        slums_to_port(state, player)
                        and any_gun(state, player)
                        and state.has("Yellow Security Pass", player)),
    32: Jak2MissionData(mission_id=32, name="Drain Sewers to find Statue", rule=lambda state, player:
                        slums_to_port(state, player)
                        and state.has("JET-Board", player)),
    33: Jak2MissionData(mission_id=33, name="Hunt Haven Forest Metal Heads", rule=lambda state, player:
                        slums_to_port(state, player)
                        and any_gun(state, player)
                        and state.has("Yellow Security Pass", player)),
    34: Jak2MissionData(mission_id=34, name="Intercept Tanker", rule=lambda state, player:
                        slums_to_market(state, player)
                        and (any_gun(state, player)
                        or state.has("Dark Jak", player))),
    35: Jak2MissionData(mission_id=35, name="Win Class 3 Race at Stadium", rule=lambda state, player:
                        slums_to_stadium(state, player)),
    36: Jak2MissionData(mission_id=36, name="Get Seal Piece at Water Slums", rule=lambda state, player:
                        any_gun(state, player)
                        or state.has("JET-Board", player)),
    37: Jak2MissionData(mission_id=37, name="Get Seal Piece at Dig", rule=lambda state, player:
                        slums_to_market(state, player)
                        and any_gun(state, player)
                        and state.has("JET-Board", player)),
    38: Jak2MissionData(mission_id=38, name="Destroy 5 HellCat Cruisers", rule=lambda state, player:
                        state.has("Red Security Pass", player)
                        and any_gun(state, player)),
    39: Jak2MissionData(mission_id=39, name="Beat Onin Game", rule=lambda state, player:
                        slums_to_market(state, player)),
    40: Jak2MissionData(mission_id=40, name="Use items in No Man's Canyon", rule=lambda state, player:
                        slums_to_market(state, player)
                        and state.has("JET-Board", player)
                        and state.has_all("Seal Piece #1", "Seal Piece #2", "Seal Piece #3")),
    41: Jak2MissionData(mission_id=41, name="Pass the first Test of Manhood", rule=lambda state, player:
                        slums_to_market(state, player)
                        and state.has_all("Lens", "Gear", "Shard")),
    42: Jak2MissionData(mission_id=42, name="Pass the second Test of Manhood", rule=lambda state, player:
                        slums_to_market(state, player)
                        and state.has_all("Lens", "Gear", "Shard")),
    43: Jak2MissionData(mission_id=43, name="Defeat Baron in Mar's Tomb", rule=lambda state, player:
                        slums_to_market(state, player)
                        and any_gun(state, player)),
    # Act 3 (Tomb Baron Fight Complete)
    44: Jak2MissionData(mission_id=44, name="Rescue Friends in Fortress", rule=lambda state, player:
                        slums_to_market(state, player)
                        and any_gun(state, player)
                        and state.has("JET-Board", player)),
    45: Jak2MissionData(mission_id=45, name="Escort men through Sewers", rule=lambda state, player:
                        slums_to_port(state, player)
                        and any_gun(state, player)),
    46: Jak2MissionData(mission_id=46, name="Win Class 2 Race at Stadium", rule=lambda state, player:
                        slums_to_stadium(state, player)),
    47: Jak2MissionData(mission_id=47, name="Protect Hideout from Bombots", rule=lambda state, player:
                        state.has_all("Red Security Pass", "Vulcan Fury")),
    48: Jak2MissionData(mission_id=48, name="Beat Erol in Race Challenge", rule=lambda state, player:
                        slums_to_port(state, player)
                        and state.has("Yellow Security Pass", player)),
    49: Jak2MissionData(mission_id=49, name="Destroy Eggs in Strip Mine", rule=lambda state, player:
                        slums_to_port(state, player)
                        and state.has("JET-Board", player)),
    50: Jak2MissionData(mission_id=50, name="Get Life Seed in Dead Town", rule=lambda state, player:
                        any_gun(state, player)
                        and state.has("Titan Suit", player)),
    51: Jak2MissionData(mission_id=51, name="Protect Samos in Haven Forest", rule=lambda state, player:
                        slums_to_market(state, player)
                        and any_gun(state, player)
                        and state.has("Life Seed", player)),
    52: Jak2MissionData(mission_id=52, name="Destroy Drill Platform Tower", rule=lambda state, player:
                        slums_to_port(state, player)
                        and (state.has("Titan Suit", player)
                             and state.has_any("Blaster", "Vulcan Fury"))),
    53: Jak2MissionData(mission_id=53, name="Rescue Lurkers for Brutter #2", rule=lambda state, player:
                        slums_to_market(state, player)
                        and (state.has("Yellow Security Pass", player))
                        and any_gun(state, player)),
    54: Jak2MissionData(mission_id=54, name="Win Class 1 Race at Stadium", rule=lambda state, player:
                        slums_to_stadium(state, player)),
    55: Jak2MissionData(mission_id=55, name="Explore Palace", rule=lambda state, player:
                        slums_to_market(state, player)
                        and state.has_all(("JET-Board", "Purple Security Pass"), player)
                        and any_gun(state, player)),
    56: Jak2MissionData(mission_id=56, name="Get Heart of Mar in Weapons Lab", rule=lambda state, player:
                        slums_to_landing(state, player)
                        and state.has("Black Security Pass", player)
                        and any_gun(state, player)),
    57: Jak2MissionData(mission_id=57, name="Beat Krew in Weapons Lab", rule=lambda state, player:
                        slums_to_landing(state, player)
                        and state.has("Black Security Pass", player)
                        and any_gun(state, player)),
    58: Jak2MissionData(mission_id=58, name="Beat the Metal Head Mash Game", rule=lambda state, player:
                        slums_to_port(state, player)),
    59: Jak2MissionData(mission_id=59, name="Find Sig in Under Port", rule=lambda state, player:
                        slums_to_port(state, player)
                        and state.has_all("Ruby Key", "Titan Suit")),
    60: Jak2MissionData(mission_id=60, name="Escort Sig in Under Port", rule=lambda state, player:
                        slums_to_port(state, player)
                        and state.has_all("Ruby Key", "Titan Suit")
                        and any_gun(state, player)),
    61: Jak2MissionData(mission_id=61, name="Defend Stadium", rule=lambda state, player:
                        slums_to_stadium(state, player)
                        and state.has_all("Heart of Mar", "Time Map", "Rift Rider")
                        and any_gun(state, player)),
    62: Jak2MissionData(mission_id=62, name="Check the Construction Site", rule=lambda state, player:
                        slums_to_port(state, player)),
    63: Jak2MissionData(mission_id=63, name="Break Barrier at Nest", rule=lambda state, player:
                        slums_to_nest(state, player)
                        and state.has("Precursor Stone")
                        and any_gun(state, player)),
    64: Jak2MissionData(mission_id=64, name="Attack the Metal Head Nest", rule=lambda state, player:
                        slums_to_nest(state, player)
                        and state.has("Precursor Stone")
                        and any_gun(state, player)),
    65: Jak2MissionData(mission_id=65, name="Destroy Metal Kor at Nest", rule=lambda state, player:
                        slums_to_nest(state, player)
                        and state.has("Precursor Stone")
                        and any_gun(state, player))
}

# Names of Side Missions are taken from the Fandom Jak II Wiki
side_mission_table = {
    # Orb Searches
    1: Jak2SideMissionData(mission_id=1, name="Orb Search 1 (Computer #2)"),
    2: Jak2SideMissionData(mission_id=2, name="Orb Search 2 (Computer #3)", rule=lambda state, player:
                           slums_to_port(state, player)),
    3: Jak2SideMissionData(mission_id=3, name="Orb Search 3 (Computer #4)", rule=lambda state, player:
                           slums_to_port(state, player)),
    4: Jak2SideMissionData(mission_id=4, name="Orb Search 4 (Computer #5)"),
    5: Jak2SideMissionData(mission_id=5, name="Orb Search 5 (Computer #9)", rule=lambda state, player:
                           slums_to_market(state, player)),
    6: Jak2SideMissionData(mission_id=6, name="Orb Search 6 (Computer #10)", rule=lambda state, player:
                           slums_to_market(state, player)),
    7: Jak2SideMissionData(mission_id=7, name="Orb Search 7 (Computer #11)" , rule=lambda state, player:
                           slums_to_market(state, player)),
    8: Jak2SideMissionData(mission_id=8, name="Orb Search 8 (Computer #12)", rule=lambda state, player:
                           slums_to_market(state, player)),
    9: Jak2SideMissionData(mission_id=9, name="Orb Search 9 (Computer #6)" , rule=lambda state, player:
                           slums_to_stadium(state, player)),
    10: Jak2SideMissionData(mission_id=10, name="Orb Search 10 (Computer #14)", rule=lambda state, player:
                            slums_to_port(state, player)),
    11: Jak2SideMissionData(mission_id=11, name="Orb Search 11 (Computer #15)", rule=lambda state, player:
                            slums_to_stadium(state, player)),
    12: Jak2SideMissionData(mission_id=12, name="Orb Search 12 (Computer #7)", rule=lambda state, player:
                            state.has_all("Red Security Pass", "Yellow Security Pass")
                            or slums_to_market(state, player)),
    13: Jak2SideMissionData(mission_id=13, name="Orb Search 13 (Computer #16)", rule=lambda state, player:
                            state.has("Green Security Pass", player)),
    14: Jak2SideMissionData(mission_id=14, name="Orb Search 14 (Computer #17)", rule=lambda state, player:
                            slums_to_stadium(state, player)),
    15: Jak2SideMissionData(mission_id=15, name="Orb Search 15 (Computer #18)", rule=lambda state, player:
                            slums_to_market(state, player)),
    # Ring Races
    16: Jak2SideMissionData(mission_id=16, name="Ring Race 1 (Computer #1)"),
    17: Jak2SideMissionData(mission_id=17, name="Ring Race 2 (Computer #8)", rule=lambda state, player:
                            slums_to_port(state, player)
                            or state.has("Yellow Security Pass", player)),
    18: Jak2SideMissionData(mission_id=18, name="Ring Race 3 (Computer #1)", rule=lambda state, player:
                            state.has("Red Security Pass", player)),
    # Orb Collections
    19: Jak2SideMissionData(mission_id=19, name="Collection 1 (Computer #6)", rule=lambda state, player:
                            slums_to_stadium(state, player)),
    20: Jak2SideMissionData(mission_id=20, name="Collection 2 (Computer #13)", rule=lambda state, player:
                            slums_to_stadium(state, player)),
    21: Jak2SideMissionData(mission_id=21, name="Collection 3 (Computer #12)", rule=lambda state, player:
                            slums_to_market(state, player)),
    # Missions Turned Side Missions
    22: Jak2SideMissionData(mission_id=22, name="Deliver Package Side Mission (Computer #7)"),
    23: Jak2SideMissionData(mission_id=23, name="Shuttle Underground Fighters Side Mission (Computer #7)",
                            rule=lambda state, player: state.has_all("Red Security Pass", "Yellow Security Pass")),
    24: Jak2SideMissionData(mission_id=24, name="Destroy Blast Bots Side Mission (Computer #7)",
                            rule=lambda state, player: slums_to_market(state, player)
                                                       or state.has("Yellow Security Pass", player)),
    # Extra Race Missions
    25: Jak2SideMissionData(mission_id=25, name="Erol Race Side Mission", rule=lambda state, player:
                            slums_to_port(state, player)
                            or state.has("Yellow Security Pass", player)),
    26: Jak2SideMissionData(mission_id=26, name="Port Race Side Mission", rule=lambda state, player:
                            slums_to_port(state, player)),
    # Stadium Challenges
    27: Jak2SideMissionData(mission_id=27, name="JET-Board Stadium Challenge Side Mission", rule=lambda state, player:
                            state.has("JET-Board", player)),
    28: Jak2SideMissionData(mission_id=28, name="Class 3 Race Side Mission (Computer by Stadium)", rule=lambda state, player:
                            slums_to_stadium(state, player)),
    29: Jak2SideMissionData(mission_id=29, name="Class 2 Race Side Mission (Computer by Stadium)", rule=lambda state, player:
                            slums_to_stadium(state, player)),
    30: Jak2SideMissionData(mission_id=30, name="Class 1 Race Side Mission (Computer by Stadium)", rule=lambda state, player:
                            slums_to_stadium(state, player)),
    31: Jak2SideMissionData(mission_id=31, name="Class 3R Race Side Mission (Computer by Stadium)", rule=lambda state, player:
                            slums_to_stadium(state, player)),
    32: Jak2SideMissionData(mission_id=32, name="Class 2R Race Side Mission (Computer by Stadium)", rule=lambda state, player:
                            slums_to_stadium(state, player)),
    33: Jak2SideMissionData(mission_id=33, name="Class 1R Race Side Mission (Computer by Stadium)", rule=lambda state, player:
                            slums_to_stadium(state, player))
}