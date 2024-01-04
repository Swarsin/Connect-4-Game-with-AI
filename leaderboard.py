# #code for fetching and sorting the leaderboard

# #sorting algorithm
# def mergeSort(array):
#     if len(array) > 1:
#         middle = len(array) // 2

#         left = array[:middle]
#         right = array[middle:]

#         mergeSort(left)
#         mergeSort(right)

#         i = 0
#         j = 0
#         k = 0 

#         while i < len(left) and j < len(right):
#             if left[i] <= right[j]:
#                 array[k] = left[i]
#                 i += 1
#             else:
#                 array[k] = right[j]
#                 j += 1
#             k += 1
        
#         while i < len(left):
#             array[k] = left[i]
#             i += 1
#             k += 1

#         while j < len(right):
#             array[k] = right[j]
#             j += 1
#             k += 1

# print(mergeSort([14, 24, 23, 5, 7, 8, 2]))


# def merge_sort(array):
#     if len(array) > 1:
#         middle = len(array) // 2
#         left = array[:middle]
#         right = array[middle:]

#         merge_sort(left)
#         merge_sort(right)

#         i, j, k = 0, 0, 0
#         while i < len(left) and j < len(right):
#             if left[i] < right[j]:
#                 array[k] = left[i]
#                 i += 1
#             else:
#                 array[k] = right[j]
#                 j += 1
#             k += 1

#         while i < len(left):
#             array[k] = left[i]
#             i += 1
#             k += 1

#         while j < len(right):
#             array[k] = right[j]
#             j += 1
#             k += 1

# list =[38, 27, 43, 10, 45, 23 , 4, 23, 67]
# print(merge_sort(list))


#Working merge sort
from createtable import list

# def merge_sort(arr, key=lambda x: x[1]):
#     if len(arr) > 1:
#         mid = len(arr) // 2
#         left_half = arr[:mid]
#         right_half = arr[mid:]

#         merge_sort(left_half, key)
#         merge_sort(right_half, key)

#         i, j, k = 0, 0, 0
#         while i < len(left_half) and j < len(right_half):
#             if key(left_half[i]) < key(right_half[j]):
#                 arr[k] = left_half[i]
#                 i += 1
#             else:
#                 arr[k] = right_half[j]
#                 j += 1
#             k += 1

#         while i < len(left_half):
#             arr[k] = left_half[i]
#             i += 1
#             k += 1

#         while j < len(right_half):
#             arr[k] = right_half[j]
#             j += 1
#             k += 1
#     return arr


#print(merge_sort(list)) #both createtable.py and leaderboard.py

def merge_sort(arr, wins=lambda x: x[1]):
    if len(arr) < 2:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    merge_sort(left, wins)
    merge_sort(right, wins)

    i = 0 #index for the left array 
    j = 0 #index for the right array
    k = 0 #index for the main array
    
    while i < len(left) and j < len(right): #while there are elements in the left and right arrays
        if wins(left[i]) > wins(right[j]): #if the current element in the left array is greater than the corresponding in the right array, add it to the main array
            arr[k] = left[i]
            i += 1 
        else:
            arr[k] = right[j] #else (bigger in right array) add it to the main array
            j += 1
        k += 1

    while i < len(left): #copies remaining element from the left array into the main array
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right): #copies any remaining elements from the right array into the main array
        arr[k] = right[j]
        j += 1
        k += 1

    return arr

# Example usage

sorted_tuples = merge_sort(list, wins=lambda x: x[1])

# for i in sorted_tuples:
#     print(i[0])


