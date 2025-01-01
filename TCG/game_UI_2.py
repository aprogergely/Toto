import tkinter as tk
from tkinter import ttk
import random


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

    def __str__(self):
        return f"{self.name} \ncolor: {self.color}\nHP: {self.health}\nATK: {self.attack}\nAtk Cost: {self.attack_cost}\nRetreat: {self.retreat_cost}\nMana: {self.mana_attached}\n"

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
    def __init__(self, name, effect, requires_target=False):
        self.effect = effect
        self.name = name
        self.requires_target = requires_target  # Only applicable for spells

    def __str__(self):
        return f"\n{self.name}\n"

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
        "Draw": {"Effect": "draw", "requires_target": False},
        "Boost": {"Effect": "boost", "requires_target": False},
        "Weaken": {"Effect": "weaken", "requires_target": False},
        "Heal": {"Effect": "heal", "requires_target": True},
        "Switch": {"Effect": "switch", "requires_target": True}
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
            cards.append(SpellCard(name, stats["Effect"], stats["requires_target"]))

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
            print("Choose a monster to sacrifice:")
            for i, (location, monster) in enumerate(eligible_sacrifices):
                print(f"{i + 1}: {monster.name} (Location: {location}, Mana: {monster.mana_attached})")
            choice = self.get_choice(None, len(eligible_sacrifices))
            if choice is None:
                print("No sacrifice made, super monster cannot be played.")
                return
            location, sacrifice = eligible_sacrifices[choice]
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
            input("An invalid mana type was generated!")
            return
        self.frontline.mana_attached[mana_color] += 1
        self.can_attach_mana = False
        print(f"Attached 1 {mana_color} mana to {self.frontline.name}")

    def retreat_frontline(self):
        retreat_status = self.frontline.decrease_mana(self.frontline.retreat_cost)
        if not retreat_status:
            print("Not enough mana to retreat!")
            return
        # If backline has multiple monsters, prompt the player to choose
        if len(self.backline) > 1 and not self.is_ai:
            print("Choose a monster to send out:")
            for i, monster in enumerate(self.backline):
                print(f"{i + 1}: {monster.name} (Mana: {monster.mana_attached})")
            choice = self.get_choice(None, len(self.backline))
            if choice is None:
                print("Chose not to retreat.")
                return
            new_monster = self.backline[choice]
        else:
            new_monster = self.backline[0]
        
        self.frontline.reset_bonuses()
        self.backline.append(self.frontline)
        self.frontline = new_monster
        self.backline.remove(new_monster)
        self.can_retreat = False

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
        effectiveness = CardGame.type_effectiveness(None, self.frontline.color, opponent.frontline.color)
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

    def get_choice(self, num_choices):
        while True:
            try:
                choice = int(input(f"Choose a card (1-{num_choices}, or 0 to skip): ")) - 1
                if -1 <= choice < num_choices:
                    return choice if choice != -1 else None
            except ValueError:
                print("Invalid input. Please enter a number.")


