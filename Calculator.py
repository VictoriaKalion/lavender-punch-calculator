import tkinter as tk
from tkinter import messagebox
import math
import os
from PIL import Image, ImageTk

class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Лавандовый пунш!")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        self.images = {}
        self.current_input = ""
        self.result_var = tk.StringVar()

        self.colors = {
            'text_dark': '#4A3F6B'
        }

        self.images_dir = os.path.join(os.path.dirname(__file__), 'images')

        self.load_images()
        self.create_widgets()

    def load_images(self):
        files_to_load = {
            'background': 'background.png',
            'button': 'button.png',
            'entry_bg': 'entry_background.png'
        }

        for key, filename in files_to_load.items():
            filepath = os.path.join(self.images_dir, filename)
            if os.path.exists(filepath):
                try:
                    image = Image.open(filepath)

                    if image.mode in ('RGB', 'RGBA'):
                        image = image.convert('RGBA')
                        datas = image.getdata()

                        new_data = []
                        for item in datas:
                            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                                new_data.append((255, 255, 255, 0))
                            else:
                                new_data.append(item)

                        image.putdata(new_data)

                    if key == 'background':
                        image = image.resize((400, 550), Image.Resampling.LANCZOS)
                    elif key == 'entry_bg':
                        image = image.resize((360, 50), Image.Resampling.LANCZOS)
                    else:
                        image = image.resize((70, 60), Image.Resampling.LANCZOS)

                    self.images[key] = ImageTk.PhotoImage(image)

                except Exception as e:
                    print(f"Ошибка загрузки {filename}: {e}")

    def create_widgets(self):
        if 'background' in self.images:
            self.bg_canvas = tk.Canvas(self.root, width=400, height=550, highlightthickness=0)
            self.bg_canvas.pack(fill='both', expand=True)
            self.bg_canvas.create_image(0, 0, image=self.images['background'], anchor='nw')
            container = self.bg_canvas

            title_label = tk.Label(
                container,
                text="Лавандовый пунш!",
                font=('Georgia', 16, 'bold'),
                fg=self.colors['text_dark'],
                pady=10
            )
            container.create_window(200, 40, window=title_label, width=380, height=40)

            if 'entry_bg' in self.images:
                entry_canvas = tk.Canvas(
                    container,
                    width=360,
                    height=50,
                    highlightthickness=0
                )
                container.create_window(200, 100, window=entry_canvas, width=360, height=50)
                entry_canvas.create_image(0, 0, image=self.images['entry_bg'], anchor='nw')

                self.entry = tk.Entry(
                    container,
                    textvariable=self.result_var,
                    font=('Georgia', 18, 'bold'),
                    justify='right',
                    state='readonly',
                    bg='#FFFFFF',
                    fg=self.colors['text_dark'],
                    bd=0,
                    relief='flat',
                    insertbackground=self.colors['text_dark']
                )
                entry_canvas.create_window(180, 25, window=self.entry, width=340, height=40)
            else:
                self.entry = tk.Entry(
                    container,
                    textvariable=self.result_var,
                    font=('Georgia', 18, 'bold'),
                    justify='right',
                    state='readonly',
                    bg='#FFFFFF',
                    fg=self.colors['text_dark'],
                    bd=2,
                    relief='solid'
                )
                container.create_window(200, 100, window=self.entry, width=360, height=50)

            buttons_frame = tk.Frame(container)
            container.create_window(200, 350, window=buttons_frame, width=360, height=350)

        else:
            # Если нет фонового изображения
            container = tk.Frame(self.root)
            container.pack(fill='both', expand=True)

            title_label = tk.Label(
                container,
                text="Лавандовый пунш",
                font=('Georgia', 16, 'bold'),
                fg=self.colors['text_dark'],
                pady=10
            )
            title_label.pack(fill='x', padx=10, pady=10)

            self.entry = tk.Entry(
                container,
                textvariable=self.result_var,
                font=('Georgia', 18, 'bold'),
                justify='right',
                state='readonly',
                bg='#FFFFFF',
                fg=self.colors['text_dark'],
                bd=2,
                relief='solid'
            )
            self.entry.pack(pady=20, fill='x', padx=20, ipady=10)

            buttons_frame = tk.Frame(container)
            buttons_frame.pack(pady=20, fill='both', expand=True, padx=20)

        self.create_buttons_grid(buttons_frame)

    def create_buttons_grid(self, parent):
        buttons = [
            ['7', '8', '9', '/', '√'],
            ['4', '5', '6', '*', '²'],
            ['1', '2', '3', '-', 'C'],
            ['0', '.', '=', '+', '⌫']
        ]

        text_color = self.colors['text_dark']

        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text:
                    if 'button' in self.images:
                        btn = tk.Button(
                            parent,
                            text=text,
                            image=self.images['button'],
                            compound='center',
                            font=('Georgia', 14, 'bold'),
                            fg=text_color,
                            command=lambda t=text: self.button_click(t),
                            relief='flat',
                            bd=0
                        )
                    else:
                        btn = tk.Button(
                            parent,
                            text=text,
                            font=('Georgia', 14, 'bold'),
                            bg='#C4B7D6',
                            fg=text_color,
                            command=lambda t=text: self.button_click(t),
                            relief='raised',
                            bd=2
                        )

                    btn.grid(
                        row=i,
                        column=j,
                        sticky='nsew',
                        padx=2,
                        pady=2,
                        ipadx=8,
                        ipady=8
                    )

        for i in range(4):
            parent.grid_rowconfigure(i, weight=1)
        for j in range(5):
            parent.grid_columnconfigure(j, weight=1)

    def button_click(self, value):
        try:
            if value.isdigit() or value == '.':
                if value == '.' and '.' in self.current_input:
                    return
                self.current_input += value
                self.result_var.set(self.current_input)

            elif value in ['+', '-', '*', '/']:
                if self.current_input and self.current_input[-1] not in ['+', '-', '*', '/']:
                    self.current_input += value
                    self.result_var.set(self.current_input)

            elif value == '√':
                if self.current_input:
                    num = float(self.current_input)
                    if num < 0:
                        messagebox.showerror("Оо-ой!", "Нельзя извлечь корень из отрицательного числа, малыш!")
                        return
                    result = math.sqrt(num)
                    self.current_input = str(result)
                    self.result_var.set(self.current_input)

            elif value == '²':
                if self.current_input:
                    num = float(self.current_input)
                    result = num ** 2
                    self.current_input = str(result)
                    self.result_var.set(self.current_input)

            elif value == 'C':
                self.current_input = ""
                self.result_var.set("")

            elif value == '⌫':
                self.current_input = self.current_input[:-1]
                self.result_var.set(self.current_input)

            elif value == '=':
                if self.current_input:
                    if '/0' in self.current_input.replace(' ', ''):
                        messagebox.showerror("Аа-ай", "Котик, не дели на ноль!")
                        self.current_input = ""
                        self.result_var.set("")
                        return

                    result = eval(self.current_input)
                    self.current_input = str(result)
                    self.result_var.set(self.current_input)

        except ZeroDivisionError:
            messagebox.showerror("Упс!", "Делишь на ноль, пупсик!")
            self.current_input = ""
            self.result_var.set("")
        except Exception as e:
            messagebox.showerror("Ай!", f"Плохое выражение: {e}")
            self.current_input = ""
            self.result_var.set("")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()