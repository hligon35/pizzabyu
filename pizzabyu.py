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

# Destroy opening window after 1.5 seconds and open the order screen window
greetingWindow.after(1500, lambda: greetingWindow.destroy())

# Order Screen Window
menuWindow = tk.Tk()
menuWindow.title("Customize Your Pizza")
menuWindow.geometry("900x600")

# Create and display heading
headingLabel = tk.Label(menuWindow, text = "Customize Your Pizza", font = ("Times New Roman", 30, "bold"))
headingLabel.grid(row = 0, column = 0, columnspan = 5, pady = 10)

# Dictionary to store selected items for size, crust, sauce, cheese
selectedItems = {}

options = {
    "Size": ["Personal", "Small", "Medium", "Large", "XLarge"],
    "Crust": ["Thin", "Hand Tossed", "Stuffed"],
    "Sauce": ["Light", "Regular", "Extra"],
    "Cheese": ["Light", "Regular", "Extra"],
    "Toppings": ["Three Cheese", "Pepperoni", "Sausage", "Ham", "Onions", "Peppers", "Mushrooms"]
}

# Display options and radio buttons
rowIndex = 1
for option, items in options.items():
    optionLabel = tk.Label(menuWindow, text = option, font = ("Times New Roman", 12, "bold"))
    optionLabel.grid(row = rowIndex, column = 3, columnspan = 8, sticky = tk.W)

    if option != "Toppings":
        selectedVar = tk.StringVar()
        selectedVar.set(items[0])  # Set default selection
        selectedItems[option] = selectedVar
    else:
        selectedItems[option] = []
        for item in items:
            var = tk.IntVar()
            selectedItems[option].append(var)
    
    rowIndex += 1

    colIndex = 1
    for item in items:
        if option != "Toppings":
            itemButton = tk.Radiobutton(menuWindow, text = item, font = ("Times New Roman", 10), variable = selectedItems[option], value = item)
        else:
            itemButton = tk.Checkbutton(menuWindow, text = item, font = ("Times New Roman", 10), variable = selectedItems[option][colIndex-1], onvalue = item, offvalue = "")
        itemButton.grid(row = rowIndex, column = colIndex, padx = 20, sticky = tk.W)
        colIndex += 1

# Function to verify selections and show the view order window
def verifySelection():
    selectedCategoryCounts = {option: sum([1 if option == var.get() else 0 for var in selectedItems.values()]) for option in options}
    selectedItemCount = sum(selectedCategoryCounts.values())
    if selectedItemCount == 1:
        showViewOrderWindow()
    elif selectedItemCount == 0 or selectedItemCount > 1:
        messagebox.showerror("Error", "Please select only one item to add to the oven.")

verifyButton = tk.Button(menuWindow, text = "Add to Oven", command = verifySelection)
verifyButton.grid(row = 15, column = 3, pady = 10)

# View Order Window
viewOrderWindow = tk.Toplevel(menuWindow)
viewOrderWindow.title("View Order")
viewOrderWindow.geometry("900x600")
viewOrderWindow.withdraw()  # Keep the View Order window hidden



# Function to show the view order window
def showViewOrderWindow():
    selectedItemsList = []
    for option, var in selectedItems.items():
        if isinstance(var, list):  # Handle Toppings separately
            toppings = [item for item, selected in zip(options["Toppings"], var) if selected.get()]
            if toppings:
                selectedItemsList.append(f"{option}: {', '.join(toppings)}")
        else:
            selectedItemsList.append(f"{option}: {var.get()}")

    selectedItemsStr = " | ".join(selectedItemsList)

    orderLabel = tk.Label(viewOrderWindow, text = selectedItemsStr, font = ("Times New Roman", 12))
    orderLabel.pack()

    menuWindow.withdraw()
    viewOrderWindow.deiconify()

viewOrderButton = tk.Button(menuWindow, text = "View Order", command = showViewOrderWindow)
viewOrderButton.grid(row = 15, column = 4, pady = 10)

# View Order Window
viewOrderWindow = tk.Toplevel(menuWindow)
viewOrderWindow.title("View Order")
viewOrderWindow.geometry("900x600")
viewOrderWindow.withdraw()  # Keep the View Order window hidden

backButton = tk.Button(viewOrderWindow, text = "Go Back", command = lambda: openMenuWindow(viewOrderWindow, menuWindow))
backButton.pack(pady = 10)

# Function to hide the viewOrderWindow and open the menuWindow
def openMenuWindow(viewOrderWindow, menuWindow):
    viewOrderWindow.withdraw()
    menuWindow.deiconify()

# Submit Order and Thank You Window
def submitOrder():
    thankYouWindow.deiconify()
    viewOrderWindow.withdraw()

submitOrderButton = tk.Button(viewOrderWindow, text = "Submit Order", command = submitOrder)
submitOrderButton.pack()

# Thank You Window
thankYouWindow = tk.Toplevel(viewOrderWindow)
thankYouWindow.title("Thank You")
thankYouWindow.withdraw()

thankYouLabel = tk.Label(thankYouWindow, text = "Your order has been sent to the kitchen. Thank You for your support!", font = ("Times New Roman", 30))
thankYouLabel.pack(pady = 50)

# Hide the main window
greetingWindow.mainloop()