#!python3

"""
Implementations of some bin covering algorithms.

AUTHOR: Erel Segal-Halevi
SINCE: 2021-04
"""


class Bin:
    items:list
    sum:int
    def __init__(self):
        self.items = []
        self.sum = 0
    def append(self, item):
        if isinstance(item,list):
            for i in item:
                self.append(i)
        else:
            self.items.append(item)
            self.sum += item
    def __repr__(self):
        return str(self.items)


def bincover_ordered(bin_size:int, item_sizes:list):
    """
    Run a simple bin-covering algorithm:
    it orders the items in descending order, and puts them into a bin until it is filled.
    >>> bincover_ordered(10, [11,12,13])   # large items
    [[13], [12], [11]]
    >>> bincover_ordered(10, [3,3,3,3, 3,3,3,3, 3,3,3])   # identical items
    [[3, 3, 3, 3], [3, 3, 3, 3]]
    >>> bincover_ordered(10, [1,2,3,4,5,6,7,8,9,10])   # different items
    [[10], [9, 8], [7, 6], [5, 4, 3]]
    >>> bincover_ordered(1000, [994, 499,499,499,499,499,499, 1,1,1,1,1,1])   # worst-case example (k=1)
    [[994, 499], [499, 499, 499], [499, 499, 1, 1]]
    >>> bincover_ordered(1000, [988] + 12*[499] + 12*[1])   # worst-case example (k=2)
    [[988, 499], [499, 499, 499], [499, 499, 499], [499, 499, 499], [499, 499, 1, 1]]
    """
    bins = []
    item_sizes.sort(reverse=True)
    bin = Bin()
    while len(item_sizes)>0:
        while len(item_sizes)>0 and bin.sum<bin_size:
            next_item = item_sizes[0]
            bin.append(next_item)
            del item_sizes[0]
        if bin.sum>=bin_size:  # The current bin is full - add it and continue
            bins.append(bin)
            bin = Bin()
    return bins




def bincover_twothirds(bin_size:int, item_sizes:list):
    """
    Run the 2/3-approximation algorithm for bin covering.
    From Csirik et al (1999).

    >>> bincover_twothirds(10, [11,12,13])   # large items
    [[13], [12], [11]]
    >>> bincover_twothirds(10, [3,3,3,3, 3,3,3,3, 3,3,3])   # identical items
    [[3, 3, 3, 3], [3, 3, 3, 3]]
    >>> bincover_twothirds(10, [1,2,3,4,5,6,7,8,9,10])   # different items
    [[10], [9, 1], [8, 2], [7, 3], [6, 4]]
    >>> bincover_twothirds(1000, [994, 499,499,499,499,499,499, 1,1,1,1,1,1])   # worst-case example (k=1)
    [[994, 1, 1, 1, 1, 1, 1], [499, 499, 499], [499, 499, 499]]
    >>> bincover_twothirds(1000, [988] + 12*[499] + 12*[1])   # worst-case example (k=2)
    [[988, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [499, 499, 499], [499, 499, 499], [499, 499, 499], [499, 499, 499]]
    >>> bincover_twothirds(1200, [594,594] + 12*[399] + 12*[1])   # worst-case example for 3/4 (k=1)
    [[594, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 399, 399], [594, 399, 399], [399, 399, 399, 399], [399, 399, 399, 399]]
    """
    bins = []
    item_sizes.sort(reverse=True)
    bin = Bin()
    while len(item_sizes)>0:
        # Initialize with a single biggest item:
        biggest_item = item_sizes[0]
        bin.append(biggest_item)
        del item_sizes[0]

        while len(item_sizes)>0 and bin.sum<bin_size:
            # Fill with the smallest items in ascending order:
            smallest_item = item_sizes[-1]
            bin.append(smallest_item)
            del item_sizes[-1]

        if bin.sum>=bin_size:  # The current bin is full - add it and continue
            bins.append(bin)
            bin = Bin()

    return bins



def bincover_threequarters(bin_size:int, item_sizes:list):
    """
    Run the 3/4-approximation algorithm for bin covering.
    From Csirik et al (1999).

    >>> bincover_threequarters(10, [11,12,13])   # large items
    [[13], [12], [11]]
    >>> bincover_threequarters(10, [3,3,3,3, 3,3,3,3, 3,3,3])   # identical items
    [[3, 3, 3, 3], [3, 3, 3, 3]]
    >>> bincover_threequarters(10, [1,2,3,4,5,6,7,8,9,10])   # different items
    [[10], [9, 1], [8, 2], [7, 3], [6, 5]]
    >>> bincover_threequarters(1000, [994, 499,499,499,499,499,499, 1,1,1,1,1,1])   # worst-case example for 2/3 (k=1)
    [[499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1]]
    >>> bincover_threequarters(1000, [988] + 12*[499] + 12*[1])   # worst-case example for 2/3 (k=2)
    [[499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1]]
    >>> bincover_threequarters(1200, [594,594] + 12*[399] + 12*[1])   # worst-case example for 3/4 (k=1)
    [[594, 594, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [399, 399, 399, 399], [399, 399, 399, 399], [399, 399, 399, 399]]
    >>> bincover_threequarters(1000, [994, 501,501, 499,499,499,499]+12*[1])
    [[499, 499, 1, 1], [499, 499, 1, 1], [994, 1, 1, 1, 1, 1, 1], [501, 501]]
    """
    bins = []
    item_sizes.sort(reverse=True)

    big_items = [item for item in item_sizes if bin_size/2 <= item]  # X
    medium_items = [item for item in item_sizes if bin_size/3 <= item < bin_size/2]  # Y
    small_items = [item for item in item_sizes if item < bin_size/3]  # Z

    bin = Bin()
    while True:
        if len(small_items)==0:
            # NOTE: We re-use the items remaining in the bin.
            return bins + bincover_ordered(bin_size, big_items + bin.items) + bincover_ordered(bin_size, medium_items)

        elif len(big_items)==0 and len(medium_items)==0:
            return bins + bincover_ordered(bin_size, small_items)

        else:
            # Here, there are both small items, and big/medium items.
            # Initialize a bin with either a single biggest item, or two biggest medium items:
            biggest_item = big_items[0:1]              # It will be empty if X is empty
            biggest_medium_items = medium_items[0:2]   # It will be empty if Y is empty
            if sum(biggest_item) >= sum(biggest_medium_items):
                bin.append(biggest_item)
                if len(big_items)>=1: 
                    del big_items[0]
            else:
                bin.append(biggest_medium_items)
                if len(medium_items)>=2: 
                    del medium_items[1]
                if len(medium_items)>=1: 
                    del medium_items[0]

            while len(small_items)>0 and bin.sum<bin_size:
                # Fill with the smallest items in ascending order:
                smallest_item = small_items[-1]
                bin.append(smallest_item)
                del small_items[-1]

            if bin.sum>=bin_size:  # The current bin is full - add it and continue
                bins.append(bin)
                bin = Bin()


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))

