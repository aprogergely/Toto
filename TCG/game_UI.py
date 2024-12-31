import tkinter as tk
from tkinter import ttk
import random

class CardGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Game")
        self.Cardgame = CardGame()

        # Main layout
        self.create_layout()

    def create_layout(self):
        # Top Frame: Opponent's area
        opponent_frame = tk.Frame(self.root, bd=2, relief="ridge")
        opponent_frame.pack(side="top", fill="x")

        tk.Label(opponent_frame, text="Opponent").pack(side="left")
        self.opponent_deck_label = tk.Label(opponent_frame, text="Deck: 30")
        self.opponent_deck_label.pack(side="right")
        self.create_opponent_card_area(opponent_frame, "Opponent Backline", 3)
        self.create_opponent_card_area(opponent_frame, "Opponent Frontline", 1)

        # Center Frame: Game Info
        center_frame = tk.Frame(self.root, bd=2, relief="ridge")
        center_frame.pack(fill="x")
        self.score_label = tk.Label(center_frame, text="Score: Player 0 - 0 Opponent")
        self.score_label.pack(side="left")
        self.end_turn_label = tk.Button(center_frame, text="End Turn", command=lambda: self.pass_turn())
        self.end_turn_label.pack(side="right")

        # Bottom Frame: Player's area
        player_frame = tk.Frame(self.root, bd=2, relief="ridge")
        player_frame.pack(side="top", fill="x")

        tk.Label(player_frame, text="Player").pack(side="left")
        self.player_deck_label = tk.Label(player_frame, text="Deck: 30")
        self.player_deck_label.pack(side="right")
        self.create_frontline_area(player_frame, "Player Frontline")
        self.create_backline_area(player_frame, "Player Backline")

        # Hand Area with Scrollbar
        hand_frame = tk.Frame(self.root, bd=2, relief="ridge")
        hand_frame.pack(side="bottom", fill="x")
        tk.Label(hand_frame, text="Hand").pack(anchor="w")
        self.create_hand_area(hand_frame)

        # Card Details Display
        self.details_label = tk.Label(self.root, text="Hover over a card to see details", bd=2, relief="ridge")
        self.details_label.pack(fill="x")

    def create_opponent_card_area(self, parent, label_text, num_slots):
        frame = tk.Frame(parent, bd=1, relief="sunken")
        frame.pack(side="top", fill="x", pady=5)
        tk.Label(frame, text=label_text).pack(anchor="w")
        for _ in range(num_slots):
            card = tk.Label(frame, text="Empty", width=10, height=5, bg="white", relief="ridge")
            card.pack(side="left", padx=2)
            card.bind("<Enter>", self.show_card_details)
            card.bind("<Leave>", self.clear_card_details)

    def create_frontline_area(self, parent, label_text):
        frame = tk.Frame(parent, bd=1, relief="sunken")
        frame.pack(side="top", fill="x", pady=5)
        tk.Label(frame, text=label_text).pack(anchor="w")
        card = tk.Button(frame, text=f"Frontline Card", width=10, height=5, bg="white", relief="ridge", command=lambda: self.play_card_from_frontline())
        card.pack(side="left", padx=2)
        card.bind("<Enter>", self.show_card_details)
        card.bind("<Leave>", self.clear_card_details)

    def create_backline_area(self, parent, label_text):
        frame = tk.Frame(parent, bd=1, relief="sunken")
        frame.pack(side="top", fill="x", pady=5)
        tk.Label(frame, text=label_text).pack(anchor="w")
        for i in range(3):
            card = tk.Button(frame, text=f"Card {i+1}", width=10, height=5, bg="white", relief="ridge", command=lambda c=i: self.play_card_from_backline(c))
            card.pack(side="left", padx=2)
            card.bind("<Enter>", self.show_card_details)
            card.bind("<Leave>", self.clear_card_details)

    def create_hand_area(self, parent):
        canvas = tk.Canvas(parent, height=100)
        scrollbar = ttk.Scrollbar(parent, orient="horizontal", command=canvas.xview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)

        canvas.pack(side="top", fill="x", expand=True)
        scrollbar.pack(side="bottom", fill="x")

        for i in range(10):  # Example: Add 10 card placeholders
            card = tk.Button(scroll_frame, text=f"Card {i+1}", width=10, height=5, bg="lightgray", relief="ridge", command=lambda c=i: self.play_card_from_hand(c)) ####### NEW!
            card.pack(side="left", padx=5)
            card.bind("<Enter>", self.show_card_details)
            card.bind("<Leave>", self.clear_card_details)

    def show_card_details(self, event):
        # Show detailed stats of the card
        self.details_label.config(text=f"Details: {event.widget.cget('text')}")

    def clear_card_details(self, event):
        # Clear the details when the mouse leaves the card
        self.details_label.config(text="Hover over a card to see details")

    def play_card_from_hand(self, card_index):
        print(f"Card {card_index+1} selected! Show options.")
        # Implement action logic here
        self.Cardgame.play_card_from_hand(card_name) ####### NEW!
        self.refresh_board_state() ####### NEW!

    def play_card_from_frontline(self):
        print(f"Frontline selected! Show options.")
        options = ["attach mana", "attack", "retreat", "cancel"]
        options.show
        case selected_option:
            0:
                self.Cardgame.attach_mana(card_name)
                self.refresh_board_state()
            1:
                self.Cardgame.attack()
                self.refresh_board_state()
            2:
                self.Cardgame.retreat()
                self.refresh_board_state()
        return

    def play_card_from_backline(self, card_index):
        print(f"Card {card_index+1} selected! Show options.")
        options = ["attach mana", "cancel"]
        options.show
        if selected_option == 0:
            self.Cardgame.attach_mana(card_name)
            self.refresh_board_state()
        return

    def pass_turn(self):
        print(f"Next player's turn.")
        self.Cardgame.AI_turn()
        self.refresh_board_state()

    
