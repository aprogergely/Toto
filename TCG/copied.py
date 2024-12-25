import random

class CardGame:
    def __init__(self):
        self.players = [Player(), Player()]
        self.current_player_index = 0
        self.setup_game()

    def setup_game(self):
        # Both players draw initial hand of 5 cards
        for player in self.players:
            player.generate_initial_hand()

        # Both players place a random base monster into their frontline spot
        for player in self.players:
            base_monster = player.deck.get_random_base_monster()
            if base_monster:
                player.play_base_monster(base_monster)
            else:
                print("Player does not have a base monster to place in frontline!")

    def next_turn(self):
        player = self.players[self.current_player_index]
        opponent = self.players[1 - self.current_player_index]
        print(f"\nPlayer {self.current_player_index + 1}'s turn")

        # Display board state and hands
        print("\n--- Board State ---")
        print(f"Player 1 Frontline: {self.players[0].frontline.name}, Backline: {[card.name for card in self.players[0].backline]}")
        print(f"Player 2 Frontline: {self.players[1].frontline.name}, Backline: {[card.name for card in self.players[1].backline]}")
        print("\n--- Hands ---")
        print(f"Player 1 Hand: {[card.name for card in self.players[0].hand]}")
        print(f"Player 2 Hand: {[card.name for card in self.players[1].hand]}")

        # Draw a card
        player.draw_card()
        
        # Play a spell card (if available and chosen)
        spell = player.choose_spell_card()
        if spell:
            print(f"Player {self.current_player_index + 1} plays spell: {spell.effect}")
            spell.use(player, opponent)
        
        # Play a super monster card (if possible and chosen)
        super_monster = player.choose_super_monster_card()
        if super_monster:
            print(f"Player {self.current_player_index + 1} summons super monster: {super_monster.color} ({super_monster.name})")
            player.play_super_monster(super_monster)
        
        # Play a base monster card (if space on board and chosen)
        base_monster = player.choose_base_monster_card()
        if base_monster:
            print(f"Player {self.current_player_index + 1} plays base monster: {base_monster.color} ({base_monster.name})")
            player.play_base_monster(base_monster)
        
        # Attach mana
        player.attach_mana()
        
        # Attack with frontline monster
        if player.frontline:
            print(f"Player {self.current_player_index + 1}'s frontline monster attacks!")
            player.attack_with_frontline(opponent)

        # Check for game over
        if not opponent.frontline and not opponent.backline:
            print(f"Player {self.current_player_index + 1} wins!")
            return False

        # End turn
        self.current_player_index = 1 - self.current_player_index
        return True

class Player:
    def __init__(self):
        self.deck = Deck()
        self.hand = []
        self.frontline = None
        self.backline = []
        self.mana_pool = {"red": 0, "green": 0, "blue": 0}
        self.available_colors = self.deck.available_colors  # Use precomputed available colors

    def generate_initial_hand(self):
        for _ in range(5):
            self.draw_card()

    def draw_card(self):
        card = self.deck.draw()
        if card:
            self.hand.append(card)
            print(f"Drew card: {card.name}")

    def choose_spell_card(self):
        spells = [card for card in self.hand if isinstance(card, SpellCard)]
        if spells:
            return spells[0]  # Placeholder for player choice
        return None

    def choose_super_monster_card(self):
        super_monsters = [card for card in self.hand if isinstance(card, SuperMonsterCard)]
        for card in super_monsters:
            if card.sacrifice in self.backline:
                return card  # Placeholder for player choice
        return None

    def play_super_monster(self, super_monster):
        self.backline.remove(super_monster.sacrifice)
        self.hand.remove(super_monster)
        if not self.frontline:
            self.frontline = super_monster
        else:
            self.backline.append(super_monster)

    def choose_base_monster_card(self):
        base_monsters = [card for card in self.hand if isinstance(card, BaseMonsterCard)]
        if base_monsters and len(self.backline) < 3:
            return base_monsters[0]  # Placeholder for player choice
        return None

    def play_base_monster(self, base_monster):
        if base_monster in self.hand:
            self.hand.remove(base_monster)
        if not self.frontline:
            self.frontline = base_monster
        else:
            self.backline.append(base_monster)

    def attach_mana(self):
        if not self.available_colors:
            print("No colors available for mana generation!")
            return
        mana_color = random.choice(list(self.available_colors))
        self.mana_pool[mana_color] += 1
        print(f"Generated 1 {mana_color} mana")

    def attack_with_frontline(self, opponent):
        if not opponent.frontline:
            print("Opponent has no frontline. Attack directly!")
            return
        damage = self.frontline.attack
        effectiveness = type_effectiveness(self.frontline.color, opponent.frontline.color)
        damage += effectiveness
        opponent.frontline.health -= damage
        print(f"Dealt {damage} damage to opponent's frontline")
        if opponent.frontline.health <= 0:
            print("Opponent's frontline knocked out!")
            opponent.promote_backline()

    def promote_backline(self):
        if self.backline:
            self.frontline = self.backline.pop(0)
        else:
            self.frontline = None

