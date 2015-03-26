'''
Data bus
'''

# The central data storage bus
# 1. higherarchical, filesystem like
# 2. locations need flexible types
# 3. types need to be pluggable
# 4. needs to basically be a dict

# Import Python libs
import collections


class Leaf(object):
    '''
    The value for every entry in the data bus
    '''
    def __init__(self, value, form='raw'):
        self.value = value
        self.form = form


class Node(collections.MutableMapping):
    '''
    The core data bus class
    '''
    def __init__(self, opts, delim='/', defaults=None):
        self.opts = opts
        self.delim = delim
        self.store = {}
        if defaults:
            self.update(defaults)

    def __getitem__(self, key):
        '''
        Look up the item and return it, check for nested items via the delim
        '''
        if self.delim in key:
            keys = key.split(self.delim)
            keylen = len(keys)
            ret = self.store
            for ind in range(keylen):
                subkey = keys[ind]
                val = ret[subkey]
                if isinstance(val, Node):
                    ret = val
                else:
                    if ind == keylen - 1:
                        return val
                    else:
                        raise KeyError(key)
        else:
            return self.store[key]

    def __setitem__(self, key, value):
        '''
        Set a nested key item
        '''
        if self.delim in key:
            keys = key.split(self.delim)
            keylen = len(keys)
            node = self
            for ind in range(keylen):
                subkey = keys[ind]
                subval = node.get(subkey, None)
                if subval is None:
                    if ind == keylen - 1:
                        node[subkey] = Leaf(value)
                    else:
                        node.store[subkey] = Node(self.opts, self.delim)
                        node = node[subkey]
        else:
            self.store[key] = value

    def __delitem__(self, key):
        '''
        Remove an item from the store
        '''
        if self.delim in key:
            keys = key.split(self.delim)
            keylen = len(keys)
            node = self.store
            for ind in range(keylen):
                subkey = keys[ind]
                val = node[subkey]
                if isinstance(val, Node):
                    node = val
                else:
                    if ind == keylen - 1:
                        del node[subkey]

    def __iter__(self):
        '''
        iterate over the Node
        '''
        for key in self.store:
            val = self.store[key]
            if isinstance(val, Node):
                for ret in val:
                    yield ret
            else:
                yield key

    def __len__(self):
        '''
        Return the length of the Node and sub nodes
        '''
        ret = 0
        for key in self:
            ret += 1
        return ret
