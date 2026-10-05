#!/usr/bin/env python3
""" LIFOCache module
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache defines a LIFO caching system
    """

    def __init__(self):
        """ Initialize LIFOCache instance
        """
        super().__init__()
        self.last_key = None

    def put(self, key, item):
        """ Add an item in the cache using LIFO algorithm
        """
        if key is None or item is None:
            return

        if (len(self.cache_data) >= BaseCaching.MAX_ITEMS and
                key not in self.cache_data):
            if self.last_key is not None:
                del self.cache_data[self.last_key]
                print("DISCARD: {}".format(self.last_key))

        self.cache_data[key] = item
        self.last_key = key

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
