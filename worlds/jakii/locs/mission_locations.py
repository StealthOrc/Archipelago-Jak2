from typing import Callable

class Jak2MissionData:
    id: int
    name: str
    rule: Callable

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

class Jak2SideMissionData:
    id: int
    name: str
    rule: Callable

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

# Names for Missions are taken directly from the game
main_mission_table = {
    # Act 1
    1: Jak2MissionData(id=1, name="Escape From Prison"),
    2: Jak2MissionData(id=2, name="Protect Kor and Kid"),
    3: Jak2MissionData(id=3, name="Retrieve Banner from Dead Town"),
    4: Jak2MissionData(id=4, name="Find Pumping Station Valve"),
    5: Jak2MissionData(id=5, name="Blow up Ammo at Fortress"),
    6: Jak2MissionData(id=6, name="Make delivery to Hip Hog Saloon"),
    7: Jak2MissionData(id=7, name="Beat Scatter Gun Course"),
    8: Jak2MissionData(id=8, name="Protect Sig at Pumping Station"),
    9: Jak2MissionData(id=9, name="Destroy Turrets in Sewers"),
    10: Jak2MissionData(id=10, name="Rescue Vin at Strip Mine"),
    11: Jak2MissionData(id=11, name="Find Pumping Station Patrol"),
    12: Jak2MissionData(id=12, name="Find Lens in Mountain Temple"),
    13: Jak2MissionData(id=13, name="Find Gear in Mountain Temple"),
    14: Jak2MissionData(id=14, name="Find Shard in Mountain Temple"),
    15: Jak2MissionData(id=15, name="Beat Time to Race Garage"),
    16: Jak2MissionData(id=16, name="Win JET-Board Stadium Challenge"),
    17: Jak2MissionData(id=17, name="Collect Money for Krew"),
    18: Jak2MissionData(id=18, name="Beat Blaster Gun Course"),
    19: Jak2MissionData(id=19, name="Destroy Eggs at Drill Platform"),
    20: Jak2MissionData(id=20, name="Turn on 5 Power Switches"),
    21: Jak2MissionData(id=21, name="Ride Elevator up to Palace"),
    22: Jak2MissionData(id=22, name="Defeat Baron at Palace"),
    # Act 2 (Palace Baron Fight Complete)
    23: Jak2MissionData(id=23, name="Shuttle Underground Fighters"),
    24: Jak2MissionData(id=24, name="Protect Site in Dead Town"),
    25: Jak2MissionData(id=25, name="Catch Scouts in Haven Forest"),
    26: Jak2MissionData(id=26, name="Escort Kid to Power Station"),
    27: Jak2MissionData(id=27, name="Destroy Equipment at Dig"),
    28: Jak2MissionData(id=28, name="Blow up Strip Mine Eco Wells"),
    29: Jak2MissionData(id=29, name="Destroy Ship at Drill Platform"),
    30: Jak2MissionData(id=30, name="Destroy Cargo in Port"),
    31: Jak2MissionData(id=31, name="Rescue Lurkers for Brutter #1"),
    32: Jak2MissionData(id=32, name="Drain Sewers to find Statue"),
    33: Jak2MissionData(id=33, name="Hunt Haven Forest Metal Heads"),
    34: Jak2MissionData(id=34, name="Intercept Tanker"),
    35: Jak2MissionData(id=35, name="Win Class 3 Race at Stadium"),
    36: Jak2MissionData(id=36, name="Get Seal Piece at Water Slums"),
    37: Jak2MissionData(id=37, name="Get Seal Piece at Dig"),
    38: Jak2MissionData(id=38, name="Destroy 5 HellCat Cruisers"),
    39: Jak2MissionData(id=39, name="Beat Onin Game"),
    40: Jak2MissionData(id=40, name="Use items in No Man's Canyon"),
    41: Jak2MissionData(id=41, name="Pass the first Test of Manhood"),
    42: Jak2MissionData(id=42, name="Pass the second Test of Manhood"),
    43: Jak2MissionData(id=43, name="Defeat Baron in Mar's Tomb"),
    # Act 3 (Tomb Baron Fight Complete)
    44: Jak2MissionData(id=44, name="Rescue Friends in Fortress"),
    45: Jak2MissionData(id=45, name="Escort men through Sewers"),
    46: Jak2MissionData(id=46, name="Win Class 2 Race at Stadium"),
    47: Jak2MissionData(id=47, name="Protect Hideout from Bombots"),
    48: Jak2MissionData(id=48, name="Beat Erol in Race Challenge"),
    49: Jak2MissionData(id=49, name="Destroy Eggs in Strip Mine"),
    50: Jak2MissionData(id=50, name="Get Life Seed in Dead Town"),
    51: Jak2MissionData(id=51, name="Protect Samos in Haven Forest"),
    52: Jak2MissionData(id=52, name="Destroy Drill Platform Tower"),
    53: Jak2MissionData(id=53, name="Rescue Lurkers for Brutter #2"),
    54: Jak2MissionData(id=54, name="Win Class 1 Race at Stadium"),
    55: Jak2MissionData(id=55, name="Explore Palace"),
    56: Jak2MissionData(id=56, name="Get Heart of Mar in Weapons Lab"),
    57: Jak2MissionData(id=57, name="Beat Krew in Weapons Lab"),
    58: Jak2MissionData(id=58, name="Beat the Metal Head Mash Game"),
    59: Jak2MissionData(id=59, name="Find Sig in Under Port"),
    60: Jak2MissionData(id=60, name="Escort Sig in Under Port"),
    61: Jak2MissionData(id=61, name="Defend Stadium"),
    62: Jak2MissionData(id=62, name="Check the Construction Site"),
    63: Jak2MissionData(id=63, name="Break Barrier at Nest"),
    64: Jak2MissionData(id=64, name="Attack the Metal Head Nest"),
    65: Jak2MissionData(id=65, name="Destroy Metal Kor at Nest")
}

