#Archipelago Imports
import settings
from worlds.AutoWorld import World, WebWorld
from BaseClasses import (Tutorial)

# Jak 2 imports
from .game_id import jak2_name
from .items import (key_item_table, symbol_lookup)
from .locations import (JakIILocation, all_locations_table)

class JakIIWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up ArchipelaGOAL II (Archipelago on OpenGOAL)",
        "English",
        "setup_en.md",
        "setup/en",
        ["narramoment"]
    )

    tutorials = [setup_en]
    bug_report_page = "https://github.com/narramoment/Archipelago/issues"

class JakIIWorld(World):
    """
    Jak II is an action-adventure game published by Naughty Dog in 2003 for the PlayStation 2.
    Set directly after the events of Jak and Daxter: The Precursor Legacy, Jak, Daxter, Samos
    and Keira have set up the Rift Rider they found at the end of their previous adventure, and
    are ready to see where it leads. However, a strange and hostile species of creatures known as
    Metal Heads suddenly fly through the portal, and in a panic, Daxter activates the machine,
    sending them flying through the open portal. Separated, they find themselves in "glorious" Haven City,
    and Jak is quickly captured. Two years later, Daxter finds Jak locked up in prison,
    and Jak has only one thought on his mind: vengeance.
    """

    game = jak2_name

    web = JakIIWebWorld

    item_name_to_id = {name: k for k, name in key_item_table.items()}
    location_name_to_id = {name: k for k, name in all_locations_table.items()}
    item_name_groups = {}
    location_name_groups = {}
