# Aggregate Function

This repository contains a Python function `aggregate(lst)` that processes a list by aggregating adjacent elements. The function is useful for condensing a list of integers or floats by summing every two consecutive elements into one.

## Function Overview

### `aggregate(lst)`

The `aggregate` function takes a list of integers or floats as input and returns a new list where every two consecutive elements from the original list are aggregated (summed together). If the list has an odd number of elements, the last element remains unchanged.

### Parameters
- `lst`: A list of integers or floats.

### Returns
- A new list where every two consecutive elements are summed together.

### Example

```python
def aggregate(lst):
    length = len(lst)
    ret = [0] * ((length >> 1) + (length & 0b1))
    for i in range(0, length):
        if i % 2 == 1:
            ret[i // 2] = ret[i // 2] + lst[i]
        else:
            ret[i // 2] = lst[i]
    return ret

