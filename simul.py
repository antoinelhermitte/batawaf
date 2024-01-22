import random
    
NB_PLAYERS = 4
NB_TRIES = 10000
VERBOSE = True

class Game():
    
    cards: dict
    status: str
    winner: int
    nb_players: int
    verbose: bool
    MAX_HANDS = 10000


    def shuffle_deal(nb_players):
            elements = [i for i in range(1, 7) for _ in range(6)]

            if len(elements) % nb_players!= 0:
                raise ValueError("List cannot be divided into {} equal parts".format(nb_players))
            
            random.shuffle(elements)
            sublist_size = len(elements) // nb_players
            return {i:elements[i:i + sublist_size] for i in range(0, nb_players)}


    def __init__(self, nb_players, init_state=False, verbose=True):
        self.status = 'playing'
        self.nb_players = nb_players
        self.verbose = verbose
        if init_state:
            self.cards = init_state
        else:
            self.cards = Game.shuffle_deal(nb_players)
        self.winner = None


    def __str__(self):
        s = f'{self.nb_players} players in game - {self.status}\n'
        for k,v in self.cards.items():
            s += f'Player {k} cards: {v}\n'
        return s
    

    def keys_of_max_values(hand):
        max_indexes = []
        if hand.values():
            max_value = max(hand.values())
            max_indexes = [k for k, v in hand.items() if v == max_value]
        return max_indexes
    

    def get_round_remaining_players(self):
        return [k for k,v in self.cards.items() if v]


    def play_hand(self):
        # at the beginning of the hand we assume all players should have at least 1 card in their stack
        rrp = self.get_round_remaining_players()
        test_cards = {k: self.cards[k][0] for k in rrp}
        trick_cards = [self.cards[k].pop(0) for k in rrp]
        
        hand_remaining_players = Game.keys_of_max_values(test_cards)

        # case when at least 2 cards of the hand have the same value
        while len(hand_remaining_players) > 1:
            
            # test that there's enough cards in decks before doing this
            for k in hand_remaining_players:
                if self.cards[k]:
                    trick_cards.append(self.cards[k].pop(0))

            # test that there's enough cards in decks
            test_cards = {}
            for k in hand_remaining_players:
                if self.cards[k]:
                    test_cards[k] = self.cards[k].pop(0)
            
            trick_cards.extend(list(test_cards.values()))
            hand_remaining_players = Game.keys_of_max_values(test_cards)
        
        rrp = self.get_round_remaining_players()
        print(rrp)
        print(hand_remaining_players)
        if len(rrp) == 0 and len(test_cards) == 0:
            self.status = 'finished'
            self.winner = -1
            if self.verbose:
                print(f'==== Game ended in a draw ====')
        elif len(rrp) == 0 and len(test_cards) > 0:
            self.status = 'finished'
            self.winner = hand_remaining_players[0]
        elif len(rrp) == 1 and rrp == hand_remaining_players:
            self.status = 'finished'
            self.winner = rrp[0]
        elif len(rrp) == 1 and len(hand_remaining_players) == 0:
            self.status = 'finished'
            self.winner = rrp[0]
        else:
            hand_winner = hand_remaining_players[0]
            if self.verbose:
                print(f'Player {hand_winner} won the hand!')
            # distribute the cards to the winning player
            self.cards[hand_winner].extend(trick_cards)


    def play_round(self):
        if self.verbose:
            print('--- Starting game ---')
        i = 1
        while self.status == 'playing' and i <= Game.MAX_HANDS:
            if self.verbose:
                print(f'--- Playing hand {i} ---')            
                print(str(self))
            self.play_hand()
            if self.status == 'finished':
                if self.verbose:
                    print(f'==== Game finished after {i} hands - Player {self.winner} won the game =====')
                return i
            elif i == Game.MAX_HANDS:
                if self.verbose:
                    print(f'Forced game to finish - infinite loop')
                return 0
            else:
                i += 1


# Run a simulation on many games
def simulate(n_games):
    nb_hands_to_finish_game = []
    for _ in range(n_games):
        g = Game(NB_PLAYERS,verbose=True)
        nb_hands = g.play_round()
        nb_hands_to_finish_game.append(nb_hands)
        del g
    return nb_hands_to_finish_game


# r = simulate(100)
# print(f"Number of games that didn't finish {len([e for e in r if e == 0])}")
# print(f"Average number of hands to finish a game {sum(r)/len([e for e in r if e != 0])}")
# print(f"Min-Max number of hands to finish a game {min([e for e in r if e != 0])} - {max(r)}")

# init_s = {0: [5, 3, 5, 1, 1, 2, 4, 1, 4, 6, 2, 6, 3, 6, 4, 2, 5, 3],
#       1: [3, 5, 1, 1, 2, 4, 1, 4, 6, 2, 6, 3, 6, 4, 2, 5, 3, 5]}

# init_s = {0: [6, 1, 6, 5, 3, 3, 2],
#           1: [1, 2, 5, 3, 3, 3, 3, 2, 3, 3, 2, 6, 2, 3, 1, 3, 6, 3, 6, 1, 1, 6, 3],
#           2: [6, 1, 6, 1, 3],
#           3: [1]}

init_s = {
    0: [2, 3, 3, 3, 4, 4, 2, 2, 4, 2, 3, 3],
    1: [3, 3, 3, 4, 4, 2, 2, 5],
    2: [3, 3, 4, 4, 2, 2, 5, 5],
    3: [3, 4, 4, 2, 2, 5, 5, 4]
}

g = Game(4, init_s)
nb_hands = g.play_round()
print(nb_hands)
