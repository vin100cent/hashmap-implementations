# Name: Vincewa Tran
# OSU Email: tranvinc@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/07/2023
# Description: Hash Map implementation using separate chaining for collision
# resolution. The underlying data structure is a DynamicArray of LinkedLists(
# singly linked lists).
# Methods:
# put(): updates the key/value pair in the hash map
# resize_table(): changes the capacity of the internal hash table
# table_load(): calculates and returns the load factor
# empty_buckets(): returns the number of empty buckets in the table
# get(): returns a value associated with the given key
# contains_key(): returns whether or not a key is in the hash map
# remove(): removes a key/value pair from the hash map
# get_keys_and_values(): returns a DynamicArray of tuples containing  all the
# key/value pairs in the hash map
# clear(): clears the hash map
# find_mode(): returns the mode(s) and their frequency in a tuple


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        updates the key/value pair in the hash map. If key already exists in
        the hash map, its associated value is replaced with the new value.
        If key is NOT in the hash map, a new key/value pair is added.
        param key: key to be added
        param value: value to be added at key
        return : None
        modify : if key already exists, replace value
        """
        threshold = 1.0

        # resize if load factor is greater than threshold
        if self.table_load() >= threshold:
            self.resize_table(self._capacity*2)

        hashKey = self._hash_function(key) % self._capacity
        currChain = self._buckets.get_at_index(hashKey)

        keyFound = False

        # check if key is already in the hash map
        for item in currChain:
            if item.key == key:
                keyFound = True

        # if key is found remove else incr size to insert new key
        if keyFound:
            currChain.remove(key)
        else:
            self._size += 1

        currChain.insert(key, value)

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing
        key/value pairs must remain in the new hash map, and all hash table
        links must be rehashed.
        param new_capacity: capacity of new hash map
        """
        # check if new capacity is valid (> 1)
        if new_capacity < 1:
            return

        # make sure new capacity is prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        newTable = HashMap(new_capacity, self._hash_function)

        if new_capacity == 2:
            newTable._capacity = 2

        # old table -> new table
        for bucket in range(self._capacity):
            currChain = self._buckets.get_at_index(bucket)
            if currChain.length() > 0:
                for item in currChain:
                    newTable.put(item.key, item.value)

        # update self to new hash map
        self._buckets = newTable._buckets
        self._size = newTable._size
        self._capacity = newTable._capacity

    def table_load(self) -> float:
        """
        Calculate and return load factor
        load factor(lambda) = n(number of elements)/m(number of buckets)
        return float: load factor
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Return number of empty buckets in the table
        params: None
        return bucketCount: n empty buckets as int
        """
        bucketCount = 0

        # iterate through the buckets and incr for every empty bucket
        for bucket in range(self._capacity):
            if self._buckets.get_at_index(bucket).length() == 0:
                bucketCount += 1

        return bucketCount

    def get(self, key: str):
        """
        returns a value associated with the given key.
        param key: search target
        returns : key's value if found else None
        """
        # calculate the hashKey to set chain
        hashKey = self._hash_function(key) % self._capacity
        chain = self._buckets.get_at_index(hashKey)

        if chain.length() == 0:
            return None

        # iterate through the chain at the hashKey index
        # return the value if found
        for item in chain:
            if item.key == key:
                return item.value

        # if key is not in the hash map, return None
        return None

    def contains_key(self, key: str) -> bool:
        """
        searches for the arg key and returns a boolean
        param key: search target
        returns : True if found else False
        """
        # iter through map of buckets
        for bucket in range(self._capacity):
            currChain = self._buckets.get_at_index(bucket)
            # iter through chain at bucket index
            if currChain.length() > 0:
                for item in currChain:
                    # found return true else esc loop and return false
                    if item.key == key:
                        return True
        return False

    def remove(self, key: str) -> None:
        """
        searches for arg key and removes it if found
        param key: search target
        returns : None
        """
        # iter through map of buckets
        for bucket in range(self._capacity):
            currChain = self._buckets.get_at_index(bucket)
            # iter through chain at bucket index
            if currChain.length() > 0:
                for item in currChain:
                    # found remove and decr size
                    if item.key == key:
                        currChain.remove(key)
                        self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns a DynamicArray of tuples containing all the key/value pairs
        in the hash map
        return : DynamicArray of tuples(key, value)
        """
        contentsArray = DynamicArray()

        for bucket in range(self._capacity):
            currChain = self._buckets.get_at_index(bucket)
            for item in currChain:
                contentsArray.append((item.key, item.value))

        return contentsArray

    def clear(self) -> None:
        """
        clears the hash map
        """
        # remove buckets by reinitializing
        self._buckets = DynamicArray()
        self._size = 0

        # initialize new chains for each bucket
        for bucket in range(self._capacity):
            self._buckets.append(LinkedList())


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    return the mode(s) and their frequency in a tuple
    param da: DynamicArray of strings
    return : tuple of mode(s) and their frequency
    """
    # create a new map and move the contents of the dynamic array into it
    map = HashMap()
    for bucket in range(da.length()):
        key = da.get_at_index(bucket)
        if map.contains_key(key):
            map.put(key, map.get(key) + 1)
        else:
            map.put(key, 1)

    # setup variables to find mode and frequency
    frequency = 0
    keyValArray = map.get_keys_and_values()
    mode = DynamicArray()

    # find the frequency of the mode
    for pair in range(keyValArray.length()):
        _, value = keyValArray.get_at_index(pair)
        if frequency < value:
            frequency = value

    # find the modes(s) and append to mode array
    for pair in range(keyValArray.length()):
        key, value = keyValArray.get_at_index(pair)
        if value == frequency:
            mode.append(key)

    # return an array of mode's and their frequency
    return mode, frequency

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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
