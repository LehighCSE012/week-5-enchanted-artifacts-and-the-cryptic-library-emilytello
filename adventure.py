''' 
Week 5: Enhance your text-based adventure game by using dictionaries
to manage enchanted artifacts and sets to handle unique clues in a
cryptic library.
'''
import random
def display_player_status(player_stats):
    """Displays the player's current health and attack."""
    print(f"\nPlayer Status: Health = {player_stats['health']}, Attack = {player_stats['attack']}")
def discover_artifact(player_stats, artifacts, artifact_name):
    """Handles finding an enchanted artifact and updating player stats accordingly."""
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"\nYou found an artifact: {artifact_name.replace('_', ' ').title()}!")
        print(f"Description: {artifact['description']}")
        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
            print(f"The artifact increases your health by {artifact['power']}!")
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
            print(f"The artifact enhances your attack by {artifact['power']}!")
        del artifacts[artifact_name]
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts
def find_clue(clues, new_clue):
    """Adds a new unique clue to the clues set."""
    if new_clue in clues:
        print("You already know this clue.")
    else:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    return clues
def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """Handles dungeon exploration and events."""
    for room in dungeon_rooms:
        room_name, item, challenge_type, challenge_outcome = room
        print(f"\nEntering: {room_name}")
        if room_name == "Cryptic Library":
            print("A vast library filled with ancient, cryptic texts.")
            clue_list = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows.",
                "The amulet unlocks the final door."
            ]
            found_clues = random.sample(clue_list, 2)
            for clue in found_clues:
                clues = find_clue(clues, clue)
            if "staff_of_wisdom" in inventory:
                print("With the Staff of Wisdom, you understand the meaning of the", 
                " clues and can bypass a puzzle challenge later.")
        elif challenge_type == "puzzle":
            success = random.choice([True, False])
            if success:
                print(challenge_outcome[0])
            else:
                print(challenge_outcome[1])
                player_stats['health'] += challenge_outcome[2]
        elif challenge_type == "trap":
            triggered = random.choice([True, False])
            if triggered:
                print(challenge_outcome[1])
                player_stats['health'] += challenge_outcome[2]
            else:
                print(challenge_outcome[0])
        if item:
            print(f"You found a {item}!")
            inventory.append(item)
    return player_stats, inventory, clues
def combat_encounter(player_stats, monster_health, has_treasure):
    """Handles combat with a monster."""
    print("\nA monster appears!")
    while player_stats['health'] > 0 and monster_health > 0:
        player_attack = random.randint(1, player_stats['attack'])
        monster_health -= player_attack
        print(f"You attack for {player_attack} damage. Monster's health: {monster_health}")
        if monster_health > 0:
            monster_attack = random.randint(5, 15)
            player_stats['health'] -= monster_attack
            print(f"The monster strikes for {monster_attack} damage!",
            "Your health: {player_stats['health']}")
    if player_stats['health'] <= 0:
        print("You have been defeated!")
        return None
    print("You defeated the monster!")
    if has_treasure:
        print("The monster dropped a treasure!")
        return "treasure"
    return None
def handle_path_choice(player_stats):
    """Handles the player's choice of path."""
    print("\nYou stand before two paths: one is well-lit, the other dark and eerie.")
    choice = input("Choose a path (light/dark): ").strip().lower()
    if choice == "dark":
        print("A shadowy figure attacks you!")
        damage = random.randint(5, 15)
        player_stats['health'] -= damage
        print(f"You take {damage} damage. Current health: {player_stats['health']}")
    else:
        print("You walk safely through the path.")
    return player_stats
def display_inventory(inventory):
    """Displays the player's inventory."""
    if inventory:
        print(", ".join(inventory))
    else:
        print("Empty.")
def check_for_treasure(treasure):
    """Checks if the player has obtained a treasure."""
    if treasure:
        print("You obtained a treasure!")
def main():
    """Main game loop."""
    dungeon_rooms = [
        ("Dusty library", "key", "puzzle", 
        ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap", ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle", ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]
    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()
    artifacts = {
        "amulet_of_vitality": {
            "description": "A glowing amulet that enhances your life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "A powerful ring that boosts your attack damage.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "A staff imbued with ancient wisdom.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }
    has_treasure = random.choice([True, False])
    display_player_status(player_stats)
    player_stats = handle_path_choice(player_stats)
    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat is not None:
            check_for_treasure(treasure_obtained_in_combat)
        if random.random() < 0.3:
            artifact_keys = list(artifacts.keys())
            if artifact_keys:
                artifact_name = random.choice(artifact_keys)
                player_stats, artifacts = discover_artifact(player_stats, artifacts,
                artifact_name)
                display_player_status(player_stats)
        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues)
            print("\n--- Game End ---")
            display_player_status(player_stats)
            print("Final Inventory:")
            display_inventory(inventory)
            print("Clues:")
            if clues:
                for clue in clues:
                    print(f"- {clue}")
            else:
                print("No clues.")
if __name__ == "__main__":
    main()
    
