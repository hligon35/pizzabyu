"""
Author: Harold Ligon
Date written: 12/11/2024
This program gathers the users choice selection for a pizza then creates an order.
"""

import tkinter as tk
from tkinter import messagebox

# Create the main window
greetingWindow = tk.Tk()
greetingWindow.title("PizzaByU")
greetingWindow.state("zoomed")

# Display "PizzaByU" in the center
titleLabel = tk.Label(greetingWindow, text = "PizzaByU", font = ("Times New Roman", 100))
titleLabel.pack(expand = True, fill = tk.BOTH)

# Function to open the order screen window
def openMenuWindow():
    # Order Screen Window
    menuWindow = tk.Tk()
    menuWindow.title("Customize Your Pizza")
    menuWindow.geometry("1200x800")
    menuWindow.resizable(True, True)  # Make the window resizable
    menuWindow.grid_rowconfigure(0, weight=1)
    for i in range(1, 30):
        menuWindow.grid_rowconfigure(i, weight=1)
    for j in range(7):
        menuWindow.grid_columnconfigure(j, weight=1)

    # Create and display heading
    headingLabel = tk.Label(menuWindow, text = "Customize Your Pizza", font = ("Times New Roman", 40, "bold"))
    headingLabel.grid(row = 0, column = 0, columnspan = 7, pady = 0, sticky = tk.NSEW)

    # Dictionary to store selected items for size, crust, sauce, cheese
    pizzaDetails = {
        "Size": [],
        "Crust": [],
        "Sauce": [],
        "Cheese": [],
        "Toppings": []
    }

    pizzaOptions = {
        "Size": ["Personal", "Small", "Medium", "Large", "XLarge"],
        "Crust": ["Thin", "Hand Tossed", "Stuffed"],
        "Sauce": ["Light", "Regular", "Extra"],
        "Cheese": ["Light", "Regular", "Extra"],
        "Toppings": ["Three Cheese", "Pepperoni", "Sausage", "Ham", "Onions", "Peppers", "Mushrooms"]
    }

    # Function to create and display pizzaOptions
    def createOptionMenu(optionName, optionValues, row):
        if optionName == "Size":
            label = tk.Label(menuWindow, text=optionName, font=("Times New Roman", 20))
            label.grid(row=row, column=0, columnspan=5, pady=10, sticky=tk.NSEW)
            for index, value in enumerate(optionValues):
                var = tk.IntVar()
                pizzaDetails[optionName].append((value, var))
                check_button = tk.Checkbutton(menuWindow, text=value, variable=var, font=("Times New Roman", 20))
                check_button.grid(row=row+1, column=index, columnspan=1, pady=10, padx=5, sticky=tk.NSEW)
        elif optionName in ["Crust", "Cheese"]:
            label = tk.Label(menuWindow, text=optionName, font=("Times New Roman", 20))
            label.grid(row=row, column=0, columnspan=3, pady=10, sticky=tk.NSEW)
            for index, value in enumerate(optionValues):
                var = tk.IntVar()
                pizzaDetails[optionName].append((value, var))
                check_button = tk.Checkbutton(menuWindow, text=value, variable=var, font=("Times New Roman", 20))
                check_button.grid(row=row+1, column=index*2, columnspan=1, pady=10, padx=5, sticky=tk.NSEW)
        else:
            label = tk.Label(menuWindow, text=optionName, font=("Times New Roman", 20))
            label.grid(row=row, column=0, columnspan=7, pady=10, sticky=tk.NSEW)
            for index, value in enumerate(optionValues):
                var = tk.IntVar()
                pizzaDetails[optionName].append((value, var))
                check_button = tk.Checkbutton(menuWindow, text=value, variable=var, font=("Times New Roman", 20))
                check_button.grid(row=row+1, column=index, columnspan=1, pady=10, padx=5, sticky=tk.NSEW)

    # Create and display pizzaOptions
    row = 1
    for optionName, optionValues in pizzaOptions.items():
        createOptionMenu(optionName, optionValues, row)
        row += 2

    # Function to validate selections and open the view order window
    def addToOven():
        for key in ["Size", "Crust", "Sauce", "Cheese"]:
            if not any(var.get() for _, var in pizzaDetails[key]):
                messagebox.showerror("Error", f"Please select at least one {key.lower()}.")
                return
        
        viewOrderWindow()

    # Function to open the view order window
    def viewOrderWindow():
        viewOrderWindow = tk.Tk()
        viewOrderWindow.title("View Your Order")
        viewOrderWindow.geometry("600x400")
        
        order_summary = ""
        for key, items in pizzaDetails.items():
            selected = [name for name, var in items if var.get() == 1]
            if selected:
                order_summary += f"{key}: {', '.join(selected)}\n"
        
        order_label = tk.Label(viewOrderWindow, text=order_summary, font=("Times New Roman", 20))
        order_label.pack(expand=True, fill=tk.BOTH)
        
        viewOrderWindow.mainloop()

    # Add to Oven button
    addToOvenButton = tk.Button(menuWindow, text="Add to Oven", command=addToOven, font=("Times New Roman", 20))
    addToOvenButton.grid(row=row, column=0, columnspan=7, pady=20, sticky=tk.NSEW)

    # Start the menu window main loop
    menuWindow.mainloop()

# Destroy opening window after 1.5 seconds and open the order screen window
greetingWindow.after(1500, lambda: (greetingWindow.destroy(), openMenuWindow()))

# Start the greeting window main loop
greetingWindow.mainloop()