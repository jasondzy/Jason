def insert_seq(seq_data):
    """这里是采用插入排序的方式，具体实现原理是通过将序列分成两列来对待，即前边的有序序列和后边的无序序列，每次从无序序列中提取一个数插入到前边的有序序列中去"""
    n = len(seq_data)
    for j in range(n):
        i = j
        while i > 0:
            if seq_data[i] < seq_data[i-1]:
                seq_data[i-1], seq_data[i] = seq_data[i], seq_data[i-1]
            i -= 1


if __name__ == '__main__':
    seq = [54, 226, 93, 17, 77, 31, 44, 55, 20, 6, 23, 54]

    insert_seq(seq)

    print(seq)