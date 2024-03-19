from collections import defaultdict

class MessageList:

    class Node:
        def __init__(self, message_string):
            '''Initialize a node with a message string.'''

            self.message_string = message_string
            self.next = None
            self.prev = None
        
    def __init__(self):
        '''Initialize an empty list.'''

        self.message_dict = defaultdict(None)
        self.head = None
        self.tail = None

    def append(self, message_string, message_id):
        '''Append a message to the list.'''

        new_node = self.new_Node(message_string)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        # add message to cache
        self.message_dict[message_id] = new_node

    def prepend(self, message_string, message_id):
        '''Prepend a message to the list.'''

        new_node = self.new_Node(message_string)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        # add message to cache
        self.message_dict[message_id] = new_node

    def delete(self, message_id):
        '''Delete a message from the list.'''

        node = self.message_dict[message_id]

        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        # remove message from cache
        del self.message_dict[message_id]

    def edit(self, message_id, new_message_string):
        '''Edit a message in the list.'''

        self.message_dict[message_id].message_string = new_message_string