class CardGame:
    def __init__(self):
        self.players = [Player(is_ai=True), Player(is_ai=False)]
        self.current_player_index = 0
        self.current_turn = 1
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

    def AI_turn(self):
        player = self.players[self.current_player_index]
        opponent = self.players[1 - self.current_player_index]
        print(f"\nTurn {self.current_turn}!")
        print(f"Player {self.current_player_index + 1}'s turn")

        # Display board state and hands
        print("\n--- Board State ---")
        print(f"Player 1 Frontline: {self.players[0].frontline.name}, Backline: {[card.name for card in self.players[0].backline]}")
        print(f"Player 2 Frontline: {self.players[1].frontline.name}, Backline: {[card.name for card in self.players[1].backline]}")
        print(f"Player 1 Mana: {self.players[0].frontline.mana_attached}, Backline: {[card.mana_attached for card in self.players[0].backline]}")
        print(f"Player 2 Mana: {self.players[1].frontline.mana_attached}, Backline: {[card.mana_attached for card in self.players[1].backline]}")

        # Draw a card
        player.draw_card()

        print("\n--- Hands ---")
        print(f"Player 1 Hand: {[card.name for card in self.players[0].hand]}")
        print(f"Player 2 Hand: {[card.name for card in self.players[1].hand]}")

        # Play a spell card (if available and chosen)
        spell = player.choose_spell_card()
        if spell:
            print(f"Player {self.current_player_index + 1} plays spell: {spell.effect}")
            spell.use(player, opponent)
            player.play_spell_card(spell)

        # Play a super monster card (if possible and chosen)
        super_monster = player.choose_super_monster_card()
        if super_monster:
            print(f"Player {self.current_player_index + 1} summons super monster: {super_monster.color} ({super_monster.name})")
            player.play_super_monster(super_monster)
        
        # Play a base monster card (if space on board and chosen)
        if len(player.backline) < 3:
            base_monster = player.choose_base_monster_card()
            if base_monster:
                print(f"Player {self.current_player_index + 1} plays base monster: {base_monster.color} ({base_monster.name})")
                player.play_base_monster(base_monster)
    
        # Attach mana
        mana_color = random.choice(list(player.available_colors))
        print(f"generated 1 {mana_color} mana!")
        player.attach_mana_to_frontline(mana_color)

        # Attack with frontline monster
        print(f"Player {self.current_player_index + 1}'s frontline monster attacks!")
        player.attack_with_frontline(opponent)

        # inbetween turns
        # Check for game over
        if player.score > 2:
            print(f"Player {self.current_player_index + 1} wins due to reaching 3 points!")
            return False

        if not opponent.frontline and not opponent.backline:
            print(f"Player {self.current_player_index + 1} wins due to opponent having no monster left!")
            return False

        # Reset attack bonuses
        player.reset_bonuses()

        # End turn
        self.current_player_index = 1 - self.current_player_index
        self.current_turn += 1
        return True

    def play_card_from_hand(self, player, card):
        if isinstance(card, SpellCard):
            if player.can_play_card(card, "spell"):
                card.use(player, self.players[1 - self.current_player_index])
                player.play_spell_card(card)
            else:
                print("Cannot play this card right now!")
        elif isinstance(card, SuperMonsterCard):
            if player.can_play_card(card, "super_monster"):
                player.play_super_monster(card)
            else:
                print("Cannot play this card right now!")
        elif isinstance(card, BaseMonsterCard):
            if player.can_play_card(card, "base_monster"):
                player.play_base_monster(card)
            else:
                print("Cannot play this card right now!")


