
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
            self.handle_preflop(game_state)
        else:
            score = self.compute_hand(game_state)
            if (score != 0):
                self.raise_amount = game_state["current_buy_in"] - self.our_player["bet"] + game_state["minimum_raise"] * score
                if (self.raise_amount * score) > (self.our_player['stack']/(8-score)):
                    self.raise_amount = 0 
            else:
                self.raise_amount = 0

        if (self.raise_amount > self.our_player['stack']):
            self.raise_amount = self.our_player['stack']
        
        return self.raise_amount

    def showdown(self, game_state):
        pass

    def handle_preflop(self, game_state):
        
        self.raise_amount = 0
        hole_cards = self.our_player["hole_cards"]
        is_pair = hole_cards[0]["rank"] == hole_cards[1]["rank"]
        is_suite = hole_cards[0]["suit"] == hole_cards[1]["suit"]
        if is_pair:
            # raise
            self.raise_amount = game_state["current_buy_in"] * 2
        elif is_suite:
            self.raise_amount = game_state["current_buy_in"] - self.our_player["bet"]
        else:
            rank1 = self.rank_order[hole_cards[0]["rank"]]
            rank2 = self.rank_order[hole_cards[1]["rank"]]
            if (rank1 + rank2) > 14:
                self.raise_amount = game_state["current_buy_in"] - self.our_player["bet"]
            elif (rank1 + rank2) > 4:
                if game_state["current_buy_in"] > 300:
                    self.raise_amount = 0
                else:
                    self.raise_amount = game_state["current_buy_in"] - self.our_player["bet"]

        
        
        if (self.raise_amount > self.our_player['stack']):
            self.raise_amount = self.our_player['stack']

    def compute_hand(self, game_state):
        all_cards = self.our_player["hole_cards"] + game_state['community_cards']   
        all_cards_ranking = self.convert_to_ranks(all_cards)
        occurances = {}
        suits = {}
        for card in all_cards:
            if card['suit'] in suits.keys():
                suits[card['suit']] += 1
            else:
                suits[card['suit']] = 1
        if 5 in list(suits.values()):
            score = 5
        
        for card in all_cards_ranking:
            if card in occurances.keys():
                occurances[card] += 1
            else:
                occurances[card] = 1
        score = 0
        key_list = list(occurances.keys())
        val_list = list(occurances.values())
        if val_list.count(2) == 1 and self.is_pair_on_our_hand(game_state):
            score = 1
        elif val_list.count(2) == 2 and self.is_pair_on_our_hand(game_state):
            score = 2
        elif val_list.count(3) == 1 and self.is_pair_on_our_hand(game_state):
            score = 3
        elif val_list.count(4) == 1 and self.is_pair_on_our_hand(game_state):
            score = 7
        
        if val_list.count(2) == 1 and val_list.count(3) == 1 and self.is_pair_on_our_hand(game_state):
            score = 6
        
        if self.have_straight(all_cards_ranking):
            score = 4
        return score

    def have_straight(self, all_cards_ranking):
        sorted_rankings = sorted(all_cards_ranking)
        for i in range(1, len(sorted_rankings)):
            if sorted_rankings[i-1] + 1 != sorted_rankings[i]:
                return False
        return True

    def is_pair_on_our_hand(self, game_state):
        hole_cards = self.our_player['hole_cards']
        hole_cards_ranking = self.convert_to_ranks(hole_cards)
        community_ranks = self.convert_to_ranks(game_state['community_cards'])
        return self.is_pair_on_our_hand_impl(hole_cards_ranking, community_ranks)
        
    def convert_to_ranks(self, cards):
        cards_ranking = []
        for card in cards:
            cards_ranking += [self.rank_order[card['rank']]]
        return cards_ranking

    def is_pair_on_our_hand_impl(self, hole_ranking, community_rankings):
        if hole_ranking[0] == hole_ranking[1]:
            return True

        for card in hole_ranking:
            if card in community_rankings:
                return True
        
        return False
            
