#from tabulate import tabulate

# Blackjack strategy chart (same as before)
bj_strategy = {
    "hard": {
        (17, 21): "Stand",
        (13, 16): {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit",
                   11: "Hit"},
        (12, 12): {2: "Hit", 3: "Hit", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit",
                   11: "Hit"},
        (5, 11): "Hit",
    },
    "soft": {
        (19, 21): "Stand",
        (18, 18): {2: "Stand", 3: "Double", 4: "Double", 5: "Double", 6: "Double", 7: "Stand", 8: "Stand", 9: "Hit",
                   10: "Hit", 11: "Hit"},
        (13, 17): {2: "Hit", 3: "Hit", 4: "Hit", 5: "Double", 6: "Double", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit",
                   11: "Hit"},
    },
    "pairs": {
        11: "Split", 10: "Stand",
        9: {2: "Split", 3: "Split", 4: "Split", 5: "Split", 6: "Split", 7: "Stand", 8: "Split", 9: "Split", 10: "Stand",
            11: "Stand"},
        8: "Split",
        7: {2: "Split", 3: "Split", 4: "Split", 5: "Split", 6: "Split", 7: "Split", 8: "Hit", 9: "Hit", 10: "Hit",
            11: "Hit"},
        6: {2: "Split", 3: "Split", 4: "Split", 5: "Split", 6: "Split", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit",
            11: "Hit"},
        5: "Double",
        4: {2: "Hit", 3: "Hit", 4: "Split", 5: "Split", 6: "Split", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        3: {2: "Split", 3: "Split", 4: "Split", 5: "Split", 6: "Split", 7: "Split", 8: "Hit", 9: "Hit", 10: "Hit",
            11: "Hit"},
        2: {2: "Split", 3: "Split", 4: "Split", 5: "Split", 6: "Split", 7: "Split", 8: "Hit", 9: "Hit", 10: "Hit",
            11: "Hit"},
    }
}

# Hi-Lo Card Counting Values
card_values = {2: +1, 3: +1, 4: +1, 5: +1, 6: +1, 7: 0, 8: 0, 9: 0, 10: -1, 11: -1}
running_count = 0
decks_remaining = 8  # Assume a 6-deck game


def get_best_move(player_cards, dealer_card):
    player_total = sum(player_cards)

    if len(player_cards) == 2 and player_cards[0] == player_cards[1]:  # Check if it's a pair
        pair_value = player_cards[0]
        if pair_value in bj_strategy["pairs"]:
            move = bj_strategy["pairs"][pair_value]
            return move if isinstance(move, str) else move.get(dealer_card, "Hit")

    if 11 in player_cards and player_total <= 21:  # Soft hand check
        soft_value = player_total
        if soft_value in bj_strategy["soft"]:
            move = bj_strategy["soft"][soft_value]
            return move if isinstance(move, str) else move.get(dealer_card, "Hit")

    for (low, high), move in bj_strategy["hard"].items():  # Hard hand strategy
        if low <= player_total <= high:
            return move if isinstance(move, str) else move.get(dealer_card, "Hit")

    return "Hit"


# Function to update the running count
def update_count(cards):
    global running_count
    for card in cards:
        running_count += card_values.get(card, 0)


# Function to calculate True Count
def get_true_count():
    return round(running_count / max(1, decks_remaining), 2)


# Main game loop
while True:
    print("\n🎰 **Blackjack Strategy & Card Counter** 🎰")

    #Get adissional cards
    addisional_cards = list(map(int,input("Enter additional cards: ").split()))
    # Get player and dealer cards
    player_cards = list(map(int, input("Enter your cards (separated by space): ").split()))
    # print(player_cards)
    dealer_card = int(input("Enter dealer's card: "))

    # Update the count
    update_count(player_cards + [dealer_card]+addisional_cards)

    # Get the best move
    best_move = get_best_move(player_cards, dealer_card)

    # Display strategy recommendation
    print(f"\n💡 **Recommended Move:** {best_move.upper()}")
    addisional_cards1 = list(map(int,input("Enter additional cards: ").split()))
    update_count(addisional_cards1)
    # Display running and true count
    print(f"📊 **Running Count:** {running_count}")
    print(f"📈 **True Count:** {get_true_count()}")

    # Betting advice based on True Count
    if get_true_count() > 2:
        print("🔥 **Advice:** The count is high! Increase your bets.")
    elif get_true_count() < -1:
        print("❄️ **Advice:** The count is bad. Lower your bets or sit out.")

    # Ask if the user wants to continue
    # again = input("\nDo you want to check another hand? (y/n): ").strip().lower()
    # if again != 'y':
    #     break
