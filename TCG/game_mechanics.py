import random

class CardGame:
    def __init__(self):
        num_human_players = self.get_num_human_players()
        self.players = [Player(is_ai=(i >= num_human_players)) for i in range(2)]
        self.current_player_index = 0
        self.current_turn = 1
        self.setup_game()

    def get_num_human_players(self):
        while True:
            try:
                num = int(input("Enter the number of human players (0, 1, or 2): "))
                if num in (0, 1, 2):
                    return num
                else:
                    print("Please enter a valid number (0, 1, or 2).")
            except ValueError:
                print("Invalid input. Please enter a number.")

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
        
        # during player's turn
        if not player.is_ai:
            # Play a spell card (if available and chosen)
            self.prompt_for_card_play(player, "spell")

            # Retreat
            if len(player.backline) > 0:
                retreat = input("Would you like to retreat your frontline monster? (y/n): ").strip().lower() == 'y'
                if retreat:
                    player.retreat_frontline()

            # Play a super monster card (if possible and chosen)
            self.prompt_for_card_play(player, "super_monster")

            # Play a base monster card (if space on board and chosen)
            self.prompt_for_card_play(player, "base_monster")

            # Attach mana
            mana_color = random.choice(list(player.available_colors))
            print(f"generated 1 {mana_color} mana!")
            attach = input("Would you like to attach mana? (y/n): ").strip().lower() == 'y'
            if attach:
                player.attach_mana_to_frontline(mana_color)

            # Attack with frontline monster
            attack = input("Would you like to attack with your frontline monster? (y/n): ").strip().lower() == 'y'
            if attack:
                print(f"Player {self.current_player_index + 1}'s frontline monster attacks!")
                player.attack_with_frontline(opponent)

        else:
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
    
    def prompt_for_card_play(self, player, card_type):
        if card_type == "spell":
            spells = [card for card in player.hand if isinstance(card, SpellCard)]
            if spells:
                print("Available spell cards:")
                for i, card in enumerate(spells):
                    print(f"{i + 1}: {card.name} - Effect: {card.effect}")
                choice = self.get_choice(len(spells))
                if choice is not None:
                    spell = spells[choice]
                    spell.use(player, self.players[1 - self.current_player_index])
                    player.play_spell_card(spell)
        elif card_type == "super_monster":
            super_monsters = [card for card in player.hand if isinstance(card, SuperMonsterCard) and any(backline_card.name == card.sacrifice for backline_card in player.backline)]
            if super_monsters:
                print("Available super monsters:")
                for i, card in enumerate(super_monsters):
                    print(f"{i + 1}: {card.name} - Sacrifice: {card.sacrifice}")
                choice = self.get_choice(len(super_monsters))
                if choice is not None:
                    super_monster = super_monsters[choice]
                    player.play_super_monster(super_monster)
        elif card_type == "base_monster":
            if len(player.backline) < 3:
                base_monsters = [card for card in player.hand if isinstance(card, BaseMonsterCard)]
                if base_monsters:
                    print("Available base monsters:")
                    for i, card in enumerate(base_monsters):
                        print(f"{i + 1}: {card.name}")
                    choice = self.get_choice(len(base_monsters))
                    if choice is not None:
                        base_monster = base_monsters[choice]
                        player.play_base_monster(base_monster)

    def get_choice(self, num_choices):
        while True:
            try:
                choice = int(input(f"Choose a card (1-{num_choices}, or 0 to skip): ")) - 1
                if -1 <= choice < num_choices:
                    return choice if choice != -1 else None
            except ValueError:
                print("Invalid input. Please enter a number.")

class Player:
    def __init__(self, is_ai):
        self.deck = Deck()
        self.hand = []
        self.frontline = None
        self.backline = []
        self.available_colors = self.deck.available_colors  # Use precomputed available colors
        self.score = 0
        self.is_ai = is_ai

        self.can_retreat = True #NEW!
        self.can_play_support = True #NEW!
        self.can_attach_mana = True #NEW!
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

    def choose_spell_card(self):
        spells = [card for card in self.hand if isinstance(card, SpellCard)]
        if spells:
            return spells[0]
        return None

    def play_spell_card(self, spell):
        self.hand.remove(spell)

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
            choice = CardGame.get_choice(None, len(eligible_sacrifices))
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
            choice = CardGame.get_choice(None, len(self.backline))
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
        
        self.can_retreat = True #NEW!
        self.can_play_support = True #NEW!
        self.can_attach_mana = True #NEW!
        self.can_play_base_monster = True #NEW!
        self.can_play_super_monster = True #NEW!
        self.can_play_item = True #NEW!

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
        self.damage_taken = 0 #NEW!
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
        self.defense_bonus = 0 #NEW!
        #self.health_bonus = 0 #NEW!
        #self.damage_taken = 0 #NEW!
        self.mana_bonus = 0 #NEW!
        self.retreat_bonus = 0 #NEW!
        self.score_bonus = 0 #NEW!

        self.can_attack = True #NEW!
        self.can_retreat = True #NEW!
        self.can_be_sacrificed = True #NEW!
        self.can_use_skill = True #NEW!
        self.can_be_hit = True #NEW!

        self.status = 0 #NEW!

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

# Example game loop
game = CardGame()
while game.next_turn():
    pass
