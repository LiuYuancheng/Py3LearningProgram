# Python program to reverse a linked list
# Time Complexity : O(n)
# Space Complexity : O(n) as 'next'
#variable is getting created in each loop.

# Node class
import copy

class Node:
    # Constructor to initialize the node object
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:

    # Function to initialize head
    def __init__(self):
        self.head = None

    # Function to reverse the linked list
    def reverse(self):
        prev = None
        current = self.head
        while(current is not None):
            next = current.next
            current.next = prev
            prev = current
            current = next
        self.head = prev

    # Function to insert a new node at the beginning
    def push(self, newNode):
        newNode.next = self.head
        self.head = newNode

    # Utility function to print the linked LinkedList
    def printList(self):
        temp = self.head
        while temp:
            print(temp.data)
            temp = temp.next

    def splitN(self, n):
        temp = self.head
        count = 0
        while temp:
            #print(temp.data)
            temp = temp.next
            count +=1
            if count == n:
                splitedList = LinkedList()
                splitedList.push(temp)
                temp.next = None
                return splitedList


# Driver program to test above functions
llist = LinkedList()
llist.push(Node(4))
llist.push(Node(3))
llist.push(Node(2))
llist.push(Node(1))

print("Given Linked List")
llist.printList()

llist.reverse()
print("\nReversed Linked List")
llist.printList()

print(">> split N")
nList = llist.splitN(2)
nList.printList()
llist.printList()

# This code is contributed by Nikhil Kumar Singh(nickzuck_007)

#Title
#indices of last negative and first positive numbers from sorted integer array

#Question description
#given a sorted integer array, like [-10,-5,-1,1,4,6,10,100]​
#output: [2,3] means​
#indices of last negative and first positive numbers

# Python3 program to find first and
# last occurrences of a number in a
# given sorted array

# If x is present in arr[] then
# returns the index of FIRST
# occurrence of x in arr[0..n-1],
# otherwise returns -1
def first(arr, x, n):
    
    low = 0
    high = n - 1
    res = -1
    
    while (low <= high):
        
        # Normal Binary Search Logic
        mid = (low + high) // 2
        
        if arr[mid] > x:
            high = mid - 1
        elif arr[mid] < x:
            low = mid + 1
            
        # If arr[mid] is same as x, we
        # update res and move to the left
        # half.
        else:
            res = mid
            high = mid - 1

    return res

# If x is present in arr[] then returns
# the index of FIRST occurrence of x in
# arr[0..n-1], otherwise returns -1
def last(arr, x, n):
    
    low = 0
    high = n - 1
    res = -1
    
    while(low <= high):
        
        # Normal Binary Search Logic
        mid = (low + high) // 2
        
        if arr[mid] > x:
            high = mid - 1
        elif arr[mid] < x:
            low = mid + 1
            
        # If arr[mid] is same as x, we
        # update res and move to the Right
        # half.
        else:
            res = mid
            low = mid + 1

    return res

# Driver code
arr = [ 1, 2, 2, 2, 2, 3, 4, 7, 8, 8 ]
n = len(arr)
x = 8

print("First Occurrence =", first(arr, x, n))
print("Last Occurrence =", last(arr, x, n))

# This code is contributed by Ediga_Manisha.
