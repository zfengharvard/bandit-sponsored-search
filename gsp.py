###################
# Implements GSP class
# Includes Functions:
# - compute: return allocation and payment
###################


import numpy as np
import random
import math


class GSP():
    """
    Implements the generalized second price auction mechanism.
    """
    def __init__(self, slot_clicks, reserve, bids, slot):
        self.slot_clicks = slot_clicks
        self.reserve = reserve
        self.bids = bids
        self.slot = slot
    
    
    def compute(self):
        """
        Given info about the setting (clicks for each slot, and self.reserve price),
        and self.bids (list of (id, bid) tuples), compute the following:
          allocation:  list of the occupant in each slot
              len(allocation) = min(len(self.bids), len(self.slot_clicks))
          per_click_payments: list of payments for each slot
              len(per_click_payments) = len(allocation)

        If any self.bids are below the self.reserve price, they are ignored.

        Returns a pair of lists (allocation, per_click_payments):
         - allocation is a list of the ids of the bidders in each slot
            (in order)
         - per_click_payments is the corresponding payments.
        """
        valid = lambda (a, bid): bid >= self.reserve
        valid_self.bids = filter(valid, self.bids)

        rev_cmp_self.bids = lambda (a1, b1), (a2, b2): cmp(b2, b1)
        # shuffle first to make sure we don't have any bias for lower or
        # higher ids
        random.shuffle(valid_self.bids)
        valid_self.bids.sort(rev_cmp_self.bids)

        num_slots = len(self.slot_clicks)
        allocated_self.bids = valid_self.bids[:num_slots]
        if len(allocated_self.bids) == 0:
            return ([], [])

        (allocation, just_self.bids) = zip(*allocated_self.bids)

        # Each pays the bid below them, or the self.reserve
        per_click_payments = list(just_self.bids[1:])  # first num_slots - 1 slots
        # figure out whether the last slot payment is set by the self.reserve or
        # the first non-allocated bidder
        if len(valid_self.bids) > num_slots:
            last_payment = valid_self.bids[num_slots][1]
        else:
            last_payment = self.reserve
        per_click_payments.append(last_payment)
        return (list(allocation), per_click_payments)

       

