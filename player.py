
class Player:
    VERSION = "0.2"
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
        if (game_state["round"] == 0):
            self.handle_preflop(game_state)
        else:
            if (self.raise_amount != 0):
                self.raise_amount = game_state["current_buy_in"] - self.our_player["bet"]
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
        
                     