# Names of Side Missions are taken from the Fandom Jak II Wiki
side_mission_table = {
    # Orb Searches
    1: Jak2SideMissionData(id=1, name="Orb Search 1 (Computer #2)"),
    2: Jak2SideMissionData(id=2, name="Orb Search 2 (Computer #3)"),
    3: Jak2SideMissionData(id=3, name="Orb Search 3 (Computer #4)"),
    4: Jak2SideMissionData(id=4, name="Orb Search 4 (Computer #5)"),
    5: Jak2SideMissionData(id=5, name="Orb Search 5 (Computer #9)"),
    6: Jak2SideMissionData(id=6, name="Orb Search 6 (Computer #10)"),
    7: Jak2SideMissionData(id=7, name="Orb Search 7 (Computer #11)"),
    8: Jak2SideMissionData(id=8, name="Orb Search 8 (Computer #12)"),
    9: Jak2SideMissionData(id=9, name="Orb Search 9 (Computer #6)"),
    10: Jak2SideMissionData(id=10, name="Orb Search 10 (Computer #14)"),
    11: Jak2SideMissionData(id=11, name="Orb Search 11 (Computer #15)"),
    12: Jak2SideMissionData(id=12, name="Orb Search 12 (Computer #7)"),
    13: Jak2SideMissionData(id=13, name="Orb Search 13 (Computer #16)"),
    14: Jak2SideMissionData(id=14, name="Orb Search 14 (Computer #17)"),
    15: Jak2SideMissionData(id=15, name="Orb Search 15 (Computer #18)"),
    # Ring Races
    16: Jak2SideMissionData(id=16, name="Ring Race 1 (Computer #1)"),
    17: Jak2SideMissionData(id=17, name="Ring Race 2 (Computer #8)"),
    18: Jak2SideMissionData(id=18, name="Ring Race 3 (Computer #1)"),
    # Orb Collections
    19: Jak2SideMissionData(id=19, name="Collection 1 (Computer #6)"),
    20: Jak2SideMissionData(id=20, name="Collection 2 (Computer #13)"),
    21: Jak2SideMissionData(id=21, name="Collection 3 (Computer #12)"),
    # Missions Turned Side Missions
    22: Jak2SideMissionData(id=22, name="Deliver Package Side Mission (Computer #7)"),
    23: Jak2SideMissionData(id=23, name="Shuttle Underground Fighters Side Mission (Computer #7)"),
    24: Jak2SideMissionData(id=24, name="Destroy Blast Bots Side Mission (Computer #7)"),
    # Extra Race Missions
    25: Jak2SideMissionData(id=25, name="Erol Race Side Mission"),
    26: Jak2SideMissionData(id=26, name="Port Race Side Mission"),
    # Stadium Challenges
    27: Jak2SideMissionData(id=27, name="JET-Board Stadium Challenge Side Mission"),
    28: Jak2SideMissionData(id=28, name="Class 3 Race Side Mission (Computer by Stadium)"),
    29: Jak2SideMissionData(id=29, name="Class 2 Race Side Mission (Computer by Stadium)"),
    30: Jak2SideMissionData(id=30, name="Class 1 Race Side Mission (Computer by Stadium)"),
    31: Jak2SideMissionData(id=31, name="Class 3R Race Side Mission (Computer by Stadium)"),
    32: Jak2SideMissionData(id=32, name="Class 2R Race Side Mission (Computer by Stadium)"),
    33: Jak2SideMissionData(id=33, name="Class 1R Race Side Mission (Computer by Stadium)")
}