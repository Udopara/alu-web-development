#!/usr/bin/env python3
""" MRUCache module
"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache defines a MRU caching system
    """

    def __init__(self):
        """ Initialize MRUCache instance
        """
        super().__init__()
        self.mru_key = None

    def put(self, key, item):
        """ Add an item in the cache using MRU algorithm
        """
        if key is None or item is None:
            return

        if (len(self.cache_data) >= BaseCaching.MAX_ITEMS and
                key not in self.cache_data):
            if self.mru_key is not None and self.mru_key in self.cache_data:
                del self.cache_data[self.mru_key]
                print("DISCARD: {}".format(self.mru_key))

        self.cache_data[key] = item
        self.mru_key = key

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        self.mru_key = key
        return self.cache_data[key]