class Player:
    def __init__(self, is_ai):
        self.deck = Deck()
        self.hand = []
        self.frontline = None
        self.backline = []
        self.available_colors = self.deck.available_colors  # Use precomputed available colors
        self.score = 0
        self.is_ai = is_ai

        self.can_retreat = True
        self.can_play_support = True #NEW!
        self.can_attach_mana = True
        self.can_play_base_monster = True #NEW!
        self.can_play_super_monster = True #NEW!
        self.can_play_item = True #NEW!

    def generate_initial_hand(self):
        for _ in range(5):
            self.draw_card()

    def draw_card(self):
        card = self.deck.draw()
        if card:
            self.hand.append(card)
            print(f"Drew card: {card.name}")

    def cards_in_hand(self, card_type):
        if card_type == "spell":
            spells = [card for card in self.hand if isinstance(card, SpellCard)]
            if spells:
                return spells
        elif card_type == "base_monster":
            base_monsters = [card for card in self.hand if isinstance(card, BaseMonsterCard)]
            if base_monsters:
                return base_monsters
        elif card_type == "super_monster":
            super_monsters = [card for card in self.hand if isinstance(card, SuperMonsterCard)]
            if super_monsters:
                return super_monsters
        elif card_type == "any":
            return self.hand
        return None

    def choose_spell_card(self):
        spells = [card for card in self.hand if isinstance(card, SpellCard)]
        if spells:
            return spells[0]
        return None

    def play_spell_card(self, spell):
        self.hand.remove(spell)
        self.can_play_support = False

    def choose_super_monster_card(self):
        super_monsters = [card for card in self.hand if isinstance(card, SuperMonsterCard)]
        for card in super_monsters:
            # Check if a card in the backline matches the sacrifice name
            if any(backline_card.name == card.sacrifice for backline_card in self.backline) or self.frontline.name == card.sacrifice:
                return card
        return None

    def play_super_monster(self, super_monster):
        # Find all eligible sacrifices
        eligible_sacrifices = []
        if self.frontline and self.frontline.name == super_monster.sacrifice:
            eligible_sacrifices.append(('frontline', self.frontline))
        eligible_sacrifices.extend(
            ('backline', card) for card in self.backline if card.name == super_monster.sacrifice
        )

        # If multiple sacrifices are possible, prompt the player to choose
        if len(eligible_sacrifices) > 1 and not self.is_ai:
            location, sacrifice = eligible_sacrifices[0]
        else:
            location, sacrifice = eligible_sacrifices[0]

        # Store mana from the sacrificed monster
        current_mana = sacrifice.mana_attached.copy()
        damage_taken = sacrifice.damage_taken

        # Remove the sacrificed monster from its location
        if location == 'frontline':
            self.frontline = None
        elif location == 'backline':
            self.backline.remove(sacrifice)

        # Remove the super monster card from the hand and play it
        self.hand.remove(super_monster)
        if not self.frontline:
            self.frontline = super_monster
        else:
            self.backline.append(super_monster)

        # Inherit mana from the sacrificed monster
        super_monster.mana_attached = current_mana
        super_monster.damage_taken = damage_taken
        print(f"{super_monster.name} is summoned, inheriting mana: {current_mana}")

    def choose_base_monster_card(self):
        base_monsters = [card for card in self.hand if isinstance(card, BaseMonsterCard)]
        if base_monsters:
            return base_monsters[0]
        return None

    def play_base_monster(self, base_monster):
        if base_monster in self.hand:
            self.hand.remove(base_monster)
        if not self.frontline:
            self.frontline = base_monster
        else:
            self.backline.append(base_monster)

    def attach_mana_to_frontline(self, mana_color):
        if mana_color not in self.frontline.mana_attached:
            print("An invalid mana type was generated!")
            return
        self.frontline.mana_attached[mana_color] += 1
        self.can_attach_mana = False
        print(f"Attached 1 {mana_color} mana to {self.frontline.name}")

    def attack_with_frontline(self, opponent):
        if not opponent.frontline:
            print("Opponent has no frontline!")
            return
        attack_cost = self.frontline.attack_cost
        cost_color = self.frontline.color
        if self.frontline.mana_attached[cost_color] < attack_cost:
            print(f"Insufficient mana: {self.frontline.mana_attached}")
            return
        damage = self.frontline.attack
        damage += self.frontline.attack_bonus
        effectiveness = type_effectiveness(self.frontline.color, opponent.frontline.color)
        damage += effectiveness if damage > 0 else 0
        opponent.frontline.damage_taken += damage
        print(f"{self.frontline.name} dealt {damage} damage to opponent's {opponent.frontline.name}")
        if opponent.frontline.health <= opponent.frontline.damage_taken:
            print("Opponent's frontline knocked out!")
            self.score += 1
            opponent.promote_backline()

    def reset_bonuses(self):
        self.frontline.reset_bonuses()
        for card in self.backline:
            card.reset_bonuses()

        self.can_retreat = True
        self.can_play_support = True
        self.can_attach_mana = True
        self.can_play_base_monster = True
        self.can_play_super_monster = True
        self.can_play_item = True

    def promote_backline(self):
        if self.backline:
            self.frontline = self.backline.pop(0)
            print(f'Sent out {self.frontline.name}!')
        else:
            self.frontline = None

