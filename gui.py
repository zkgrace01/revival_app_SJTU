# gui.py

import tkinter as tk
from tkinter import messagebox
from data_handler import DataHandler
import config


class RevivalApp:
    def __init__(self, root):
        self.root = root
        self.root.title(config.APP_TITLE)
        self.data_handler = DataHandler()

        # 界面设计
        self.setup_ui()

    def setup_ui(self):
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
        name = self.item_name_entry.get()
        desc = self.item_desc_entry.get()
        contact = self.contact_info_entry.get()

        if self.data_handler.add_item(name, desc, contact):
            messagebox.showinfo("成功", "物品已添加!")
            self.clear_entries()
        else:
            messagebox.showwarning("输入错误", "请填写所有字段！")

    def delete_item(self):
        name = self.item_name_entry.get()

        if self.data_handler.delete_item(name):
            messagebox.showinfo("成功", f"物品 {name} 已删除!")
        else:
            messagebox.showwarning("错误", f"物品 {name} 不存在！")
        self.clear_entries()

    def show_items(self):
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
        self.item_name_entry.delete(0, tk.END)
        self.item_desc_entry.delete(0, tk.END)
        self.contact_info_entry.delete(0, tk.END)
