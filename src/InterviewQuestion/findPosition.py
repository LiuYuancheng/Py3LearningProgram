#Title
#indices of last negative and first positive numbers from sorted integer array
#Question description
#given a sorted integer array, like [-10,-5,-1,1,4,6,10,100]
#output: [2,3] means​ indices of last negative and first positive numbers

def getIndex(arr):
    low = 0
    high = len(arr) - 1
    res = -1

    while (low < high):
        mid = (low + high) // 2
        if mid == res:
            break
        if arr[mid] > 0:
            high = mid
        elif arr[mid] < 0:
            low = mid
        else:
            low = mid - 1
        res = mid

    return (low, high)

arr = [-10, -5, -1, 1, 4, 6, 10, 100]
#arr = [-10, -5, -1, -1, 0, 4, 6, 10, 100]
#arr = [-10, -5, 4, 6, 10, 100]

reuslt = getIndex(arr)
print(reuslt)