class CardGame:
    def __init__(self):
        self.players = [Player(is_ai=False), Player(is_ai=True)]
        self.player = self.players[0]
        self.opponent = self.players[1]
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

    def play_spell(self, player, card_index, target=None):
        card = player.hand[card_index]
        if not isinstance(card, SpellCard):
            print("Invalid action: Only spells can be played this way.")
            return

        if card.requires_target and not target:
            print(f"{card.name} requires a target!")
        else:
            print(f"Playing {card.name} on {target if target else 'the board'}")
            card.use(player, self.players[1 - self.current_player_index])
            player.play_spell_card(card)
            # Implement spell effects here

    def play_monster(self, player, card_index, to_frontline=False):
        card = player.hand[card_index]
        if not isinstance(card, MonsterCard):
            print("Invalid action: Only monsters can be played this way.")
            return

        player.hand.pop(card_index)
        if to_frontline:
            if player.frontline is None:
                player.frontline = card
            else:
                print("Frontline is occupied!")
                player.hand.append(card)  # Return to hand if invalid
        else:
            if len(player.backline) < 3:
                player.backline.append(card)
            else:
                print("Backline is full!")
                player.hand.append(card)  # Return to hand if invalid

    def attach_mana(self, player, card):
        mana_color = random.choice(list(player.available_colors))
        print(f"generated 1 {mana_color} mana!")
        player.attach_mana_to_frontline(mana_color)

    def attack(self, player, opponent):
        print(f"{player.frontline.name} attacks {opponent.frontline.name}")
        player.attack_with_frontline(opponent)

    def ai_turn(self):
        
        self.opponent.draw_card()
        
        # Play a spell card (if available and chosen)
        spell = self.opponent.choose_spell_card()
        if spell:
            print(f"Player {self.current_player_index + 1} plays spell: {spell.effect}")
            spell.use(self.opponent, self.player)
            self.opponent.play_spell_card(spell)

        # Play a super monster card (if possible and chosen)
        super_monster = self.opponent.choose_super_monster_card()
        if super_monster:
            print(f"Player {self.current_player_index + 1} summons super monster: {super_monster.color} ({super_monster.name})")
            self.opponent.play_super_monster(super_monster)
        
        # Play a base monster card (if space on board and chosen)
        if len(self.opponent.backline) < 3:
            base_monster = self.opponent.choose_base_monster_card()
            if base_monster:
                print(f"Player {self.current_player_index + 1} plays base monster: {base_monster.color} ({base_monster.name})")
                self.opponent.play_base_monster(base_monster)
    
        # Attach mana
        mana_color = random.choice(list(self.opponent.available_colors))
        print(f"generated 1 {mana_color} mana!")
        self.opponent.attach_mana_to_frontline(mana_color)

        # Attack with frontline monster
        print(f"Player {self.current_player_index + 1}'s frontline monster attacks!")
        self.opponent.attack_with_frontline(self.player)

    def type_effectiveness(self, attacker_color, defender_color):
        if attacker_color == "red" and defender_color == "green":
            return 20
        if attacker_color == "green" and defender_color == "blue":
            return 20
        if attacker_color == "blue" and defender_color == "red":
            return 20
        return 0


class CardGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Game")
        self.game = CardGame()

        self.create_layout()
        self.refresh_board_state()

    def create_layout(self):
        opponent_frame = tk.Frame(self.root, bd=2, relief="ridge")
        opponent_frame.pack(side="top", fill="x")
        tk.Label(opponent_frame, text="Opponent").pack(side="left")
        self.opponent_deck_label = tk.Label(opponent_frame, text="Deck: 30")
        self.opponent_deck_label.pack(side="right")
        self.opponent_backline = self.create_card_area(opponent_frame, "Opponent Backline", 3)
        self.opponent_frontline = self.create_card_area(opponent_frame, "Opponent Frontline", 1)

        center_frame = tk.Frame(self.root, bd=2, relief="ridge")
        center_frame.pack(fill="x")
        self.score_label = tk.Label(center_frame, text="Score: Player 0 - 0 Opponent")
        self.score_label.pack(side="left")
        tk.Button(center_frame, text="End Turn", command=self.pass_turn).pack(side="right")

        self.player_frame = tk.Frame(self.root, bd=2, relief="ridge")
        self.player_frame.pack(side="top", fill="x")
        tk.Label(self.player_frame, text="Player").pack(side="left")
        self.player_deck_label = tk.Label(self.player_frame, text="Deck: 30")
        self.player_deck_label.pack(side="right")
        self.player_frontline = self.create_card_area(self.player_frame, "Player Frontline", 1, True)
        self.player_backline = self.create_card_area(self.player_frame, "Player Backline", 3, True)

        hand_frame = tk.Frame(self.root, bd=2, relief="ridge")
        hand_frame.pack(side="bottom", fill="x")
        tk.Label(hand_frame, text="Hand").pack(anchor="w")
        self.player_hand_frame = self.create_hand_area(hand_frame)

        self.details_label = tk.Label(self.root, text="Hover over a card to see details", bd=2, relief="ridge", height=4)
        self.details_label.pack(fill="x")

    def create_card_area(self, parent, label_text, num_slots, player=False):
        frame = tk.Frame(parent, bd=1, relief="sunken")
        frame.pack(side="top", fill="x", pady=5)
        tk.Label(frame, text=label_text).pack(anchor="w")
        slots = []
        for _ in range(num_slots):
            card_button = tk.Button(frame, text="Empty", width=14, height=7, bg="white", relief="ridge")
            card_button.pack(side="left", padx=2)
            card_button.bind("<Enter>", self.show_card_details)
            card_button.bind("<Leave>", self.clear_card_details)
            slots.append(card_button)
        return slots

    def create_hand_area(self, parent):
        canvas = tk.Canvas(parent, height=100)
        scrollbar = ttk.Scrollbar(parent, orient="horizontal", command=canvas.xview)
        scroll_frame = tk.Frame(canvas)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)
        canvas.pack(side="top", fill="x", expand=True)
        scrollbar.pack(side="bottom", fill="x")
        return scroll_frame

    def refresh_board_state(self):
        self.opponent_deck_label.config(text=f"Deck: {len(self.game.opponent.deck.cards)}")
        self.score_label.config(text=f"Score: Player {self.game.player.score} - {self.game.opponent.score} Opponent")
        self.player_deck_label.config(text=f"Deck: {len(self.game.player.deck.cards)}")

        # hand
        for widget in self.player_hand_frame.winfo_children():
            widget.destroy()
        for i, card in enumerate(self.game.player.hand):
            button = tk.Button(self.player_hand_frame, text=str(card), width=14, height=7, bg="lightgray",
                               command=lambda c=i: self.show_card_popup("hand", c))
            button.pack(side="left", padx=5)
            button.bind("<Enter>", self.show_card_details)
            button.bind("<Leave>", self.clear_card_details)

        # player
        for i, card_button in enumerate(self.player_backline):
            if i < len(self.game.player.backline):
                card_button.config(text=str(self.game.player.backline[i]), bg="lightblue",
                                   command=lambda c=i: self.show_card_popup("backline", c))
            else:
                card_button.config(text="Empty", bg="white", command=None)

        if self.game.player.frontline:
            self.player_frontline[0].config(text=str(self.game.player.frontline), bg="lightgreen",
                                            command=lambda: self.show_card_popup("frontline", 0))
        else:
            self.player_frontline[0].config(text="Empty", bg="white", command=None)

        # opponent
        for i, card_button in enumerate(self.opponent_backline):
            if i < len(self.game.opponent.backline):
                card_button.config(text=str(self.game.opponent.backline[i]), bg="lightblue")
            else:
                card_button.config(text="Empty", bg="white", command=None)

        if self.game.opponent.frontline:
            self.opponent_frontline[0].config(text=str(self.game.opponent.frontline), bg="lightgreen")
        else:
            self.opponent_frontline[0].config(text="Empty", bg="white", command=None)

    def show_card_popup(self, area, index):
        if area == "hand":
            card = self.game.player.hand[index]
        elif area == "frontline":
            card = self.game.player.frontline
        elif area == "backline":
            card = self.game.player.backline[index]
        else:
            card = None
        actions = []

        if area == "hand" and card:
            if isinstance(card, BaseMonsterCard):
                actions = ["Play to Backline", "Cancel"]
            elif isinstance(card, SuperMonsterCard):
                actions = ["Play to Backline", "Play to Frontline", "Cancel"]
            elif isinstance(card, SpellCard):
                actions = ["Play Spell", "Cancel"]
        elif area == "frontline" and card:
            actions = ["Attack", "Attach Mana", "Retreat", "Cancel"]
        elif area == "backline" and card:
            actions = ["Attach Mana", "Cancel"]

        choice = self.select_from_list(f"Select an action for {card.name}:", actions)

        if choice == "Play to Backline":
            self.game.play_monster(self.game.player, index)
        elif choice == "Play to Frontline":
            self.game.play_monster(self.game.player, index, to_frontline=True)
        elif choice == "Play Spell":
            if card.requires_target:
                target = self.select_target_popup()
                self.game.play_spell(self.game.player, index, target)
            else:
                self.game.play_spell(self.game.player, index)
        elif choice == "Attach Mana":
            if area == "frontline":
                self.game.attach_mana(self.game.player, self.game.player.frontline)
            if area == "backline":
                self.game.attach_mana(self.game.player, self.game.player.backline[index])
        elif choice == "Retreat":
            selected_index = self.select_new_frontline_popup()
            if selected_index != "Cancel":
                new_frontline = self.game.player.backline[int(selected_index)]
                self.game.player.backline[int(selected_index)] = self.game.player.frontline
                self.game.player.frontline = new_frontline
        elif choice == "Attack":
           self.game.attack(self.game.player, self.game.opponent)
        self.refresh_board_state()

    def select_target_popup(self):
        # Show a popup to let the player choose a target (player or opponent cards)
        popup = tk.Toplevel(self.root)
        popup.title("Select a Target")
        selected_target = tk.StringVar(value="Cancel")

        def on_close():
            selected_target.set("Cancel")
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)

        # Add player's frontline and backline
        tk.Label(popup, text="Player's Monsters:").pack()
        if self.game.player.frontline:
            tk.Radiobutton(popup, text=f"Frontline: {self.game.player.frontline}",
                           variable=selected_target,
                           value="Player Frontline").pack(anchor="w")
        for i, card in enumerate(self.game.player.backline):
            tk.Radiobutton(popup, text=f"Backline {i + 1}: {card}",
                           variable=selected_target,
                           value=f"Player Backline {i + 1}").pack(anchor="w")

        # Add opponent's frontline and backline
        tk.Label(popup, text="Opponent's Monsters:").pack()
        if self.game.opponent.frontline:
            tk.Radiobutton(popup, text=f"Frontline: {self.game.opponent.frontline}",
                           variable=selected_target,
                           value="Opponent Frontline").pack(anchor="w")
        for i, card in enumerate(self.game.opponent.backline):
            tk.Radiobutton(popup, text=f"Backline {i + 1}: {card}",
                           variable=selected_target,
                           value=f"Opponent Backline {i + 1}").pack(anchor="w")

        tk.Button(popup, text="OK", command=popup.destroy).pack()

        popup.grab_set()
        self.root.wait_window(popup)
        return selected_target.get()

    def select_new_frontline_popup(self):
        # Show a popup to let the player choose a target (player or opponent cards)
        popup = tk.Toplevel(self.root)
        popup.title("Select a Target")
        selected_target = tk.StringVar(value="Cancel")

        def on_close():
            selected_target.set("Cancel")
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)

        # Add player's frontline and backline
        tk.Label(popup, text="Player's Monsters:").pack()
        for i, card in enumerate(self.game.player.backline):
            tk.Radiobutton(popup, text=f"Backline {i + 1}: {card}",
                           variable=selected_target,
                           value=i).pack(anchor="w")

        tk.Button(popup, text="OK", command=popup.destroy).pack()

        popup.grab_set()
        self.root.wait_window(popup)
        return selected_target.get()

    def select_from_list(self, title, options):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        selected_action = tk.StringVar(value=options[0])

        def on_close():
            # Ensure "Cancel" is selected if the window is closed without confirmation
            selected_action.set("Cancel")
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)  # Bind the close event to `on_close`

        for option in options:
            tk.Radiobutton(popup, text=option, variable=selected_action, value=option).pack(anchor="w")
        tk.Button(popup, text="OK", command=popup.destroy).pack()

        popup.grab_set()
        self.root.wait_window(popup)
        return selected_action.get()

    def show_card_details(self, event):
        self.details_label.config(text=f"Details: {event.widget.cget('text')}")

    def clear_card_details(self, event):
        self.details_label.config(text="Hover over a card to see details")

    def pass_turn(self):
        self.game.ai_turn()
        self.game.player.draw_card()
        self.refresh_board_state()


if __name__ == "__main__":
    root = tk.Tk()
    app = CardGameUI(root)
    root.mainloop()
