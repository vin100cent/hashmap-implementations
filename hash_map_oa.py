# Name: Vincewa Tran
# OSU Email: tranvinc@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/7/2023
# Description: Implementation of a hash map using open addressing with
# quadratic probing for collision resolution. The underlying data structure
# is a dynamic array or key/value pairs. The number of objects in the hash
# are from [0, 1,000,000].
# Methods:
# put() - adds or updates a new key/value pair to the hash map.
# resize_table() - resizes the hash table to passed in new capacity.
# table_load() - returns the current load factor of the hash table.
# empty_buckets() - returns the number of empty buckets in the hash table.
# get() - returns the value associated with the given key.
# contains_key() - returns whether or not a key is in the hash table.
# remove() - removes the key/value pair associated with the given key.
# get_keys_and_values() - returns a dynamic array of all keys and values in the hash table.
# clear() - clears all contents of the hash table without changing the underlying hash table capacity.
# __iter__(), __next__()
# methods to enable iteration over the hash map.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key/value pair in the hashmap
        param key: key to be updated
        param value: value to be updated
        conditions: if key is already in hashmap, update value @ key with new value
                    if key is not in hashmap, a new key/value pair is added

        """
        threshold = 0.5

        # resize if load factor is greater than threshold
        if self.table_load() > threshold:
            self.resize_table(self._capacity*2)

        # get the starting index using hash function and probe open index
        hashIndex = self._hash_function(key) % self._capacity
        target = self._quad_probe(hashIndex, key)

        # Insert key/value pair if target index is empty or tombstone(removed)
        if self._buckets.get_at_index(target) is None or \
                self._buckets.get_at_index(target).is_tombstone:
            self._buckets.set_at_index(target, HashEntry(key, value))
            self._size += 1

            # if tombstone, set to False to indicate index is no longer removed
            if self._buckets.get_at_index(target).is_tombstone:
                self._buckets.get_at_index(target).is_tombstone = False

        else:
            # update key/value pair at the target index
            self._buckets.set_at_index(target, HashEntry(key, value))

    def _quad_probe(self, hash_index: int, key: str) -> int:
        """
        helper method to probe for an open index using quadratic probing
        """
        offset = 1
        openIndex = hash_index

        # probe until an available spot is found
        while self._buckets.get_at_index(openIndex):
            if self._buckets.get_at_index(openIndex).key == key:
                return openIndex

            # update target index using quadratic probing
            openIndex = (hash_index + offset ** 2) % self._capacity
            offset += 1

        # return valid index to insert a key/value pair
        return openIndex

    def resize_table(self, new_capacity: int) -> None:
        """
        Change capacity of the internal hash table to new_capacity
        param new_capacity: new capacity to resize to
        """

        # Check if new capacity is greater than current size if not return
        # without resizing
        if new_capacity <= self._size:
            return

        # make sure new capacity is prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # new table with updated capacity
        resizedTable = HashMap(new_capacity, self._hash_function)

        if new_capacity == 2:
            resizedTable._capacity = 2

        # iterate through and rehash items from old table to new table
        for item in self:
            if item:
                resizedTable.put(item.key, item.value)

        # update data
        self._buckets = resizedTable._buckets
        self._size = resizedTable._size
        self._capacity = resizedTable.get_capacity()

    def table_load(self) -> float:
        """
        Calculate and return load factor
        load factor(lambda) = n(number of elements)/m(number of buckets)
        return float: load factor
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets. Simpler than chained hashmap.
        empty buckets = m - n
        return int: number of empty buckets
        """
        return self._capacity-self._size

    def get(self, key: str) -> object:
        """
        Get value associated with key
        param key: key user is searching for
        return object: target key's value
        """
        for item in self:
            if item and item.key == key and not item.is_tombstone:
                    return item.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Check if key is in hashmap
        param key: key user is searching for
        return bool: True if key is found else False
        """
        for item in self:
            if item and item.key == key and not item.is_tombstone:
                    return True

        return False

    def remove(self, key: str) -> None:
        """
        Searches for and removes target key from hashmap
        param key: key user wishes to remove
        """
        for item in self:
            # remove item by setting tombstone to True and decr size
            if item and item.key == key and not item.is_tombstone:
                    item.is_tombstone = True
                    self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all keys and values in a hashmap
        return DynamicArray: DynamicArray, contains tuples of key and value
        """
        tupleArr = DynamicArray()

        for item in self:
            if item and not item.is_tombstone:
                tupleArr.append((item.key, item.value))

        return tupleArr

    def clear(self) -> None:
        """
        Clears all contents of the hashmap without changing underlying hash
        table capacity
        """
        # new DA to store hash elements, clears existing contents
        self._buckets = DynamicArray()
        # set everything to None and reset size to None to indicate empty
        # hashmap
        for bucket in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def __iter__(self):
        """
        Enables iteration over hashmap
        """
        self.index = 0
        return self

    def __next__(self):
        """
        Returns the next item in the hashmap based on the current location of the iterator
        return value: next item in hashmap that is not a tombstone or None
        """
        try:
            value = None

            # loop until not none or tombstoned
            while value is None or value.is_tombstone:
                value = self._buckets.get_at_index(self.index)
                self.index += 1

        # if out of bounds raise StopIteration
        except DynamicArrayException:
            raise StopIteration

        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
