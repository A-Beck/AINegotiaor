from negotiator_base import BaseNegotiator
from random import random, shuffle


class Negotiator(BaseNegotiator):

    def __init__(self):
        super().__init__()
        self.opponent_utility = 0

    def make_offer(self, offer):
        if self.offer == [] or self.offer is None:
            self.offer = self.preferences[:]
        if self.offer == offer:
            return offer
        else:
            self.offer = self.one_up(offer[:])
            return self.offer

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

    # def receive_utility(self, utility):
    #         self.utility_history[self.current_iter] = (utility, self.utility())
    #
    # def compare_offers(self, opponent_offer):
    #     pass
    #
    # def counter_offer(self, opponent_offer):
    #     pass