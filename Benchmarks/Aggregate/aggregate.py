def aggregate(lst):
    length = len(lst)
    ret = [0] * ((length >> 1) + (length & 0b1))
    for i in range(0, length):
        if i % 2 == 1:
            ret[i // 2] = ret[i // 2] + lst[i]
        else:
            ret[i // 2] = lst[i]
    return ret

# Test the aggregate function with a sample list
sample_list = [1, 2, 3, 4, 5]
result = aggregate(sample_list)
print("Aggregated List:", result)

