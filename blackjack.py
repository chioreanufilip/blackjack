from tabulate import tabulate
import random
# Blackjack strategy chart (same as before)


class Blackjack :
    cards=[]
    win=0
    card_values = {1: -1, 2: +1, 3: +1, 4: +1, 5: +1, 6: +1, 7: 0, 8: 0, 9: 0, 10: -1, 11: -1}
    running_count = 0
    decks_remaining = 8
    # def __init__(self):
    bj_strategy = {
    "hard": {
        (17, 21): "Stand",
        (13, 16): {2: "Stand", 3: "Stand", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        (12,12): {2: "Hit", 3: "Hit", 4: "Stand", 5: "Stand", 6: "Stand", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
        (5, 11): "Hit",
    },
    "soft": {
        (19, 21): "Stand",
        (18,18): {2: "Stand", 3: "Double", 4: "Double", 5: "Double", 6: "Double", 7: "Stand", 8: "Stand", 9: "Hit", 10: "Hit", 11: "Hit"},
        (13, 17): {2: "Hit", 3: "Hit", 4: "Hit", 5: "Double", 6: "Double", 7: "Hit", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
    },
    "pairs": {
        11: "Split", 10: "Stand",
        9: {2: "Split", 3: "Split", 4: "Split", 5: "Split", 6: "Split", 7: "Stand", 8: "Split", 9: "Split", 10: "Stand", 11: "Stand"},
        8: "Split",
        7: {2: "Split", 3: "Split", 4: "Split", 5: "Split", 6: "Split", 7: "Split", 8: "Hit", 9: "Hit", 10: "Hit", 11: "Hit"},
    }
}

    # Hi-Lo Card Counting Values
    # card_values = {1: -1, 2: +1, 3: +1, 4: +1, 5: +1, 6: +1, 7: 0, 8: 0, 9: 0, 10: -1, 11: -1}
    # running_count = 0
    # decks_remaining = 8
# def getSoftValueTupple(number):
#     for key in bj_strategy["soft"]:


    def get_best_move(self,player_cards, dealer_card):
        player_total = sum(player_cards)
        countAsses = player_cards.count(11)
        if len(player_cards) == 2 and player_cards[0] == player_cards[1]:
            pair_value = player_cards[0]
            if pair_value in self.bj_strategy["pairs"]:
                move = self.bj_strategy["pairs"][pair_value]
                return move if isinstance(move, str) else move.get(dealer_card, "Hit")
        if 11 in player_cards and player_total-(countAsses-1)*10<=21:
            if player_total<=21:
                soft_value = player_total
            elif player_total-(countAsses-1)*10<=21:
                soft_value= player_total-(countAsses-1)*10
            # else:
            #     soft_value = player_total-countAsses*10
            for (low,high),move in self.bj_strategy["soft"].items():
                if low<=soft_value<=high:
                    return move if isinstance(move, str) else move.get(dealer_card, "Hit")
            # if soft_value in bj_strategy["soft"]:
            #     move = bj_strategy["soft"][soft_value]
            #     return move if isinstance(move, str) else move.get(dealer_card, "Hit")
        if 11 in player_cards:
            player_total -= 10 * countAsses
        for (low, high), move in self.bj_strategy["hard"].items():
            # if 11 in player_cards :
            #     player_total-=10*countAsses
                # return "Bust"
            if low <= player_total <= high:
                return move if isinstance(move, str) else move.get(dealer_card, "Hit")
        # return "Bust"
        # if player_cards
        return "Bust"

    def update_count(self,cards):
        # global running_count
        for card in cards:
            self.running_count += self.card_values.get(card, 0)
    # def update_count(self, cards):
    #     for card in cards:
    #         if isinstance(card, list):  # If card is a list, flatten it
    #             for c in card:
    #                 self.running_count += self.card_values.get(c, 0)
    #         else:
    #             self.running_count += self.card_values.get(card, 0)

    def get_true_count(self):
        return round(self.running_count / max(1, self.decks_remaining), 2)

    def checkWin(self,player_cards,dealer_cards):
        # dealer=dealer_cards[0]
        if len(dealer_cards)==1:
            dealer_cards.append(self.cards[0])
            dealer = sum(dealer_cards)
            self.update_count([self.cards[0]])
            self.cards.remove(self.cards[0])
        else: dealer = sum(dealer_cards)
        while dealer < 17:
            dealer += self.cards[0]
            dealer_cards.append(self.cards[0])
            self.update_count([self.cards[0]])
            self.cards.remove(self.cards[0])
            if 11 in dealer_cards and dealer > 21:
                dealer_cards.remove(11)
                dealer -= 10
        sum_player = sum(player_cards)
        if sum_player > 21 and 11 in player_cards:
            sum_player = sum_player - (player_cards.count(11) - 1) * 10
        if dealer > 21 >= sum_player:
            return True
        elif sum_player < 21 and sum_player >= dealer:
            return True
        return False
    def runForTest(self):
        # cards=[]
        self.cards=[]
        for _ in range(8):
            for i in range(2,10):
                for _ in range(4):
                    self.cards.append(i)
            for _ in range(16):
                self.cards.append(10)
            for _ in range(4):
                self.cards.append(11)
        print (len(self.cards))
        random.shuffle(self.cards)
        #10,10,7,10,10,2,7,10,11,7,3,5,10,7,
        # self.cards=[11,7,3,10,7,10,10,2,8,10]
        while len(self.cards)>250:
            player_cards=[]
            player_cards = [self.cards[i] for i in range(2)]
            # print(player_cards)
            dealer_cards = [self.cards[2]]
            # print(dealer_cards)
            for i in player_cards:
                self.cards.remove(i)
            self.cards.remove(dealer_cards[0])
            self.update_count(player_cards+dealer_cards)
            best_move = self.get_best_move(player_cards, *dealer_cards)
            self.bestMoveOperator(player_cards,dealer_cards,best_move)
        print(self.win)

    def bestMoveOperator(self,player_cards,dealer_cards,best_move):
        while best_move == "Hit":
            new_card = self.cards[0]
            self.cards.remove(new_card)
            player_cards.append(new_card)
            self.update_count([new_card])
            best_move = self.get_best_move(player_cards, *dealer_cards)
        if best_move == "Stand":
            if self.checkWin(player_cards, dealer_cards):
                self.win += 1
            else:
                self.win -= 1
            # dealer_cards.append(cards[0])
            # dealer = sum(dealer_cards)
            # cards.remove(cards[0])
            # while dealer<=17:
            #     dealer+=cards[0]
            #     dealer_cards.append(cards[0])
            #     cards.remove(cards[0])
            #     if 11 in dealer_cards and dealer>21:
            #         dealer_cards.remove(11)
            #         dealer-=10
            # sum_player = sum(player_cards)
            # if sum_player>21 and 11 in player_cards:
            #     sum_player = sum_player-(player_cards.count(11)-1)*10
            # if dealer>21:
            #     self.win+=1
            # elif sum_player<21 and sum_player>dealer:
            #     self.win+=1
        if best_move == "Bust":
            self.win -= 1
        if best_move == "Double":
            player_cards.append(self.cards[0])
            self.update_count([self.cards[0]])
            self.cards.remove(self.cards[0])
            if self.checkWin(player_cards, dealer_cards):
                self.win += 1
            else:
                self.win -= 1
        if best_move == "Split":
            player_cards1=[player_cards[0]]
            player_cards2 = [player_cards[1]]
            player_cards1.append(self.cards[0])
            self.update_count([self.cards[0]])
            self.cards.remove(self.cards[0])
            print(dealer_cards)
            dealer_cards1=dealer_cards
            best_move1 = self.get_best_move(player_cards1,*dealer_cards)
            self.bestMoveOperator(player_cards1,dealer_cards,best_move1)
            player_cards2.append(self.cards[0])
            self.update_count([self.cards[0]])
            self.cards.remove(self.cards[0])
            print(dealer_cards)
            best_move2 = self.get_best_move(player_cards2,dealer_cards1[0])
            self.bestMoveOperator(player_cards2,dealer_cards1,best_move2)


    def runWithInput(self):

        while True:
            print("\n🎰 **Blackjack Strategy & Card Counter** 🎰")
            addisional_cards = list(map(int, input("Enter additional cards: ").split()))
            player_cards = list(map(int, input("Enter your cards: ").split()))
            dealer_card = int(input("Enter dealer's card: "))
            self.update_count(player_cards + [dealer_card]+addisional_cards)
            best_move = self.get_best_move(player_cards, dealer_card)
            print(f"\n💡 **Recommended Move:** {best_move.upper()}")
            while best_move == "Hit":
                new_card = int(input("Enter additional card: "))
                player_cards.append(new_card)
                self.update_count([new_card])
                best_move = self.get_best_move(player_cards, dealer_card)
                print(f"\n💡 **New Recommended Move:** {best_move.upper()}")
            addisional_cards1 = list(map(int, input("Enter additional cards: ").split()))
            self.update_count(addisional_cards1)
            print(f"📊 **Running Count:** {self.running_count}")
            print(f"📈 **True Count:** {self.get_true_count()}")
            if self.get_true_count() > 2:
                print("🔥 **Advice:** Increase your bets.")
            elif self.get_true_count() < -1:
                print("❄️ **Advice:** Lower your bets or sit out.")
black =  Blackjack()
black.runForTest()