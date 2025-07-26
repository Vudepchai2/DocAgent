from typing import Dict, List, Optional
from ..models.product import Item

class Store:
    """
    ```Manage a collection of items with positional storage and retrieval capabilities.

        This class provides a structured way to store, manage, and retrieve items
        using a unique code and optional positional indexing. It is designed to
        facilitate efficient inventory management by allowing items to be added,
        updated, removed, and queried based on their unique identifiers or storage
        positions.

        Description:
            The Store class is motivated by the need for a flexible and efficient
            system to manage items, particularly in contexts where items are
            frequently added, removed, or updated. It is suitable for use in
            applications such as inventory management, resource tracking, or any
            scenario where items need to be organized and accessed efficiently.

            The class fits into larger systems by providing a robust interface for
            item management, allowing for easy integration with other components
            that require item data. It achieves its purpose by maintaining an
            internal mapping of items and their positions, ensuring quick access
            and modification capabilities.

        Parameters:
            cap (int): The maximum capacity of the store, defining how many items
            can be stored at once. Default is 20.

        Attributes:
            cap (int): The maximum number of items the store can hold.
            _data (Dict[str, Item]): A dictionary mapping item codes to their
            corresponding Item objects.
            _map (Dict[int, str]): A dictionary mapping position indices to item
            codes, facilitating positional access.

        Example:
            # Initialize a store with a capacity of 30
            store = Store(cap=30)

            # Add a new item to the store
            item = Item(code='A123', label='Sample Item', val=10.0, count=5)
            store.put(item)

            # Retrieve an item by code
            retrieved_item = store.get('A123')
            print(f"Retrieved item: {retrieved_item.label}")

            # Remove an item from the store
            store.rm('A123')
        ```
    """

    def __init__(self, cap: int=20):
        self.cap = cap
        self._data: Dict[str, Item] = {}
        self._map: Dict[int, str] = {}

    def put(self, obj: Item, pos: Optional[int]=None) -> bool:
        """
        ```Add a new item to the store or update an existing item's count.

            This method is used to insert a new item into the store or increase the count
            of an existing item if it is already present. If a valid and unoccupied position
            is specified, the item is placed there; otherwise, it is placed in the first
            available position.

            Args:
                obj (Item): The item to be added or updated in the store. Must have a unique code.
                pos (Optional[int]): The desired position index for the item. Must be a non-negative
                integer within the store's capacity. If None, the item is placed in the first available position.

            Returns:
                bool: Returns `True` if the item was successfully added or updated. Returns `False` if
                the specified position is invalid, occupied, or if no positions are available.

            Usage:
                Use this method to manage items within the store, ensuring that items are added
                or updated efficiently. This is particularly useful for maintaining stock levels
                and organizing items by position.

            Examples:
                # Example of adding a new item
                store = Store()
                new_item = Item(code='A123', label='Sample Item', val=10.0, count=5)
                success = store.put(new_item)
                if success:
                    print("New item added successfully.")
                else:
                    print("Failed to add new item.")

                # Example of updating an existing item
                existing_item = Item(code='A123', label='Sample Item', val=10.0, count=3)
                success = store.put(existing_item)
                if success:
                    print("Existing item updated successfully.")
                else:
                    print("Failed to update existing item.")
            ```
        """
        if obj.code in self._data:
            curr = self._data[obj.code]
            curr.count += obj.count
            return True
        if pos is not None:
            if pos < 0 or pos >= self.cap:
                return False
            if pos in self._map:
                return False
            self._map[pos] = obj.code
        else:
            for i in range(self.cap):
                if i not in self._map:
                    self._map[i] = obj.code
                    break
            else:
                return False
        self._data[obj.code] = obj
        return True

    def rm(self, code: str) -> bool:
        """
        ```Remove an item from the store using its unique code.

            This method deletes an item from the store's inventory based on its unique
            identifier code. It removes the item from both the data storage and the
            position mapping, ensuring that the item is no longer tracked or accessible.

            Args:
                code (str): The unique identifier code of the item to be removed.

            Returns:
                bool: Returns `True` if the item was successfully removed. Returns `False`
                if the item with the specified code does not exist in the store.

            Usage:
                Use this method to remove items that are no longer needed or available
                in the store. This is useful for maintaining an accurate inventory by
                clearing out items that are out of stock or discontinued.

            Example:
                store = Store()
                success = store.rm("A123")
                if success:
                    print("Item removed successfully.")
                else:
                    print("Item not found in the store.")
            ```
        """
        if code not in self._data:
            return False
        for k, v in list(self._map.items()):
            if v == code:
                del self._map[k]
        del self._data[code]
        return True

    def get(self, code: str) -> Optional[Item]:
        '''
        """Retrieve an item from the store using its unique code.

            This method accesses the store's internal data structure to fetch an item
            based on its unique identifier code. It is useful for obtaining the full
            item details when only the code is known.

            Args:
                code (str): The unique identifier code of the item to retrieve.

            Returns:
                Optional[Item]: The item associated with the given code if it exists;
                otherwise, None.

            Usage:
                Use this method when you need to access the details of an item stored
                in the system by providing its unique code. This is particularly useful
                in inventory management systems where item details are frequently
                accessed by their codes.

            Example:
                store = Store()
                item = store.get("item123")
                if item is not None:
                    print(f"Retrieved item: {item.label}")
                else:
                    print("Item not found.")
            """
        '''
        return self._data.get(code)

    def get_at(self, pos: int) -> Optional[Item]:
        '''
        """Retrieve an item from a specific position in the store.

            This method accesses the store's internal mapping to fetch an item
            located at a given position index. It is useful for scenarios where
            items are organized by position, and you need to retrieve an item
            based on its storage location.

            Args:
                pos (int): The position index from which to retrieve the item.
                Must be a non-negative integer within the store's capacity.

            Returns:
                Optional[Item]: The item located at the specified position if it exists;
                otherwise, None.

            Usage:
                Use this method when you need to access an item based on its
                position in the store, such as in inventory systems where items
                are stored in specific slots or locations.

            Example:
                store = Store()
                item = store.get_at(5)
                if item is not None:
                    print(f"Item at position 5: {item.label}")
                else:
                    print("No item found at position 5.")
            """
        '''
        if pos not in self._map:
            return None
        code = self._map[pos]
        return self._data.get(code)

    def ls(self) -> List[Item]:
        """
        ```Retrieve a list of all valid items currently in the store.

            This method compiles and returns a list of items that are considered valid
            based on their current state. An item is deemed valid if it has a positive
            count and, if applicable, has not expired. This function is useful for
            inventory management tasks where only active and available items need to
            be considered.

            Returns:
                List[Item]: A list of items that are currently valid and available in
                the store. The list will be empty if no valid items are found.

            Usage:
                Use this method when you need to obtain a snapshot of all items that
                are currently usable within the store. This can be particularly useful
                for generating reports, managing stock, or preparing orders.

            Example:
                store = Store()
                valid_items = store.ls()
                for item in valid_items:
                    print(f"Valid item: {item.label}, Count: {item.count}")
            ```
        """
        return [obj for obj in self._data.values() if obj.check()]

    def find(self, code: str) -> Optional[int]:
        '''
        """Locate the position of an item in the store by its code.

            This method searches for the given item code within the store's internal mapping
            and returns the position index if found. It is useful for determining the storage
            location of an item when its code is known.

            Args:
                code (str): The unique identifier code of the item to locate.

            Returns:
                Optional[int]: The position index of the item if found; otherwise, None.

            Usage:
                Use this method when you need to find the storage position of an item
                based on its code. This can be helpful for inventory management tasks
                where knowing the exact location of an item is necessary.

            Example:
                store = Store()
                item_position = store.find("item123")
                if item_position is not None:
                    print(f"Item is located at position {item_position}.")
                else:
                    print("Item not found in the store.")
            """
        '''
        for k, v in self._map.items():
            if v == code:
                return k
        return None