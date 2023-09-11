from sys import *
import local_search
import input
import heuristics as h
import CSP
import time

if __name__ == "__main__":
    time1 = time.clock()
    sud = None

    # The solution method: either CSP or local search
    if argv[1] == "CSP":
        # choosing the grid
        if argv[2] == "easy":
            sud = CSP.CSP(3, input.easy9)
        elif argv[2] == "hard":
            sud = CSP.CSP(3, input.hard9)
        elif argv[2] == "16":
            sud = CSP.CSP(4, input.mid16)

        # choosing set of heuristics
        if argv[3] == '1':
            order = h.by_order
            value = h.random_value
            strategy1 = h.arc_consistency
            strategy2 = h.forward_checking
            sud.solve(order, value, strategy1, strategy2)
        elif argv[3] == '2':
            order = h.by_order
            value = h.random_value
            strategy = h.forward_checking
            sud.solve(order, value, strategy)
        elif argv[3] == '3':
            order = h.min_remaining_value
            value = h.least_constraining_value
            strategy = h.forward_checking
            sud.solve(order, value, strategy)
        elif argv[3] == '4':
            order = h.by_order
            value = h.random_value
            strategy = h.arc_consistency
            sud.solve(order, value, strategy)
        elif argv[3] == '5':
            order = h.min_remaining_value
            value = h.least_constraining_value
            strategy = h.arc_consistency
            sud.solve(order, value, strategy)
        elif argv[3] == '6':
            order = h.min_remaining_value
            value = h.least_constraining_value
            strategy1 = h.arc_consistency
            strategy2 = h.forward_checking
            sud.solve(order, value, strategy1, strategy2)

    elif argv[1] == 'LCL':

        sud = local_search.LocalSearch(3, input.easy9)
        if argv[2] == 'RR':
            sud.random_restart()
        elif argv[2] == 'beam':
            sud.beam_search()

    else:
        print("Wrong parameters, please try again.")

    time2 = time.clock()
    print("Time to solve: ", time2 - time1)
