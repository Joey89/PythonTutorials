# make a doubly linked list for calling which function runs next. and prev.
'''
class Node:
    # instance attributes
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insertAtBeginning(self, new_data):
        new_node = Node(new_data)  # Create a new node 
    
        if self.head is None: #first new_node.. make head and tail point to this node
            self.head = new_node
            self.tail = new_node
        else: # second new_node, 
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            
    def insertAtEnd(self, new_data):
        new_node = Node(new_data)
        if self.head is None: #first new_node.. make head and tail point to this node
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node # LL Tail.next is now the last entered node
            self.tail = new_node      # LL Tail is now the new last entered node

    def removeAtStart(self):
        #self.head.next.prev = None
        self.head = self.head.next

    def removeAtEnd(self):
        temp = self.head # Start from the head of the list
        while temp.next.next:
            temp = temp.next # Move to the next node
        temp.next = None
        self.tail = self.tail.prev

    def printList(self):
        temp = self.head # Start from the head of the list
        while temp:
            print(temp.data,end=' ') # Print the data in the current node
            temp = temp.next # Move to the next node
        print()  # Ensures the output is followed by a new line
        
    def printListRev(self):
        temp = self.tail # Start from the tail of the list
        while temp:
            print(temp.data,end=' ') # Print the data in the current node
            temp = temp.prev # Move to the prev node
        print()  # Ensures the output is followed by a new line
        
    def countNodes(self):
        x = 1
        if self.head is None:
            x = 0
        else:
            next = self.head.next
        while self.head != None and self.head.next != None:
            self.head = self.head.next
            x+=1
        return x
    
    def find(self, needle):
        if self.head is not None:
            while self.head.next != None:
                if needle == self.head.data:
                    print("Found item")
                    return needle
                self.head = self.head.next
        return False
    

def test():
    return 444

def test2():
    return 8888

def test3():
    return 5555


joe = DoublyLinkedList()

joe.insertAtBeginning(test())
joe.insertAtBeginning(test2())
joe.insertAtBeginning(test3())
    # [ 5555, 8888, 444]
#joe.removeAtEnd()


#print("\n")
#joe.printList()

#print(joe.head.next.prev.data)



#test
'''
myList = [ 9, 5, 2, 5, 6, 7, 1, 5]


def insertionSort(n):

    i=1
    while( i < len(n)): # start at 1
        temp = n[i] # pos [1] 5
        j = i-1 # [0] 9
        print(temp)
        #[9, 5]
        while( j>=0 and n[j] > temp ): # while n[n-1] is greater than n[n]
            n[j+1] = n[j] # move next pos to current
            #[x, 9]
            j-=1
        #[5, 9]
        n[j+1] = temp
        i+=1


insertionSort(myList)

print(myList)