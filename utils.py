def ints_in_range(low, high):
    ''' Return the number of ints between low and high. Non-inclusive '''
    low = int(low+1)
    if int(high) == high:
        high = int(high)
    else:
        high = int(high + 1)
    return high - low