
from typing import Counter


class Player:
    VERSION = "0.3"
    rank_order = {
        "2":2,
        "3":3,
        "4":4,
        "5":5,
        '6':6,
        '7':7,
        '8':8,
        '9':9,
        '10':10,
        'J':11,
        'Q':12,
        'K':13,
        'A':14
    }

    def betRequest(self, game_state):
        self.our_player = game_state["players"][game_state["in_action"]]
        self.compute_hand(game_state)
        if (game_state["round"] == 0):
            # test edit from Jan!
            self.handle_preflop(game_state)
        else:
            score = self.compute_hand(game_state)
            if (score != 0):
                self.raise_amount = game_state["current_buy_in"] - self.our_player["bet"] + game_state["minimum_raise"]
            else:
                self.raise_amount = 0

        return self.raise_amount

    def showdown(self, game_state):
        pass

    def handle_preflop(self, game_state):
        
        self.raise_amount = 0
        hole_cards = self.our_player["hole_cards"]
        is_pair = hole_cards[0]["rank"] == hole_cards[1]["rank"]
        if is_pair:
            # raise
            self.raise_amount = game_state["current_buy_in"] * 2
        else:
            rank1 = self.rank_order[hole_cards[0]["rank"]]
            rank2 = self.rank_order[hole_cards[1]["rank"]]
            if (rank1 + rank2) > 14:
                self.raise_amount = game_state["current_buy_in"] - self.our_player["bet"]
        
        
        if (self.raise_amount > self.our_player['stack']):
            self.raise_amount = self.our_player['stack']

    def compute_hand(self, game_state):
        all_cards = self.our_player["hole_cards"] + game_state['community_cards']    
        all_cards_ranking = []
        for card in all_cards:
            all_cards_ranking += [self.rank_order[card['rank']]]
        occurances = {}
        for card in all_cards_ranking:
            if card in occurances.keys():
                occurances[card] += 1
            else:
                occurances[card] = 1
        score = 0;
        key_list = list(occurances.keys())
        val_list = list(occurances.values())
        if val_list.count(2) == 1:
            score = 1
        elif val_list.count(2) == 2:
            score = 2
        elif val_list.count(3) == 1:
            score = 3
        elif val_list.count(4) == 1:
            score = 4
        return score

        
        
                  



