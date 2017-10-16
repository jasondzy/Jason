def sort(left, right):
    lst = []
    j = 0
    i = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            lst.append(left[i])
            i = i+1
        else:
            lst.append(right[j])
            j += 1
    lst += left[i:]
    lst += right[j:]

    return lst


def merge(lst):

    if len(lst) <= 1:
        return lst

    middle = len(lst) // 2
    left = merge(lst[:middle])
    right = merge(lst[middle:])

    return sort(left, right)


if __name__ == '__main__':
    ll = [54, 26, 93, 17, 77, 31, 44, 55, 20]
    result = merge(ll)
    print(result)