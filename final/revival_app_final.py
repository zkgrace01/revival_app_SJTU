import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import Toplevel, ttk


# 设置数据库连接
def create_connection():
    conn = sqlite3.connect("items.db")
    return conn


# 初始化数据库，创建物品表、用户表、物品类型表
def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        attributes TEXT
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,       -- 外键，指向 categories 表
        name TEXT,
        description TEXT,
        address TEXT,
        phone TEXT,
        email TEXT,
        extra_1 TEXT,   -- 用于存储属性的值
        extra_2 TEXT,   -- 用于存储第二个属性的值
        extra_3 TEXT,   -- 用于存储第三个属性的值
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        address TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        approved BOOLEAN NOT NULL
    )"""
    )

    conn.commit()
    conn.close()


# 删除物品
def delete_item(item_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


# 查找物品
def search_item(category_id, keyword):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT * FROM items WHERE category_id = ? AND 
    (name LIKE ? OR description LIKE ?)
    """,
        (category_id, "%" + keyword + "%", "%" + keyword + "%"),
    )

    items = cursor.fetchall()
    conn.close()
    return items


# 管理员批准用户
def approve_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET approved = ? WHERE id = ?", (True, user_id))
    conn.commit()
    conn.close()


# 创建GUI
class ItemResurrectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("物品复活系统")

        self.admin = False  # 管理员标志

        # 登录框
        self.login_frame = Frame(root)
        self.login_frame.pack()

        self.username_label = Label(self.login_frame, text="用户名")
        self.username_label.grid(row=0, column=0)
        self.username_entry = Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = Label(self.login_frame, text="密码")
        self.password_label.grid(row=1, column=0)
        self.password_entry = Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = Button(self.login_frame, text="登录", command=self.login)
        self.login_button.grid(row=2, columnspan=2)

        # 注册按钮
        self.register_button = Button(
            self.login_frame, text="注册", command=self.register_ui
        )
        self.register_button.grid(row=3, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # 进行用户验证（假设管理员用户名为 admin，密码为 admin）
        if username == "admin" and password == "admin":
            self.admin = True
            self.login_frame.destroy()
            self.create_admin_ui()
            return

        # 对于普通用户，检查用户名和密码是否匹配
        conn = create_connection()
        cursor = conn.cursor()

        # 查询用户信息，验证用户名和密码
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (username, password)
        )
        user = cursor.fetchone()

        if user:
            # 检查该用户是否已经被管理员批准
            if user[6]:  # 假设 approved 字段是第6列，0-未批准，1-已批准
                self.admin = False
                self.login_frame.destroy()
                self.create_user_ui(username)  # 创建普通用户界面
            else:
                self.show_message("登录失败", "您的账户还没有被管理员批准。")
        else:
            self.show_message("登录失败", "用户名或密码错误。")

        conn.close()

    def register_ui(self):
        # 普通用户注册窗口
        self.register_window = Toplevel(self.root)
        self.register_window.title("用户注册")

        # 设置新窗口的大小
        # self.register_window.geometry("400x400")

        self.register_username_label = Label(self.register_window, text="用户名")
        self.register_username_label.grid(row=0, column=0)
        self.register_username_entry = Entry(self.register_window)
        self.register_username_entry.grid(row=0, column=1)

        self.register_password_label = Label(self.register_window, text="密码")
        self.register_password_label.grid(row=1, column=0)
        self.register_password_entry = Entry(self.register_window, show="*")
        self.register_password_entry.grid(row=1, column=1)

        self.register_address_label = Label(self.register_window, text="住址")
        self.register_address_label.grid(row=2, column=0)
        self.register_address_entry = Entry(self.register_window)
        self.register_address_entry.grid(row=2, column=1)

        self.register_phone_label = Label(self.register_window, text="手机号")
        self.register_phone_label.grid(row=3, column=0)
        self.register_phone_entry = Entry(self.register_window)
        self.register_phone_entry.grid(row=3, column=1)

        self.register_email_label = Label(self.register_window, text="邮箱")
        self.register_email_label.grid(row=4, column=0)
        self.register_email_entry = Entry(self.register_window)
        self.register_email_entry.grid(row=4, column=1)

        self.register_button = Button(
            self.register_window, text="注册", command=self.register_user
        )
        self.register_button.grid(row=5, columnspan=2)

    def register_user(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        address = self.register_address_entry.get()
        phone = self.register_phone_entry.get()
        email = self.register_email_entry.get()

        if not username or not password or not address or not phone or not email:
            messagebox.showwarning("输入不完整", "所有字段不能为空。")
            return

        # 将用户注册信息保存到数据库（需要等待管理员批准）
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (username, password, address, phone, email, approved) 
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (username, password, address, phone, email, False),
        )  # 默认未批准
        conn.commit()
        conn.close()

        self.show_message("注册成功", "注册成功，等待管理员批准。")
        self.register_window.destroy()  # 关闭注册窗口

    def create_admin_ui(self):
        self.admin_frame = Frame(self.root)
        self.admin_frame.pack()

        self.add_item_button = Button(
            self.admin_frame, text="添加物品", command=self.add_item_ui
        )
        self.add_item_button.pack()

        self.add_category_button = Button(
            self.admin_frame, text="添加物品类型", command=self.add_category_ui
        )
        self.add_category_button.pack()

        # 在管理员界面添加修改物品类型按钮
        self.modify_category_button = Button(
            self.admin_frame, text="修改物品类型", command=self.modify_category_ui
        )
        self.modify_category_button.pack()

        self.view_items_button = Button(
            self.admin_frame, text="查看物品列表", command=self.view_items
        )
        self.view_items_button.pack()

        # 在管理员界面中添加“删除物品”按钮
        self.delete_items_button = Button(
            self.admin_frame, text="删除物品", command=self.delete_items_ui
        )
        self.delete_items_button.pack()

        self.approve_user_button = Button(
            self.admin_frame, text="批准用户", command=self.approve_user_ui
        )
        self.approve_user_button.pack()

        self.logout_button = Button(
            self.admin_frame, text="退出登录", command=self.logout_admin
        )
        self.logout_button.pack()

    # 批准用户界面

    def approve_user_ui(self):
        self.approve_user_window = Toplevel(self.root)
        self.approve_user_window.title("批准用户")

        # 获取所有待批准的用户
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE approved = ?", (False,))
        users = cursor.fetchall()
        conn.close()

        if not users:
            messagebox.showinfo("无待批准用户", "没有待批准的用户。")
            return

        # 用户列表显示
        self.user_listbox = Listbox(self.approve_user_window, height=10, width=50)
        self.user_listbox.pack()

        for user in users:
            self.user_listbox.insert(END, f"{user[0]}: {user[1]}")

        # 批准按钮
        self.approve_button = Button(
            self.approve_user_window, text="批准", command=self.approve_user
        )
        self.approve_button.pack()

    # 批准用户功能实现
    def approve_user(self):
        selected_user_index = self.user_listbox.curselection()

        if not selected_user_index:
            messagebox.showwarning("选择用户", "请选择一个用户进行批准。")
            return

        selected_user = self.user_listbox.get(selected_user_index)
        user_id = int(selected_user.split(":")[0])  # 提取用户ID

        # 更新用户批准状态
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET approved = ? WHERE id = ?", (True, user_id))
        conn.commit()
        conn.close()

        self.show_message("成功", "用户已批准")
        self.approve_user_window.destroy()  # 关闭批准用户窗口

    def add_category_ui(self):
        self.category_window = Toplevel(self.root)
        self.category_window.title("添加物品类型")

        self.category_name_label = Label(self.category_window, text="物品类型名称")
        self.category_name_label.grid(row=0, column=0)
        self.category_name_entry = Entry(self.category_window)
        self.category_name_entry.grid(row=0, column=1)

        self.category_attributes_label = Label(
            self.category_window, text="物品属性(分号分割)"
        )
        self.category_attributes_label.grid(row=1, column=0)
        self.category_attributes_entry = Entry(self.category_window)
        self.category_attributes_entry.grid(row=1, column=1)

        self.add_category_button = Button(
            self.category_window, text="添加", command=self.add_category
        )
        self.add_category_button.grid(row=2, columnspan=2)

    def add_category(self):
        category_name = self.category_name_entry.get()
        category_attributes = (
            self.category_attributes_entry.get() or None
        )  # 如果没有输入属性，则为 None

        # 将物品类型和属性保存到数据库
        conn = create_connection()
        cursor = conn.cursor()

        # 插入物品类型到 categories 表
        cursor.execute(
            "INSERT INTO categories (name, attributes) VALUES (?, ?)",
            (category_name, category_attributes),
        )
        conn.commit()
        conn.close()

        self.category_window.destroy()  # 关闭窗口
        self.show_message("添加成功", "物品类型已成功添加。")

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    # 添加物品界面

    def add_item_ui(self):
        self.item_window = Toplevel(self.root)
        self.item_window.title("添加物品")

        # 选择物品类型
        self.category_label = Label(self.item_window, text="选择物品类型")
        self.category_label.grid(row=0, column=0)

        # 获取所有物品类别
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        conn.close()

        self.category_var = StringVar(self.item_window)
        self.category_var.set(categories[0][1])  # 默认选择第一个类别

        # 物品种类选择框
        self.category_menu = OptionMenu(
            self.item_window,
            self.category_var,
            *[category[1] for category in categories],
            command=self.on_category_change,  # 监听物品类别变化
        )
        self.category_menu.grid(row=0, column=1)

        # 物品信息输入框
        self.name_label = Label(self.item_window, text="物品名称")
        self.name_label.grid(row=1, column=0)
        self.name_entry = Entry(self.item_window)
        self.name_entry.grid(row=1, column=1)

        self.description_label = Label(self.item_window, text="物品描述")
        self.description_label.grid(row=2, column=0)
        self.description_entry = Entry(self.item_window)
        self.description_entry.grid(row=2, column=1)

        self.address_label = Label(self.item_window, text="物品地址")
        self.address_label.grid(row=3, column=0)
        self.address_entry = Entry(self.item_window)
        self.address_entry.grid(row=3, column=1)

        self.phone_label = Label(self.item_window, text="联系人手机")
        self.phone_label.grid(row=4, column=0)
        self.phone_entry = Entry(self.item_window)
        self.phone_entry.grid(row=4, column=1)

        self.email_label = Label(self.item_window, text="联系人邮箱")
        self.email_label.grid(row=5, column=0)
        self.email_entry = Entry(self.item_window)
        self.email_entry.grid(row=5, column=1)

        # 动态加载额外的属性输入框
        self.extra_entries = []  # 用来保存生成的额外输入框
        self.load_extra_attributes()  # 初始化时加载属性输入框

        # 添加物品按钮
        self.add_item_button = Button(
            self.item_window, text="添加物品", command=self.add_item
        )
        self.add_item_button.grid(row=10, columnspan=2)

    def load_extra_attributes(self):
        # 获取当前选定的类别
        category_name = self.category_var.get()

        # 删除旧的额外属性输入框
        for entry in self.extra_entries:
            entry[0].destroy()  # 删除label
            entry[1].destroy()  # 删除entry
        self.extra_entries.clear()  # 清空列表

        # 获取类别特定的字段值
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT attributes FROM categories WHERE name = ?", (category_name,)
        )
        category_data = cursor.fetchone()
        conn.close()

        if category_data and category_data[0]:
            attributes = category_data[0].split(";")  # 按分号拆分属性

            # 动态创建额外的属性输入框
            for i, attribute in enumerate(attributes, start=6):  # 从第6行开始填入
                label = Label(self.item_window, text=f"{attribute} (可选)")
                label.grid(row=i, column=0)
                entry = Entry(self.item_window)
                entry.grid(row=i, column=1)
                self.extra_entries.append((label, entry))  # 保存label和entry

    def add_item(self):
        # 获取通用信息
        category_name = self.category_var.get()
        name = self.name_entry.get()
        description = self.description_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        # 获取额外的属性值
        extra_values = [entry[1].get() or None for entry in self.extra_entries]

        # 保证 extra_values 长度为 3，缺少的值用 None 填充
        while len(extra_values) < 3:
            extra_values.append(None)

        # 保存物品信息
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO items (category_id, name, description, address, phone, email, extra_1, extra_2, extra_3)
            VALUES ((SELECT id FROM categories WHERE name = ?), ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                category_name,
                name,
                description,
                address,
                phone,
                email,
                *extra_values,  # 动态插入额外属性的值
            ),
        )

        conn.commit()
        conn.close()

        self.item_window.destroy()  # 关闭添加物品窗口
        self.show_message("物品添加成功", "物品已成功添加。")

    def on_category_change(self, selected_category):
        # 当物品种类发生变化时，重新加载额外的属性输入框
        self.load_extra_attributes()

        # 修改物品类型界面

    def modify_category_ui(self):
        self.modify_category_window = Toplevel(self.root)
        self.modify_category_window.title("修改物品类型")

        # 设置新窗口的大小
        # self.modify_category_window.geometry("400x300")

        # 获取所有物品类别
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        conn.close()

        if not categories:
            messagebox.showinfo("无物品类型", "没有物品类型可以修改。")
            return

        # 选择物品类型
        self.category_label = Label(self.modify_category_window, text="选择物品类型")
        self.category_label.grid(row=0, column=0)

        self.category_var = StringVar(self.modify_category_window)
        self.category_var.set(categories[0][1])  # 默认选择第一个类别

        self.category_menu = OptionMenu(
            self.modify_category_window,
            self.category_var,
            *[category[1] for category in categories],
        )
        self.category_menu.grid(row=0, column=1)

        # 物品类型名称输入框
        self.category_name_label = Label(
            self.modify_category_window, text="物品类型名称"
        )
        self.category_name_label.grid(row=1, column=0)
        self.category_name_entry = Entry(self.modify_category_window)
        self.category_name_entry.grid(row=1, column=1)

        # 物品类型属性输入框
        self.category_attributes_label = Label(
            self.modify_category_window, text="物品属性"
        )
        self.category_attributes_label.grid(row=2, column=0)
        self.category_attributes_entry = Entry(self.modify_category_window)
        self.category_attributes_entry.grid(row=2, column=1)

        # 确定修改按钮
        self.modify_category_button = Button(
            self.modify_category_window, text="修改", command=self.modify_category
        )
        self.modify_category_button.grid(row=3, columnspan=2)

    # 修改物品类型功能实现
    def modify_category(self):
        category_name = self.category_var.get()
        new_name = self.category_name_entry.get()
        new_attributes = self.category_attributes_entry.get()

        if not new_name or not new_attributes:
            messagebox.showwarning("输入不完整", "物品类型名称和属性不能为空。")
            return

        # 更新物品类型的名称和属性
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE categories 
            SET name = ?, attributes = ? 
            WHERE name = ?
        """,
            (new_name, new_attributes, category_name),
        )
        conn.commit()
        conn.close()

        self.show_message("成功", "物品类型已修改")
        self.modify_category_window.destroy()  # 关闭修改物品类型窗口

    def create_user_ui(self, username):
        # 创建用户界面
        self.user_frame = Frame(self.root)
        self.user_frame.pack()

        welcome_label = Label(self.user_frame, text=f"欢迎 {username} 登录")
        welcome_label.pack()

        # 物品添加
        self.add_item_button = Button(
            self.user_frame, text="添加物品", command=self.add_item_ui
        )
        self.add_item_button.pack()

        # 物品搜索
        self.search_item_button = Button(
            self.user_frame, text="搜索物品", command=self.search_item_ui
        )
        self.search_item_button.pack()

        self.view_items_button = Button(
            self.user_frame, text="查看物品列表", command=self.view_items
        )
        self.view_items_button.pack()

        # 退出登录
        logout_button = Button(
            self.user_frame, text="退出登录", command=self.logout_user
        )
        logout_button.pack()

    def search_item_ui(self):
        # 创建一个新的窗口来搜索物品
        self.search_window = Toplevel(self.root)
        self.search_window.title("搜索物品")

        # 选择物品类别
        self.category_label = Label(self.search_window, text="选择物品类别")
        self.category_label.pack(padx=10, pady=5)

        # 获取所有物品类别
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM categories")
        categories = cursor.fetchall()
        conn.close()

        self.category_var = StringVar(self.search_window)
        self.category_var.set(categories[0][0])  # 默认选择第一个类别

        self.category_menu = OptionMenu(
            self.search_window,
            self.category_var,
            *[category[0] for category in categories],
        )
        self.category_menu.pack(padx=10, pady=5)

        # 输入关键字
        self.keyword_label = Label(self.search_window, text="输入关键字")
        self.keyword_label.pack(padx=10, pady=5)

        self.keyword_entry = Entry(self.search_window)
        self.keyword_entry.pack(padx=10, pady=5)

        # 搜索按钮
        self.search_button = Button(
            self.search_window, text="搜索", command=self.search_item
        )
        self.search_button.pack(padx=10, pady=20)

        # 显示搜索结果的Treeview
        self.result_tree_frame = Frame(self.search_window)
        self.result_tree_frame.pack(fill="both", expand=True)

        # 初始化Treeview控件
        self.result_tree = ttk.Treeview(
            self.result_tree_frame,
            columns=(
                "ID",
                "Name",
                "Description",
                "Category",
                "Phone",
                "Email",
                "Extra 1",
                "Extra 2",
                "Extra 3",
            ),
            show="headings",
        )

        # 设置Treeview列头
        self.result_tree.heading("ID", text="物品ID")
        self.result_tree.heading("Name", text="物品名称")
        self.result_tree.heading("Description", text="物品描述")
        self.result_tree.heading("Category", text="物品类别")
        self.result_tree.heading("Phone", text="联系人手机")
        self.result_tree.heading("Email", text="联系人邮箱")
        self.result_tree.heading("Extra 1", text="附加属性 1")
        self.result_tree.heading("Extra 2", text="附加属性 2")
        self.result_tree.heading("Extra 3", text="附加属性 3")

        # 设置列宽
        self.result_tree.column("ID", width=50)
        self.result_tree.column("Name", width=150)
        self.result_tree.column("Description", width=200)
        self.result_tree.column("Category", width=100)
        self.result_tree.column("Phone", width=100)
        self.result_tree.column("Email", width=150)
        self.result_tree.column("Extra 1", width=100)
        self.result_tree.column("Extra 2", width=100)
        self.result_tree.column("Extra 3", width=100)

        self.result_tree.pack(fill="both", expand=True)

    def search_item(self):
        # 获取用户输入的类别和关键字
        category_name = self.category_var.get()
        keyword = self.keyword_entry.get().strip()

        # 构建查询语句，使用JOIN来获取类别名称
        query = """
            SELECT i.id, i.name, i.description, c.name AS category, i.phone, i.email, i.extra_1, i.extra_2, i.extra_3 
            FROM items i
            JOIN categories c ON i.category_id = c.id
            WHERE c.name = ? 
            AND (i.name LIKE ? OR i.description LIKE ?)
        """
        search_term = f"%{keyword}%"  # 在名称和描述中查找包含关键字的物品

        # 执行查询
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(query, (category_name, search_term, search_term))
        items = cursor.fetchall()
        conn.close()

        # 清空之前的搜索结果
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        # 将搜索结果插入到Treeview中
        for item in items:
            self.result_tree.insert("", "end", values=item)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def logout_admin(self):
        # 退出登录，返回登录界面
        self.admin = False
        self.admin_frame.destroy()  # 销毁管理员面板
        self.__init__(self.root)  # 重新初始化登录界面

    def logout_user(self):
        self.user_frame.destroy()
        self.__init__(self.root)  # 重新初始化登录界面

    # 获取所有物品
    def view_items(self):
        # 创建一个新的窗口来展示所有物品
        self.view_window = Toplevel(self.root)
        self.view_window.title("所有物品列表")

        # 创建Treeview表格控件
        self.tree = ttk.Treeview(
            self.view_window,
            columns=(
                "ID",
                "Name",
                "Description",
                "Category",
                "Phone",
                "Email",
                "Extra 1",
                "Extra 2",
                "Extra 3",
            ),
            show="headings",
        )

        # 定义列头
        self.tree.heading("ID", text="物品ID")
        self.tree.heading("Name", text="物品名称")
        self.tree.heading("Description", text="物品描述")
        self.tree.heading("Category", text="物品类别")
        self.tree.heading("Phone", text="联系人手机")
        self.tree.heading("Email", text="联系人邮箱")
        self.tree.heading("Extra 1", text="附加属性 1")
        self.tree.heading("Extra 2", text="附加属性 2")
        self.tree.heading("Extra 3", text="附加属性 3")

        # 设置列宽
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Description", width=200)
        self.tree.column("Category", width=100)
        self.tree.column("Phone", width=100)
        self.tree.column("Email", width=150)
        self.tree.column("Extra 1", width=100)
        self.tree.column("Extra 2", width=100)
        self.tree.column("Extra 3", width=100)

        self.tree.grid(row=0, column=0, sticky="nsew")

        # 获取物品数据并插入到Treeview
        self.populate_items()

    def populate_items(self):
        # 从数据库获取所有物品信息
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT items.id, items.name, items.description, categories.name, items.phone, items.email, items.extra_1, items.extra_2, items.extra_3 FROM items JOIN categories ON items.category_id = categories.id"
        )
        items = cursor.fetchall()
        conn.close()

        # 插入物品信息到Treeview
        for item in items:
            self.tree.insert("", "end", values=item)

    def delete_items_ui(self):
        # 创建一个新的窗口显示所有物品
        self.delete_window = Toplevel(self.root)
        self.delete_window.title("删除物品")

        # 创建一个 Treeview 控件显示所有物品
        self.tree = ttk.Treeview(
            self.delete_window,
            columns=(
                "ID",
                "Name",
                "Description",
                "Category",
                "Phone",
                "Email",
                "Extra 1",
                "Extra 2",
                "Extra 3",
            ),
            show="headings",
        )

        # 定义列头
        self.tree.heading("ID", text="物品ID")
        self.tree.heading("Name", text="物品名称")
        self.tree.heading("Description", text="物品描述")
        self.tree.heading("Category", text="物品类别")
        self.tree.heading("Phone", text="联系人手机")
        self.tree.heading("Email", text="联系人邮箱")
        self.tree.heading("Extra 1", text="附加属性 1")
        self.tree.heading("Extra 2", text="附加属性 2")
        self.tree.heading("Extra 3", text="附加属性 3")

        # 设置列宽
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Description", width=200)
        self.tree.column("Category", width=100)
        self.tree.column("Phone", width=100)
        self.tree.column("Email", width=150)
        self.tree.column("Extra 1", width=100)
        self.tree.column("Extra 2", width=100)
        self.tree.column("Extra 3", width=100)

        # 创建删除按钮列
        self.tree["columns"] += ("Delete",)
        self.tree.heading("Delete", text="操作")

        # 获取所有物品并填充到 Treeview 中
        self.populate_items_for_deletion()

        # 使窗口中的控件自适应
        self.tree.pack(fill="both", expand=True)

    def populate_items_for_deletion(self):
        # 获取所有物品
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT i.id, i.name, i.description, c.name AS category, i.phone, i.email, i.extra_1, i.extra_2, i.extra_3
            FROM items i
            JOIN categories c ON i.category_id = c.id
        """
        )
        items = cursor.fetchall()
        conn.close()

        # 清空之前的列表
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 将物品数据插入到 Treeview 中，并为每个物品添加删除按钮
        for item in items:
            item_id = item[0]
            self.tree.insert("", "end", values=item + ("删除",), iid=item_id)

        # 为每个物品行添加删除按钮
        for item in items:
            item_id = item[0]
            # 使用lambda函数将点击事件绑定到确认删除方法
            self.tree.bind(
                "<ButtonRelease-1>",
                lambda event, iid=item_id: self.confirm_delete_item(iid),
            )

    def confirm_delete_item(self, item_id):
        # 弹出确认框
        result = messagebox.askyesno("确认删除", "您确定要删除此物品吗？")

        if result:
            # 如果确认删除，执行删除操作
            self.delete_item(item_id)
            self.show_message("删除成功", "物品已成功删除。")
        else:
            # 如果取消删除，不做任何操作
            self.show_message("取消删除", "物品删除已取消。")

    def delete_item(self, item_id):
        # 删除物品
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()

        # 刷新物品列表
        self.populate_items_for_deletion()

        # 显示删除成功提示
        self.show_message("删除成功", "物品已成功删除。")


# 启动程序
if __name__ == "__main__":
    initialize_db()
    root = Tk()
    app = ItemResurrectionApp(root)
    root.mainloop()
