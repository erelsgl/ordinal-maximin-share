#!python3

"""
Experiment comparing various MMS values.
For JAIR paper.

Author: Erel Segal-Halevi
Since : 2021-04
"""

import prtpy
import numpy as np
from collections import OrderedDict
from typing import *

from tee_table.tee_table import TeeTable

random_number_generator = np.random.default_rng()



def smallest_sums(partition:list, num_of_sums:int=1)->float:
    """
    Given a partition, return the sum of the smallest k parts (k = num_of_sums)
    
    >>> smallest_sums([[1,2],[3,4],[5,6]])
    3
    >>> smallest_sums([[1,2],[3,4],[5,6]], num_of_sums=2)
    10
    """
    sorted_sums = sorted([sum(part) for part in partition])
    return sum(sorted_sums[:num_of_sums])



def make_results(random_valuation: Callable, results_csv_file:str, n:int=4):
    TABLE_COLUMNS = [
        "num_of_agents", "num_of_items", "L", "D", 
        "greedy_approximation", "greedy_approximation_to_total", "greedy_approximation_to_MMS",
        "weak_greedy_approximation", "weak_greedy_approximation_to_total", "weak_greedy_approximation_to_MMS",
        ]
    results_table = TeeTable(TABLE_COLUMNS, results_csv_file)
    nums_of_types = [i*4*n for i in range(1,20)]
    num_of_items_per_type = 1
    L_values = range(1,10)
    for num_of_items in nums_of_types:
        valuation = sorted(random_valuation(num_of_items))
        sum_of_values = sum(valuation)
        print(f"\n{num_of_items} items", flush=True)
        # print(f"1-out-of-{n} MMS = ", end="", flush=True)
        # # mms_1_of_n = int(value_1_of_c_MMS(n, valuation, capacity=num_of_items_per_type))
        # print(f"{mms_1_of_n_upper_bound} (100%)", flush=True)
        mms_1_of_n_upper_bound = sum_of_values/n

        for L in L_values:
            D = int((L+1/2)*n)
            greedy_partition_D = prtpy.partition(algorithm=prtpy.approx.greedy, numbins=D, items=valuation)
            greedy_approximation        = smallest_sums(greedy_partition_D, num_of_sums=L)
            weak_greedy_approximation   = L*smallest_sums(greedy_partition_D, num_of_sums=1)
            try:
                results_table.add(OrderedDict((
                    ("num_of_agents", n),
                    ("num_of_items", num_of_items),
                    ("L", L),
                    ("D", D),
                    ("greedy_approximation", greedy_approximation),
                    ("greedy_approximation_to_total", int( (greedy_approximation/sum_of_values) * 100)),
                    ("greedy_approximation_to_MMS",   int( (greedy_approximation/mms_1_of_n_upper_bound) * 100)),
                    ("weak_greedy_approximation", weak_greedy_approximation),
                    ("weak_greedy_approximation_to_total", int( (weak_greedy_approximation/sum_of_values) * 100)),
                    ("weak_greedy_approximation_to_MMS",   int( (weak_greedy_approximation/mms_1_of_n_upper_bound) * 100)),
                )))
            except OSError as err:
                print(f"WARNING: OS error {err}")

    results_table.done()


# Define distributions for the simulations:

def uniform_distribution_low(num_of_items):
    return random_number_generator.integers(1, 1000, num_of_items)

def uniform_distribution_high(num_of_items):
    return random_number_generator.integers(1000, 2000, num_of_items)

def geometric_distribution(num_of_items):
    return random_number_generator.geometric(1/1000, num_of_items)


def make_results_for_JAIR_paper():
    nums_of_agents = range(4,22,2)
    for n in nums_of_agents:
        print(f"n={n}:", flush=True)
        make_results(uniform_distribution_low, "results/unif-1-1000-double.csv", n=n)
        make_results(uniform_distribution_high, "results/unif-1000-2000-double.csv", n=n)
        make_results(geometric_distribution, "results/geom-1000-double.csv", n=n)

if __name__ == "__main__":
    make_results_for_JAIR_paper()
