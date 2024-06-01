from collections import defaultdict

'''
This is a doubly linked list + dictionary implementation of a message list.
'''
class MessageList:

    class Node:
        def __init__(self, message):
            '''Initialize a node with a message string.'''

            self.message = message
            self.next = None
            self.prev = None
        
    def __init__(self, messages = []):
        '''Initialize an empty list.'''

        self.message_dict = defaultdict(lambda: None)
        self.head = None
        self.tail = None
        for message in messages:
            self.append(message.get('id'), message)

    def append(self, message_id, message):
        '''Append a message to the list.'''

        # add message to llist
        new_node = self.Node(message)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        # add message to dict
        self.message_dict[message_id] = new_node

    def prepend(self, message_id, message):
        '''Prepend a message to the list.'''

        # add message to llist
        new_node = self.Node(message)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        # add message to dict
        self.message_dict[message_id] = new_node

    def delete(self, message_id):
        '''Delete a message from the list.'''

        # find message using dict
        node = self.message_dict[message_id]
        if node is None:
            return

        # remove message from llist
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        # remove message from dict
        del self.message_dict[message_id]

    def edit(self, message_id, new_message):
        '''Edit a message in the list.'''
        # edit message in dict
        node = self.message_dict[message_id]
        if node is None:
            return
        
        node.message = new_message

    # TODO: find a better way to implement this
    def __iter__(self):
        '''Return an iterator for the list.'''
        self.node = self.head
        return self

    def __next__(self):
        '''Return the next node in the list.'''
        if self.node is None:
            raise StopIteration
        else:
            node = self.node
            self.node = self.node.next
            return node.message