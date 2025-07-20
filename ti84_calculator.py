import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from calc_engine import evaluate_expression

class TI84Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TI-84 Graphing Calculator")
        self.root.geometry("400x600")
        self.root.configure(bg='#2C3E50')
        self.root.resizable(False, False)
        
        self.current_input = ""
        self.result = 0
        self.memory = []
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_display(main_frame)
        self.create_buttons(main_frame)
        
    def create_display(self, parent):
        display_frame = tk.Frame(parent, bg='#34495E', relief=tk.SUNKEN, bd=3)
        display_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.display = tk.Text(display_frame, height=8, width=40, bg='#1E3A8A', fg='white', 
                              font=('Courier', 12), state=tk.DISABLED, wrap=tk.WORD)
        self.display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        input_frame = tk.Frame(parent, bg='#2C3E50')
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.input_display = tk.Entry(input_frame, font=('Courier', 14), bg='white', 
                                     fg='black', justify='right', state='readonly')
        self.input_display.pack(fill=tk.X, ipady=5)
        
        self.update_input_display("")
        
    def create_buttons(self, parent):
        button_frame = tk.Frame(parent, bg='#2C3E50')
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        buttons = [
            ['QUIT', 'MODE', 'DEL', 'CLEAR'],
            ['X²', 'LOG', 'LN', 'SIN'],
            ['COS', 'TAN', '^', 'EE'],
            ['(', ')', '÷', '×'],
            ['7', '8', '9', '-'],
            ['4', '5', '6', '+'],
            ['1', '2', '3', 'ENTER'],
            ['0', '(-)', '.', 'GRAPH']
        ]
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text == 'ENTER':
                    btn = tk.Button(button_frame, text=text, command=lambda t=text: self.button_click(t),
                                   bg='#3498DB', fg='white', font=('Arial', 10, 'bold'),
                                   relief=tk.RAISED, bd=2)
                    btn.grid(row=i, column=j, sticky='nsew', padx=1, pady=1, rowspan=1)
                elif text in ['QUIT', 'CLEAR', 'DEL', 'GRAPH']:
                    btn = tk.Button(button_frame, text=text, command=lambda t=text: self.button_click(t),
                                   bg='#E74C3C', fg='white', font=('Arial', 9, 'bold'),
                                   relief=tk.RAISED, bd=2)
                    btn.grid(row=i, column=j, sticky='nsew', padx=1, pady=1)
                elif text in ['SIN', 'COS', 'TAN', 'LOG', 'LN', 'X²', '^', 'MODE']:
                    btn = tk.Button(button_frame, text=text, command=lambda t=text: self.button_click(t),
                                   bg='#8E44AD', fg='white', font=('Arial', 9, 'bold'),
                                   relief=tk.RAISED, bd=2)
                    btn.grid(row=i, column=j, sticky='nsew', padx=1, pady=1)
                else:
                    btn = tk.Button(button_frame, text=text, command=lambda t=text: self.button_click(t),
                                   bg='#34495E', fg='white', font=('Arial', 11),
                                   relief=tk.RAISED, bd=2)
                    btn.grid(row=i, column=j, sticky='nsew', padx=1, pady=1)
        
        for i in range(8):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            button_frame.grid_columnconfigure(j, weight=1)
    
    def update_input_display(self, text):
        self.input_display.config(state='normal')
        self.input_display.delete(0, tk.END)
        self.input_display.insert(0, text)
        self.input_display.config(state='readonly')
    
    def update_main_display(self, text):
        self.display.config(state='normal')
        self.display.insert(tk.END, text + '\n')
        self.display.config(state='disabled')
        self.display.see(tk.END)
    
    def button_click(self, button_text):
        if button_text == 'QUIT':
            self.root.quit()
        elif button_text == 'CLEAR':
            self.current_input = ""
            self.update_input_display("")
        elif button_text == 'DEL':
            self.current_input = self.current_input[:-1]
            self.update_input_display(self.current_input)
        elif button_text == 'ENTER':
            self.calculate()
        elif button_text == 'GRAPH':
            self.open_graph_window()
        elif button_text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
            self.current_input += button_text
            self.update_input_display(self.current_input)
        elif button_text in ['+', '-', '×', '÷', '^']:
            if button_text == '×':
                self.current_input += '*'
            elif button_text == '÷':
                self.current_input += '/'
            elif button_text == '^':
                self.current_input += '**'
            else:
                self.current_input += button_text
            self.update_input_display(self.current_input.replace('*', '×').replace('/', '÷').replace('**', '^'))
        elif button_text == '(':
            self.current_input += '('
            self.update_input_display(self.current_input)
        elif button_text == ')':
            self.current_input += ')'
            self.update_input_display(self.current_input)
        elif button_text == '(-)':
            if self.current_input and self.current_input[-1].isdigit():
                self.current_input += '*(-1)'
            else:
                self.current_input += '-'
            self.update_input_display(self.current_input.replace('*(-1)', '(-)'))
        elif button_text in ['SIN', 'COS', 'TAN', 'LOG', 'LN', 'X²']:
            self.add_function(button_text)
    
    def add_function(self, func):
        if func == 'SIN':
            self.current_input += 'sin('
        elif func == 'COS':
            self.current_input += 'cos('
        elif func == 'TAN':
            self.current_input += 'tan('
        elif func == 'LOG':
            self.current_input += 'log10('
        elif func == 'LN':
            self.current_input += 'log('
        elif func == 'X²':
            self.current_input += '**2'
        
        display_text = self.current_input.replace('sin(', 'sin(').replace('cos(', 'cos(').replace('tan(', 'tan(').replace('log10(', 'log(').replace('log(', 'ln(').replace('**2', '²')
        self.update_input_display(display_text)
    
    def calculate(self):
        try:
            result = evaluate_expression(self.current_input)
            self.update_main_display(f"{self.current_input} = {result}")
            self.current_input = str(result)
            self.update_input_display(self.current_input)
        except Exception as e:
            self.update_main_display(f"Error: {str(e)}")
            
    def open_graph_window(self):
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Graph")
        graph_window.geometry("600x500")
        graph_window.configure(bg='white')
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.grid(True)
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Graph')
        
        canvas = FigureCanvasTkAgg(fig, graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    calculator = TI84Calculator()
    calculator.root.mainloop()