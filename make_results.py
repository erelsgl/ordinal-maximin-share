#!python3

"""
Experiment comparing various MMS values.
For JAIR paper.

Author: Erel Segal-Halevi
Since : 2021-04
"""

import prtpy
import numpy as np
from typing import *


#### UTILITIES:

random_number_generator = np.random.default_rng()

def uniform_distribution_low(num_of_items):
    return random_number_generator.integers(1, 1000, num_of_items)

def uniform_distribution_high(num_of_items):
    return random_number_generator.integers(1000, 2000, num_of_items)

def geometric_distribution(num_of_items):
    return random_number_generator.geometric(1/1000, num_of_items)

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




#### Run single instance:

def run_single_instance(random_valuation: Callable, num_of_agents:int, num_of_items_per_agent:int, L:int)->dict:
    num_of_items = num_of_items_per_agent*num_of_agents
    valuation = sorted(random_valuation(num_of_items))  # TODO: Construct valuation once for all values of L (for the same num_of_items)
    sum_of_values = sum(valuation)
    # print(f"\n{num_of_items} items", flush=True)
    mms_1_of_n_upper_bound = sum_of_values/num_of_agents

    D = int((L+1/2)*num_of_agents)
    greedy_partition_D = prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=D, items=valuation)
    greedy_approximation        = smallest_sums(greedy_partition_D, num_of_sums=L)
    weak_greedy_approximation   = L*smallest_sums(greedy_partition_D, num_of_sums=1)
    return {
        "D": D,
        "num_of_items": num_of_items,
        "greedy_approximation": greedy_approximation,
        "greedy_approximation_to_total": int( (greedy_approximation/sum_of_values) * 100),
        "greedy_approximation_to_MMS":   int( (greedy_approximation/mms_1_of_n_upper_bound) * 100),
        "weak_greedy_approximation": weak_greedy_approximation,
        "weak_greedy_approximation_to_total": int( (weak_greedy_approximation/sum_of_values) * 100),
        "weak_greedy_approximation_to_MMS":  int( (weak_greedy_approximation/mms_1_of_n_upper_bound) * 100),
    }


def make_results_for_JAIR_paper():
    import experiments_csv, logging
    experiments_csv.logger.setLevel(logging.INFO)

    input_ranges = {
        "num_of_agents": range(4,22,2),
        "num_of_items_per_agent": [4*i for i in range(1,20)],
        "L": range(1,10),
    }

    ex = experiments_csv.Experiment("results/", "unif-1-1000-double.csv", "results/backups/")
    input_ranges["random_valuation"] = [uniform_distribution_low]
    ex.run(run_single_instance, input_ranges)

    ex = experiments_csv.Experiment("results/", "unif-1000-2000-double.csv", "results/backups/")
    input_ranges["random_valuation"] = [uniform_distribution_high]
    ex.run(run_single_instance, input_ranges)

    ex = experiments_csv.Experiment("results/", "geom-1000-double.csv", "results/backups/")
    input_ranges["random_valuation"] = [geometric_distribution]
    ex.run(run_single_instance, input_ranges)

if __name__ == "__main__":
    make_results_for_JAIR_paper()
