# USE THIS AGENT IN PEER-PEER NEGOTIATIONS

from negotiator_base import BaseNegotiator
from random import random, shuffle

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
        self.current_iter = 0  # the current iteration of negotiations in the round
        self.round_number = 0  # the current round
        self.thresh = 0  # minimum utility we will accept, placeholder
        # keeps track of past opponent utilities: dict(round_number : dict(iteration : utility))
        self.utility_history = {}
        # keeps track of past opponent offers: dict(round_number : dict(iteration : offer))
        self.offer_history = {}
        # keeps track of the results of past rounds: dict(round_number : dict (bool, flt,flt, int))
        self.result_history = {}
        # keeps track of our past offers, cleared after each round is completed
        self.past_offers = []
        # True if making the final offer, false if going first
        self.goes_last = True

    def initialize(self, preferences, iter_limit):
        super().initialize(preferences, iter_limit)
        self.thresh = 0.75 * self.calc_utility(self.preferences)

    def make_offer(self, offer):
        #set up history data structure for current round, if needed
        self.current_iter += 1
        if self.round_number not in self.offer_history.keys():
            self.offer_history[self.round_number] = {}
        if offer is None:
            # Need to make a first offer to start negotiations, does not go last
            self.goes_last = False
            my_offer = self.make_first_offer()
        elif self.current_iter == self.iter_limit:
            # Last round - update variables, make a last offer
            self.offer_history[self.round_number][self.current_iter] = offer  # record current offer in history
            self.current_iter = 0
            my_offer = self.make_final_offer(offer)
        else:
            # In the middle of negotiations, make an offer
            self.offer_history[self.round_number][self.current_iter] = offer[:]  # record current offer in history
            my_offer = self.make_intermediate_offer(offer[:])
        self.past_offers.append(my_offer)  # keep track of our offer
        self.offer = my_offer[:]
        return self.offer[:]

    def make_first_offer(self):
        #print('first offer')
        return self.preferences[:]

    def make_intermediate_offer(self, offer):
        #print('in middle of negotiations')
        if self.offer == [] or self.offer is None:
            # if it is empty or none, initialize self.offer for one_up and random offer functions
            self.offer = self.make_first_offer()
        if offer in self.past_offers:
            return offer[:]
        elif random() < 0.10:
            my_offer = self.random_offer()
            return my_offer
        else:
            #if self.is_our_utility_higher(offer):
                #return offer
            self.submit_prefs_if_final()
            if self.is_too_late():
                return offer
            my_offer = self.one_up(offer)
            return my_offer

    def make_final_offer(self, offer):
        #print('in final inter')
        if offer in self.past_offers:
            return offer
        else:
            my_offer = self.one_up(offer)
            return my_offer

    def one_up(self, opponent_offer):
        if opponent_offer is None:
            return self.make_first_offer()
        if self.offer == opponent_offer:
            return opponent_offer
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
        # receives opponents utility and stores it
        if self.round_number not in self.utility_history.keys():
            self.utility_history[self.round_number] = {}
        round_hist = self.utility_history[self.round_number]
        round_hist[self.current_iter] = utility

    def receive_results(self, results):
        # at the end of a negotiation, store the result of that negotiation
        self.result_history[self.round_number] = results
        # update our threshold based on negotiation results
        if self.goes_last:
            res = results[2]
        else:
            res = results[1]
        if res > 0:
            self.thresh = (self.thresh * 0.75) + (.25 * res)
        self.round_number += 1  # this round is over, increment round number
        self.past_offers = []  # this round of our negotiation is over, we can clear our offer history

    def calc_utility(self, offer):
        # This is the way florian said to do it in class on 4/7
        old_offer = self.offer
        self.offer = offer[:]
        util = self.utility()
        self.offer = old_offer
        return util

    def random_offer(self):
        # create a random offer, so our bot is harder to characterize
        util = -1
        count = 0
        rand_offer = self.offer[:]
        final_offer = rand_offer[:]
        while util < self.thresh and count < 20:
            shuffle(rand_offer)
            next_util = self.calc_utility(rand_offer)
            if next_util > util:
                util = next_util
                final_offer = rand_offer[:]
        self.offer = final_offer[:]
        return self.offer

    def is_too_late(self):
        # If the number of iterations exceeds 8, meaning that 8 iterations have passed without an offer being accepted,
        # accept the next offer, since the likelihood of losing more utility is high
        if self.goes_last is False and self.current_iter > int(self.iter_limit * 0.8):
            return True
        return False

    def submit_prefs_if_final(self):
        # If we go last, and it is the last iteration of the round, submit our preferences list
        if self.goes_last and self.current_iter == 10:
            return self.preferences[:]

    def is_our_utility_higher(self, opponent_offer):
        # If our utility is greater than the opponent's utility recieved in the last iteration, accept the offer
        our_utility = self.calc_utility(opponent_offer)
        their_utility = self.utility_history.get(self.round_number).get(self.current_iter - 1)
        if our_utility > their_utility:
            return True