class Deck:
    def __init__(self):
        self.cards = self.generate_deck()
        self.available_colors = self.calculate_available_colors()

    def generate_deck(self):
        # Card data
        card_data = {
            "Goblin": {"Color": "green", "Health": 50, "Attack": 20, "Attack_Cost": 1, "Sacrifice": None},
            "Goblin King": {"Color": "green", "Health": 100, "Attack": 50, "Attack_Cost": 3, "Sacrifice": "Goblin"},
            "Dryad": {"Color": "green", "Health": 80, "Attack": 20, "Attack_Cost": 2, "Sacrifice": None},
            "Unicorn": {"Color": "green", "Health": 60, "Attack": 30, "Attack_Cost": 2, "Sacrifice": None},
            "Mermaid": {"Color": "blue", "Health": 60, "Attack": 20, "Attack_Cost": 2, "Sacrifice": None},
            "Neptune": {"Color": "blue", "Health": 80, "Attack": 50, "Attack_Cost": 2, "Sacrifice": "Mermaid"},
            "Shark": {"Color": "blue", "Health": 50, "Attack": 40, "Attack_Cost": 2, "Sacrifice": None},
            "Lizard": {"Color": "red", "Health": 40, "Attack": 20, "Attack_Cost": 2, "Sacrifice": None},
            "Dragon": {"Color": "red", "Health": 70, "Attack": 60, "Attack_Cost": 2, "Sacrifice": "Lizard"},
            "Lizardman": {"Color": "red", "Health": 80, "Attack": 40, "Attack_Cost": 1, "Sacrifice": "Lizard"},
            "Phoenix": {"Color": "red", "Health": 100, "Attack": 20, "Attack_Cost": 2, "Sacrifice": None}
        }
        # Generate the deck
        cards = []
        for name, stats in card_data.items():
            if stats["Sacrifice"]:
                cards.append(SuperMonsterCard(name, stats["Color"], stats["Health"], stats["Attack"], stats["Attack_Cost"], stats["Sacrifice"]))
            else:
                cards.append(BaseMonsterCard(name, stats["Color"], stats["Health"], stats["Attack"], stats["Attack_Cost"]))
        random.shuffle(cards)
        return cards

    def calculate_available_colors(self):
        return {card.color.lower() for card in self.cards if isinstance(card, (BaseMonsterCard, SuperMonsterCard))}

    def draw(self):
        return self.cards.pop() if self.cards else None

    def has_monsters_of_color(self, color):
        return any(isinstance(card, BaseMonsterCard) and card.color.lower() == color.lower() for card in self.cards)

    def get_random_base_monster(self):
        base_monsters = [card for card in self.cards if isinstance(card, BaseMonsterCard)]
        if base_monsters:
            monster = random.choice(base_monsters)
            self.cards.remove(monster)
            return monster
        return None

class BaseMonsterCard:
    def __init__(self, name, color, health, attack, attack_cost):
        self.name = name
        self.color = color
        self.health = health
        self.attack = attack
        self.attack_cost = attack_cost

class SuperMonsterCard(BaseMonsterCard):
    def __init__(self, name, color, health, attack, attack_cost, sacrifice):
        super().__init__(name, color, health, attack, attack_cost)
        self.sacrifice = sacrifice

class SpellCard:
    def __init__(self, effect):
        self.effect = effect

    def use(self, player, opponent):
        if self.effect == "draw":
            player.draw_card()
        elif self.effect == "boost":
            if player.frontline:
                player.frontline.attack += 10
        elif self.effect == "weaken":
            if opponent.frontline:
                opponent.frontline.attack -= 10
        elif self.effect == "heal":
            if player.frontline:
                player.frontline.health += 20
        elif self.effect == "switch":
            if opponent.backline:
                opponent.frontline, opponent.backline[random.randint(0, len(opponent.backline) - 1)] = \
                    opponent.backline[random.randint(0, len(opponent.backline) - 1)], opponent.frontline


def type_effectiveness(attacker_color, defender_color):
    if attacker_color == "red" and defender_color == "green":
        return 20
    if attacker_color == "green" and defender_color == "blue":
        return 20
    if attacker_color == "blue" and defender_color == "red":
        return 20
    if defender_color == "red" and attacker_color == "green":
        return -20
    if defender_color == "green" and attacker_color == "blue":
        return -20
    if defender_color == "blue" and attacker_color == "red":
        return -20
    return 0

# Example game loop
game = CardGame()
while game.next_turn():
    pass