class Deck:
    def __init__(self):
        self.cards = self.generate_deck()
        self.available_colors = self.calculate_available_colors()

    def generate_deck(self):
        # Card data
        card_data = {
            "Goblin": {"Color": "green", "Health": 50, "Attack": 20, "Attack_Cost": 1, "retreat_cost": 1, "Sacrifice": None},
            "Goblin King": {"Color": "green", "Health": 100, "Attack": 50, "Attack_Cost": 3, "retreat_cost": 3, "Sacrifice": "Goblin"},
            "Dryad": {"Color": "green", "Health": 80, "Attack": 20, "Attack_Cost": 2, "retreat_cost": 1, "Sacrifice": None},
            "Unicorn": {"Color": "green", "Health": 60, "Attack": 30, "Attack_Cost": 2, "retreat_cost": 1, "Sacrifice": None},
            "Mermaid": {"Color": "blue", "Health": 60, "Attack": 20, "Attack_Cost": 2, "retreat_cost": 1, "Sacrifice": None},
            "Neptune": {"Color": "blue", "Health": 80, "Attack": 50, "Attack_Cost": 2, "retreat_cost": 2, "Sacrifice": "Mermaid"},
            "Shark": {"Color": "blue", "Health": 50, "Attack": 40, "Attack_Cost": 2, "retreat_cost": 1, "Sacrifice": None},
            "Lizard": {"Color": "red", "Health": 40, "Attack": 20, "Attack_Cost": 2, "retreat_cost": 1, "Sacrifice": None},
            "Dragon": {"Color": "red", "Health": 70, "Attack": 60, "Attack_Cost": 2, "retreat_cost": 2, "Sacrifice": "Lizard"},
            "Lizardman": {"Color": "red", "Health": 80, "Attack": 40, "Attack_Cost": 1, "retreat_cost": 1, "Sacrifice": "Lizard"},
            "Phoenix": {"Color": "red", "Health": 100, "Attack": 20, "Attack_Cost": 2, "retreat_cost": 2, "Sacrifice": None}
        }

        spell_data = {
        "Draw": {"Effect": "draw"},
        "Boost": {"Effect": "boost"},
        "Weaken": {"Effect": "weaken"},
        "Heal": {"Effect": "heal"},
        "Switch": {"Effect": "switch"}
        }

        # Generate the deck
        has_base_monster = False
        while not has_base_monster:
            cards = []
            for _ in range(15):  # Add 15 monster cards at random
                name, stats = random.choice(list(card_data.items()))
                if stats["Sacrifice"]:
                    cards.append(SuperMonsterCard(name, stats["Color"], stats["Health"], stats["Attack"], stats["Attack_Cost"], stats["retreat_cost"], stats["Sacrifice"]))
                else:
                    cards.append(BaseMonsterCard(name, stats["Color"], stats["Health"], stats["Attack"], stats["Attack_Cost"], stats["retreat_cost"]))
                    has_base_monster = True

        # Generate spell cards
        for _ in range(5):  # Add 5 spell cards at random
            name, stats = random.choice(list(spell_data.items()))
            cards.append(SpellCard(stats["Effect"], name))

        random.shuffle(cards)
        return cards

    def calculate_available_colors(self):
        return {card.color.lower() for card in self.cards if isinstance(card, MonsterCard)}

    def draw(self):
        return self.cards.pop() if self.cards else None

    def get_random_base_monster(self):
        base_monsters = [card for card in self.cards if isinstance(card, BaseMonsterCard)]
        if base_monsters:
            monster = random.choice(base_monsters)
            self.cards.remove(monster)
            return monster
        return None

