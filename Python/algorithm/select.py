def select_seq(seq_data):
    """插入排序的核心思想是找到后边无序序列中的最小值，并将最小值一次的放入序列的开头"""
    n = len(seq_data)

    for j in range(n-1):
        i = j
        min_value = i
        for i in range(i, n):
            if seq_data[i] < seq_data[min_value]:
                seq_data[min_value], seq_data[i] = seq_data[i], seq_data[min_value]


if __name__ == '__main__':
    seq = [54, 226, 93, 17, 77, 31, 44, 55, 20, 6, 23, 54]

    select_seq(seq)

    print(seq)