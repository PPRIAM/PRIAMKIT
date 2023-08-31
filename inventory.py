
class Inventory:
    def __init__(self, max_quantity=999, max_capacity=999):
        self.inventory = {}
        self.max_quantity = max_quantity
        self.max_capacity = max_capacity
        self.capacity, self.quantity = 0, 0

    def add_element(self, element, quantity):
        if self.capacity < self.max_capacity:
            if element not in self.inventory.keys():
                self.inventory[element] = quantity
                self.capacity += 1
            else:
                if self.quantity < self.max_quantity:
                    self.inventory[element] += quantity
                    self.quantity += 1

    def remove(self, element):
        self.inventory.pop(element)

    def get_quantity(self, element):
        return self.inventory[element]