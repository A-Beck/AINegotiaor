from negotiator_base import BaseNegotiator
from random import random, shuffle
from functools import reduce

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".

class Negotiator(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 5%
    # of the time, and return a random permutation the rest of the time.

    def __init__(self):
        super().__init__()
        self.current_iter = 0
        self.round_number = 0
        self.utility_history = {}  # keeps track of past opponent utilities
        self.offer_history = {}  # keeps track of past opponent offers
        self.result_history = {}
        self.past_offers = []  # keeps track of our past offers
        self.goes_last = True

    def make_offer(self, offer):
        #set up history data structure for current round
        self.current_iter += 1
        if self.round_number not in self.utility_history.keys():
            self.utility_history[self.round_number] = {}
        if self.round_number not in self.offer_history.keys():
            self.offer_history[self.round_number] = {}
        if offer is None:
            # Need to make a first offer to start negotiations, does not go last
            # This offer does not count towards the number of negotiations
            self.goes_last = False
            my_offer = self.make_first_offer()
            self.past_offers.append(offer)
        elif self.current_iter == self.iter_limit:
            # Last round - update variables, make a last offer
            self.offer_history[self.round_number][self.current_iter] = offer  # record current offer in history
            self.current_iter = 0
            my_offer = self.make_final_offer(offer)
        elif offer is not None:
            # In the middle of negotiations, make an offer
            self.offer_history[self.round_number][self.current_iter] = offer  # record current offer in history
            my_offer = self.make_intermediate_offer(offer)
        self.past_offers.append(my_offer)
        self.offer = my_offer[:]
        return self.offer[:]

    def make_first_offer(self):
        # print('first offer')
        return self.preferences[:]

    def make_intermediate_offer(self, offer):
        print('in middle of negotiations')
        if offer in self.past_offers:
            return offer[:]
        else:
            my_offer = self.one_up(offer)
            return my_offer

    def make_final_offer(self, offer):
        print('in final inter')
        if offer in self.past_offers:
            return offer
        else:
            my_offer = self.one_up(offer)
            return my_offer

    def one_up(self, opponent_offer):
        if opponent_offer is None:
            return self.offer
        if self.offer == opponent_offer:
            return self.offer
        starting_index = 0
        while self.offer[starting_index] == opponent_offer[starting_index]:
            if starting_index == len(self.offer) - 1:
                break
            starting_index += 1
        swap_index = starting_index
        while True:
            if self.offer[swap_index] == opponent_offer[starting_index]:
                break
            else:
                swap_index += 1
        self.offer[starting_index], self.offer[swap_index] = self.offer[swap_index], self.offer[starting_index]
        return self.offer

    def receive_utility(self, utility):
        # recieves the utility from the previous negotiation and puts it into the right place in history
        round_hist = self.utility_history[self.round_number]
        round_hist[self.current_iter] = utility

    def receive_results(self, results):
        # at the end of a negotiation, store the result of that negotiation
        self.result_history[self.round_number] = results
        self.round_number += 1  # this round is over, increment round number
        self.past_offers = []  # this round of our negotiation is over, we can clear our offer history

    def calc_utility(self, offer):
        # This is the way florian said to do it in class on 4/7
        old_offer = self.offer
        self.offer = offer
        util = self.utility()
        self.offer = old_offer
        return util