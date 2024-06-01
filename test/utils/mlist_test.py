import unittest
import sys
import os

# add path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# import module
from utils.mlist import MessageList

class MListTest(unittest.TestCase):
    # append
    def test_append_empty(self):
        mlist = MessageList() 
        mlist.append('24', 'item')
        iterator = iter(mlist)
        self.assertEqual(next(iterator), 'item')
    def test_append(self):
        mlist = MessageList()
        mlist.append('24', 'item1')
        mlist.append('25', 'item2')
        iterator = iter(mlist)
        self.assertEqual(next(iterator), 'item1')
        self.assertEqual(next(iterator), 'item2')

    # prepend
    def test_prepend_empty(self):
        mlist = MessageList()
        mlist.prepend('24', 'item')
        iterator = iter(mlist)
        self.assertEqual(next(iterator), 'item')
    def test_prepend(self):
        mlist = MessageList()
        mlist.prepend('24', 'item1')
        mlist.prepend('25', 'item2')
        iterator = iter(mlist)
        self.assertEqual(next(iterator), 'item2')
        self.assertEqual(next(iterator), 'item1')

    # delete
    def test_delete(self):
        mlist = MessageList()
        mlist.append('24', 'item1')
        mlist.append('25', 'item2')
        mlist.delete('24')
        iterator = iter(mlist)
        self.assertEqual(next(iterator), 'item2')
    def test_delete_nonexistant(self):
        mlist = MessageList()
        mlist.append('24', 'item1')
        mlist.append('25', 'item2')
        mlist.delete('26')
        iterator = iter(mlist)
        self.assertEqual(next(iterator), 'item1')
        self.assertEqual(next(iterator), 'item2')

    # edit
    def test_edit(self):
        mlist = MessageList()
        mlist.append('24', 'item1')
        mlist.append('25', 'item2')
        mlist.edit('24', 'item3')
        iterator = iter(mlist)
        self.assertEqual(next(iterator), 'item3')
        self.assertEqual(next(iterator), 'item2')
    def test_edit_nonexistant(self):
        mlist = MessageList()
        mlist.append('24', 'item1')
        mlist.append('25', 'item2')
        mlist.edit('26', 'item3')
        iterator = iter(mlist)
        self.assertEqual(next(iterator), 'item1')
        self.assertEqual(next(iterator), 'item2')

    def test_all(self):
        mlist = MessageList()
        mlist.append('24', 'item1')
        mlist.append('25', 'item2')
        mlist.prepend('26', 'item3')
        mlist.edit('24', 'item4')
        mlist.delete('26')
        iterator = iter(mlist)
        self.assertEqual(next(iterator), 'item4')
        self.assertEqual(next(iterator), 'item2')

if __name__ == '__main__':
    unittest.main()