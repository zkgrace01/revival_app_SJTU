# main.py
# 作者: zkgrace01
# 描述: 主程序文件，用于启动整个应用程序。


import tkinter as tk
from gui import RevivalApp

if __name__ == "__main__":
    root = tk.Tk()
    app = RevivalApp(root)
    root.mainloop()
