
def recursive_max(arr):
    if len(arr) == 1:
        return arr[0]
    
    else:
        return max(arr[-1], recursive_max(arr[:-1]))

def recursive_min(arr):
    if len(arr) == 1:
        return arr[0]

    else:
        return min(arr[-1], recursive_min(arr[:-1]))

def recursive_sum_of(arr):
    if len(arr) == 0:
        return 0
    else:
        return arr[0] + recursive_sum_of(arr[1:])

def recursive_length(arr):
    if len(arr) == 0:
        return 0
    else:
        return 1 + recursive_length(arr[1:])

nums = input("Enter a list of numbers separated by spaces: ").split()
nums = list(map(int, nums))

print("Maximum value:", recursive_max(nums))
print("Minimum value:", recursive_min(nums))
print("Average of given list:", recursive_sum_of(nums) / recursive_length(nums))