class MonsterCard:
    def __init__(self, name, color, health, attack, attack_cost, retreat_cost):
        self.name = name
        self.color = color
        self.health = health
        self.attack = attack
        self.attack_cost = attack_cost
        self.retreat_cost = retreat_cost
        self.mana_attached = {"red": 0, "green": 0, "blue": 0}
        self.attack_bonus = 0
        self.defense_bonus = 0 #NEW!
        self.health_bonus = 0 #NEW!
        self.damage_taken = 0
        self.mana_bonus = 0 #NEW!
        self.retreat_bonus = 0 #NEW!
        self.score_bonus = 0 #NEW!

        self.can_attack = True #NEW!
        self.can_retreat = True #NEW!
        self.can_be_sacrificed = True #NEW!
        self.can_use_skill = True #NEW!
        self.can_be_hit = True #NEW!

        self.status = 0 #NEW!

    def decrease_mana(self, cost):
        total_mana = 0
        for color in self.mana_attached:
            total_mana += self.mana_attached[color]
        
        # action cannot be performed due to insufficient mana
        if total_mana < cost:
            return False
        
        # throw away unneeded mana first
        for color in self.mana_attached:
            if color != self.color:
                decrease_by = min(self.mana_attached[color], cost)
                self.mana_attached[color] -= decrease_by
                cost -= decrease_by
                print(f"lost {decrease_by} {color} mana while retreating!")

        # throw away same color mana if needed
        color = self.color
        decrease_by = min(self.mana_attached[color], cost)
        self.mana_attached[color] -= decrease_by
        cost -= decrease_by
        print(f"lost {decrease_by} {color} mana while retreating!")
        return True


    def reset_bonuses(self):
        self.attack_bonus = 0
        self.defense_bonus = 0
        self.mana_bonus = 0
        self.retreat_bonus = 0
        self.score_bonus = 0

        self.can_attack = True
        self.can_retreat = True
        self.can_be_sacrificed = True
        self.can_use_skill = True
        self.can_be_hit = True

        self.status = 0

class BaseMonsterCard(MonsterCard):
    def __init__(self, name, color, health, attack, attack_cost, retreat_cost):
        super().__init__(name, color, health, attack, attack_cost, retreat_cost)

class SuperMonsterCard(MonsterCard):
    def __init__(self, name, color, health, attack, attack_cost, retreat_cost, sacrifice):
        super().__init__(name, color, health, attack, attack_cost, retreat_cost)
        self.sacrifice = sacrifice
        self.can_summon = False

    def summon_check(self):
        return self.can_summon

class SpellCard:
    def __init__(self, effect,name):
        self.effect = effect
        self.name = name

    def use(self, player, opponent):
        print(f"Spell effect: {self.effect}")
        if self.effect == "draw":
            player.draw_card()
        elif self.effect == "boost" and player.frontline:
            player.frontline.attack_bonus += 10
            print(f"{player.frontline.name} attack increased by 10!")
        elif self.effect == "weaken" and opponent.frontline:
            opponent.frontline.attack_bonus -= 10
            print(f"{opponent.frontline.name} attack reduced by 10!")
        elif self.effect == "heal" and player.frontline:
            player.frontline.damage_taken = max(player.frontline.damage_taken - 20, 0)
            print(f"{player.frontline.name} healed by 20!")
        elif self.effect == "switch" and opponent.backline:
            idx = random.randint(0, len(opponent.backline) - 1)
            opponent.frontline, opponent.backline[idx] = opponent.backline[idx], opponent.frontline
            print("Opponent's frontline and backline switched!")

def type_effectiveness(attacker_color, defender_color):
    if attacker_color == "red" and defender_color == "green":
        return 20
    if attacker_color == "green" and defender_color == "blue":
        return 20
    if attacker_color == "blue" and defender_color == "red":
        return 20
    return 0

# Initialize and run the UI
root = tk.Tk()
game_ui = CardGameUI(root)
root.mainloop()
