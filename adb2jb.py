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
        self.utility_history = {}

    def make_offer(self, offer):
        if offer is not None:
            offer_util = self.calc_utility(offer)
            if self.current_iter > 0:
                old_util = self.utility_history[self.self.current_iter][0]
        self.current_iter += 1
        if random() < 0.05 and offer:
            # Very important - we save the offer we're going to return as self.offer
            self.offer = offer[:]
            return offer
        else:
            ordering = self.preferences
            shuffle(ordering)
            self.offer = ordering[:]
            return self.offer

    def receive_utility(self, utility):
        #                                         opponent | your utility
        self.utility_history[self.current_iter] = (utility , self.utility())

    def calc_utility(self, offer):
        total = len(self.preferences)
        util = reduce(lambda points, item: points + ((total / (offer.index(item) + 1)) - abs(offer.index(item) - self.preferences.index(item))), offer, 0)
        return util