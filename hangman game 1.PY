import random
import tkinter as tk
from tkinter import messagebox
import sqlite3
# ---------------- Calculator Application ---------------- #
class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x400")

        self.conn = sqlite3.connect("calculator_history.db")
        self.create_table()

        self.expression = ""
        self.input_text = tk.StringVar()

        self.entry = tk.Entry(root, textvariable=self.input_text, font=("Arial", 18), justify='right')
        self.entry.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=8)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
            ('C', 5, 0), ('History', 5, 1)
        ]

        for (text, row, col) in buttons:
            button = tk.Button(root, text=text, font=("Arial", 16), padx=20, pady=20, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky='nsew')

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, expression TEXT, result TEXT)")
        self.conn.commit()

    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
        elif char == "=":
            try:
                result = str(eval(self.expression))
                self.save_to_history(self.expression, result)
                self.expression = result
            except Exception as e:
                result = "Error"
                self.expression = ""
        elif char == "History":
            self.show_history()
            return
        else:
            self.expression += char

        self.input_text.set(self.expression)

    def save_to_history(self, expression, result):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO history (expression, result) VALUES (?, ?)", (expression, result))
        self.conn.commit()

    def show_history(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM history ORDER BY id DESC LIMIT 5")
        history = cursor.fetchall()
        history_text = "\n".join([f"{exp} = {res}" for _, exp, res in history])
        messagebox.showinfo("History", history_text)
        
if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
