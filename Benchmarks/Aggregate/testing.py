import time
import pytest
from typing import List

# Function to aggregate elements by summing consecutive pairs
def aggregate(lst):
    length = len(lst)
    result = [0] * ((length >> 1) + (length & 1))
    for i in range(length):
        if i % 2 == 0:
            result[i // 2] = lst[i]
        else:
            result[i // 2] += lst[i]
    return result


# Test cases to check the correctness of the aggregate function
@pytest.mark.parametrize("input_list, expected_output", [
    ([1, 2, 3, 4], [1, 6]),  # Basic even number of elements
    ([1, 2, 3], [1, 5]),  # Odd number of elements
    ([], []),  # Empty list
    ([10], [10]),  # Single element
    ([1, 2, 3, 4, 5], [3, 7, 5]),  # Odd number with more elements
    ([0, 0, 0, 0], [0, 0]),  # List with zeros
    ([100, 200, 300, 400, 500], [100, 500, 500])  # List with large numbers
])
def test_aggregate(input_list, expected_output):
    assert aggregate(input_list) == expected_output

@pytest.mark.parametrize("input_list, expected_output", [
    ([i for i in range(16)], [sum([i, i+1]) if i % 2 == 0 else None for i in range(15)]),  # Sequential large list
    ([-1, 1, -2, 2, -3, 3], [-1, 0, -3]),  # List with negatives
    ([2**i for i in range(8)], [2**i for i in range(8)])  # Powers of two
])
def test_edge_cases(input_list, expected_output):
    assert aggregate(input_list) == expected_output

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("Runtime:", str(time.time() - start_time))

    request.addfinalizer(finalizer)

# To run the tests if this script is executed directly
if __name__ == "__main__":
    pytest.main([__file__])

