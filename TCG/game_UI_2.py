import tkinter as tk
from tkinter import ttk
import random


class Card:
    def __init__(self, name, card_type, stats=None, requires_target=False):
        self.name = name
        self.card_type = card_type  # "Monster" or "Spell"
        self.stats = stats if stats else {}  # Monsters have stats, spells may not
        self.requires_target = requires_target  # Only applicable for spells

    def __str__(self):
        if self.card_type == "Monster":
            return f"{self.name} ({self.card_type}) - {self.stats}"
        return f"{self.name} ({self.card_type})"


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.deck = [Card(f"Card {i+1}", "Monster" if random.randint(1, 3)==2 else "Spell", {"Attack": random.randint(1, 5), "Health": random.randint(1, 5)}) for i in range(15)]
        self.frontline = None
        self.backline = []
        self.score = 0

    def draw_card(self):
        if self.deck:
            card = self.deck.pop()
            self.hand.append(card)


class CardGame:
    def __init__(self):
        self.player = Player("Player")
        self.opponent = Player("Opponent")
        self.turn = "Player"  # Tracks whose turn it is

    def play_spell(self, player, card_index, target=None):
        card = player.hand.pop(card_index)
        if card.card_type != "Spell":
            print("Invalid action: Only spells can be played this way.")
            player.hand.append(card)  # Return to hand if invalid
            return

        if card.requires_target and not target:
            print(f"{card.name} requires a target!")
            player.hand.append(card)  # Return to hand if no target provided
        else:
            print(f"Playing {card.name} on {target if target else 'the board'}")
            # Implement spell effects here

    def play_monster(self, player, card_index, to_frontline=False):
        card = player.hand[card_index]
        if card.card_type != "Monster":
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

    def attach_mana(self, card):
        print(f"Attaching mana to {card.name}")

    def attack(self, attacker, target):
        print(f"{attacker.name} attacks {target.name}")

    def ai_turn(self):
        if self.opponent.deck:
            self.opponent.draw_card()
        print("AI played a card!")


class CardGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Game")
        self.game = CardGame()

        for _ in range(5):
            self.game.player.draw_card()
            self.game.opponent.draw_card()

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

        self.details_label = tk.Label(self.root, text="Hover over a card to see details", bd=2, relief="ridge")
        self.details_label.pack(fill="x")

    def create_card_area(self, parent, label_text, num_slots, player=False):
        frame = tk.Frame(parent, bd=1, relief="sunken")
        frame.pack(side="top", fill="x", pady=5)
        tk.Label(frame, text=label_text).pack(anchor="w")
        slots = []
        for _ in range(num_slots):
            card_button = tk.Button(frame, text="Empty", width=10, height=5, bg="white", relief="ridge")
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
        self.opponent_deck_label.config(text=f"Deck: {len(self.game.opponent.deck)}")
        self.score_label.config(text=f"Score: Player {self.game.player.score} - {self.game.opponent.score} Opponent")
        self.player_deck_label.config(text=f"Deck: {len(self.game.player.deck)}")

        for widget in self.player_hand_frame.winfo_children():
            widget.destroy()
        for i, card in enumerate(self.game.player.hand):
            button = tk.Button(self.player_hand_frame, text=str(card), width=10, height=5, bg="lightgray",
                               command=lambda c=i: self.show_card_popup("hand", c))
            button.pack(side="left", padx=5)
            button.bind("<Enter>", self.show_card_details)
            button.bind("<Leave>", self.clear_card_details)

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
            if card.card_type == "Monster":
                actions = ["Play to Backline", "Play to Frontline", "Cancel"]
            elif card.card_type == "Spell":
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
            self.game.attach_mana(self.game.player.backline[index])
        elif choice == "Retreat":
            if area == "frontline":
                self.game.player.hand.append(self.game.player.frontline)
                self.game.player.frontline = None
            elif area == "backline":
                self.game.player.hand.append(self.game.player.backline.pop(index))
        elif choice == "Attack":
            print("Attack logic here.")
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
