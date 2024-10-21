# data_handler.py
# 作者: zkgrace01
# 描述: 负责管理物品信息的添加、删除、查找和获取所有物品的操作。


class DataHandler:
    def __init__(self):
        self.items = {}

    def add_item(self, name, desc, contact):
        """
        添加物品信息。

        参数：
        name (str): 物品名称。
        desc (str): 物品描述。
        contact (str): 联系人信息。

        返回：
        bool: 如果添加成功，返回 True，否则返回 False（当某个字段为空时）。
        """
        if name and desc and contact:
            self.items[name] = {"description": desc, "contact": contact}
            return True
        return False

    def delete_item(self, name):
        """
        根据物品名称删除物品信息。

        参数：
        name (str): 物品名称。

        返回：
        bool: 如果删除成功，返回 True；如果物品不存在，返回 False。
        """
        if name in self.items:
            del self.items[name]
            return True
        return False

    def find_item(self, name):
        """
        查找指定物品的信息。

        参数：
        name (str): 物品名称。

        返回：
        dict or None: 返回物品的详细信息（包含描述和联系人），如果物品不存在则返回 None。
        """
        return self.items.get(name, None)

    def get_all_items(self):
        """
        获取所有已存储的物品信息。

        返回：
        dict: 返回包含所有物品信息的字典。
        """
        return self.items
