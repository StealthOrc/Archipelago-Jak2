class Jak2ItemData:
    id: int
    name: str
    symbol: str
    
    def __init__(self, item_id: int, name: str, symbol: str) -> None:
        self.item_id = item_id
        self.name = name
        self.symbol = symbol

key_item_table = {
    # morph gun shit
    1: Jak2ItemData(item_id=1, name="Scatter Gun", symbol="gun-red"),
    2: Jak2ItemData(item_id=2, name="Blaster", symbol="gun-yellow"),
    3: Jak2ItemData(item_id=3, name="Vulcan Fury", symbol="gun-blue"),
    4: Jak2ItemData(item_id=4, name="Peacemaker", symbol="gun-dark"),
    5: Jak2ItemData(item_id=5, name="Morph Gun Ammo Upgrade", symbol="gun-upgrade-ammo"),
    6: Jak2ItemData(item_id=6, name="Morph Gun Fire Rate Upgrade", symbol="gun-upgrade-speed"),
    7: Jak2ItemData(item_id=7, name="Morph Gun Damage Upgrade", symbol="gun-upgrade-damage"),
    # jet-board
    8: Jak2ItemData(item_id=8, name="JET-Board", symbol="board"),
    # dark jak shit
    9: Jak2ItemData(item_id=9, name="Dark Jak", symbol="darkjak"),
    10: Jak2ItemData(item_id=10, name="Dark Bomb", symbol="darkjak-bomb0"),
    11: Jak2ItemData(item_id=11, name="Dark Blast", symbol="darkjak-bomb1"),
    12: Jak2ItemData(item_id=12, name="Dark Giant", symbol="darkjak-giant"),
    13: Jak2ItemData(item_id=13, name="Dark Invincibility", symbol="darkjak-invinc"),
    # security pass shit
    14: Jak2ItemData(item_id=14, name="Red Security Pass", symbol="pass-red"),
    15: Jak2ItemData(item_id=15, name="Yellow Security Pass", symbol="pass-yellow"),
    16: Jak2ItemData(item_id=16, name="Green Security Pass", symbol="pass-green"),
    17: Jak2ItemData(item_id=17, name="Purple Security Pass", symbol="pass-purple"),
    18: Jak2ItemData(item_id=18, name="Black Security Pass", symbol="pass-black"),
    19: Jak2ItemData(item_id=19, name="Air Train Pass", symbol="pass-air-train"),
    # mountain temple shit
    20: Jak2ItemData(item_id=20, name="Lens", symbol="lens"),
    21: Jak2ItemData(item_id=21, name="Gear", symbol="gear"),
    22: Jak2ItemData(item_id=22, name="Shard", symbol="shard"),
    # misc but important shit
    23: Jak2ItemData(item_id=23, name="Ruby Key", symbol="ruby-key"),
    24: Jak2ItemData(item_id=24, name="Heart of Mar", symbol="heart-of-mar"),
    25: Jak2ItemData(item_id=25, name="Time Map", symbol="time-map"),
    26: Jak2ItemData(item_id=26, name="Precursor Stone", symbol="precursor-stone"),
    27: Jak2ItemData(item_id=27, name="Life Seed", symbol="life-seed"),
    28: Jak2ItemData(item_id=28, name="Titan Suit", symbol="titan-suit"),
    29: Jak2ItemData(item_id=29, name="Gunpod", symbol="gun-turret"),
    30: Jak2ItemData(item_id=30, name="Seal Piece #1", symbol="seal-piece-1"),
    31: Jak2ItemData(item_id=31, name="Seal Piece #2", symbol="seal-piece-2"),
    32: Jak2ItemData(item_id=32, name="Seal Piece #3", symbol="seal-piece-3"),
    33: Jak2ItemData(item_id=33, name="Rift Rider", symbol="rift-rider")
}