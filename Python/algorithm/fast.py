def fast_seq(seq_data, start, end):
    """如下是快速排序的代码，快速排序代码采用的是low和high两个位置坐标来对数列进行迭代的寻找首元素的位置的操作"""
    mid_value = seq_data[start]
    low = start
    high = end

    if start >= end:
        return

    while low < high:
        while low < high and seq_data[high] >= mid_value:
            high -= 1
        seq_data[low] = seq_data[high]

        while low < high and seq_data[low] < mid_value:
            low += 1
        seq_data[high] = seq_data[low]

    seq_data[low] = mid_value
    fast_seq(seq_data,start, low-1)
    fast_seq(seq_data, low+1, end)

#    return left_seq + right_seq


if __name__ == '__main__':
    seq = [54, 226, 93, 17, 77, 31, 44, 55, 20, 6, 23, 54]

    fast_seq(seq, 0, len(seq)-1)

    print(seq)