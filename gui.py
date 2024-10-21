# gui.py
# 作者: zkgrace01
# 描述: 创建物品复活软件的图形用户界面，处理用户的输入和交互。

import tkinter as tk
from tkinter import messagebox
from data_handler import DataHandler
import config


class RevivalApp:
    def __init__(self, root):
        """
        初始化应用程序界面。

        参数：
        root (Tk): tkinter 根窗口实例。
        """
        self.root = root
        self.root.title(config.APP_TITLE)
        self.data_handler = DataHandler()

        # 界面设计
        self.setup_ui()

    def setup_ui(self):
        """
        设置用户界面，包括输入字段和操作按钮。
        """
        # 标题
        title_label = tk.Label(self.root, text=config.APP_TITLE, font=config.TITLE_FONT)
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # 物品名称输入
        self.item_name_label = tk.Label(self.root, text="物品名称:")
        self.item_name_label.grid(row=1, column=0, padx=10, pady=5)
        self.item_name_entry = tk.Entry(self.root)
        self.item_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # 物品描述输入
        self.item_desc_label = tk.Label(self.root, text="物品描述:")
        self.item_desc_label.grid(row=2, column=0, padx=10, pady=5)
        self.item_desc_entry = tk.Entry(self.root)
        self.item_desc_entry.grid(row=2, column=1, padx=10, pady=5)

        # 联系人信息输入
        self.contact_info_label = tk.Label(self.root, text="联系人信息:")
        self.contact_info_label.grid(row=3, column=0, padx=10, pady=5)
        self.contact_info_entry = tk.Entry(self.root)
        self.contact_info_entry.grid(row=3, column=1, padx=10, pady=5)

        # 按钮：添加物品
        add_button = tk.Button(self.root, text="添加物品", command=self.add_item)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # 按钮：删除物品
        delete_button = tk.Button(self.root, text="删除物品", command=self.delete_item)
        delete_button.grid(row=5, column=0, columnspan=2, pady=10)

        # 按钮：显示所有物品
        show_button = tk.Button(self.root, text="显示所有物品", command=self.show_items)
        show_button.grid(row=6, column=0, columnspan=2, pady=10)

        # 按钮：查找物品
        find_button = tk.Button(self.root, text="查找物品", command=self.find_item)
        find_button.grid(row=7, column=0, columnspan=2, pady=10)

    def add_item(self):
        """
        从输入框中获取物品信息，调用 DataHandler 添加物品信息。

        输入：
        从 item_name_entry、item_desc_entry、contact_info_entry 获取输入数据。

        输出：
        显示成功或失败的消息框。
        """
        name = self.item_name_entry.get()
        desc = self.item_desc_entry.get()
        contact = self.contact_info_entry.get()

        if self.data_handler.add_item(name, desc, contact):
            messagebox.showinfo("成功", "物品已添加!")
            self.clear_entries()
        else:
            messagebox.showwarning("输入错误", "请填写所有字段！")

    def delete_item(self):
        """
        根据输入的物品名称，删除物品信息。

        输入：
        从 item_name_entry 获取物品名称。

        输出：
        显示成功或失败的消息框。
        """
        name = self.item_name_entry.get()

        if self.data_handler.delete_item(name):
            messagebox.showinfo("成功", f"物品 {name} 已删除!")
        else:
            messagebox.showwarning("错误", f"物品 {name} 不存在！")
        self.clear_entries()

    def show_items(self):
        """
        显示所有存储的物品信息。
        """
        items = self.data_handler.get_all_items()
        if items:
            items_info = "\n".join(
                [
                    f"{name}: {info['description']} (联系人: {info['contact']})"
                    for name, info in items.items()
                ]
            )
            messagebox.showinfo("物品列表", items_info)
        else:
            messagebox.showinfo("物品列表", "没有可显示的物品信息。")

    def find_item(self):
        """
        获取物品名称并通过 DataHandler 类查找物品信息。
        显示物品详细信息或未找到物品的错误提示框。
        """
        name = self.item_name_entry.get()
        item_info = self.data_handler.find_item(name)

        if item_info:
            messagebox.showinfo(
                "物品信息",
                f"物品: {name}\n描述: {item_info['description']}\n联系人: {item_info['contact']}",
            )
        else:
            messagebox.showwarning("错误", f"物品 {name} 不存在！")
        self.clear_entries()

    def clear_entries(self):
        """
        清空所有输入字段（物品名称、描述和联系人）。
        """
        self.item_name_entry.delete(0, tk.END)
        self.item_desc_entry.delete(0, tk.END)
        self.contact_info_entry.delete(0, tk.END)
