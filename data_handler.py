# data_handler.py


class DataHandler:
    def __init__(self):
        self.items = {}

    def add_item(self, name, desc, contact):
        if name and desc and contact:
            self.items[name] = {"description": desc, "contact": contact}
            return True
        return False

    def delete_item(self, name):
        if name in self.items:
            del self.items[name]
            return True
        return False

    def find_item(self, name):
        return self.items.get(name, None)

    def get_all_items(self):
        return self.items
