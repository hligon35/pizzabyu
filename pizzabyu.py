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
menuWindow.resizable(True, True)  # Make the window resizable


# Create and display heading
headingLabel = tk.Label(menuWindow, text = "Customize Your Pizza", font = ("Times New Roman", 40, "bold"))
headingLabel.grid(row = 0, column = 0, columnspan = 7, pady = 0, sticky = tk.NSEW)

# Uncomment the following lines to change the banner to an image
# from PIL import Image, ImageTk
# bannerImage = Image.open("path/to/your/image.png")
# bannerPhoto = ImageTk.PhotoImage(bannerImage)
# bannerLabel.config(image=bannerPhoto)

# Configure the grid to expand proportionally
for i in range(8):
    menuWindow.grid_rowconfigure(i, weight=1)
for i in range(7):
    menuWindow.grid_columnconfigure(i, weight=1)

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
    optionLabel = tk.Label(menuWindow, text = option, font = ("Times New Roman", 20, "bold"))
    optionLabel.grid(row = rowIndex, column = 0, columnspan = 7, pady = 2, sticky = tk.NSEW)
    rowIndex += 2

    if option != "Toppings":
        selectedVar = tk.StringVar()
        selectedVar.set("")  # Set default selection to an empty string
        selectedItems[option] = selectedVar
    else:
        selectedItems[option] = []
        for item in items:
            var = tk.IntVar()
            var.set(0)  # Set default selection to 0 (unselected)
            selectedItems[option].append(var)
    
    rowIndex += 1

    colIndex = 2
    for item in items:
        if option != "Toppings":
            itemButton = tk.Radiobutton(menuWindow, text = item, font = ("Times New Roman", 15), variable = selectedItems[option], value = item)
        else:
            itemButton = tk.Checkbutton(menuWindow, text = item, font = ("Times New Roman", 15), variable = selectedItems[option][colIndex-2], onvalue = item, offvalue = "")
        itemButton.grid(row = rowIndex, column = colIndex, padx = 5, pady = 2, sticky = tk.NSEW)
        colIndex += 1

    rowIndex += 7 # Add 7 empty rows between each item grid

# Add 15 rows of space below the last item button directory
rowIndex += 15

# View Order Window
viewOrderWindow = tk.Toplevel(menuWindow)
viewOrderWindow.title("View Order")
viewOrderWindow.geometry("900x600")
viewOrderWindow.withdraw()  # Keep the View Order window hidden

backButton = tk.Button(viewOrderWindow, text = "Go Back", command = lambda: openMenuWindow(viewOrderWindow, menuWindow))
backButton.pack(pady = 10)

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

    orderLabel = tk.Label(viewOrderWindow, text = selectedItemsStr, font = ("Times New Roman", 15))
    orderLabel.pack()

    menuWindow.withdraw()
    viewOrderWindow.deiconify()

# Function to verify selections and show the view order window
def verifySelection():
    selectedItemCount = 0
    for option, var in selectedItems.items():
        if isinstance(var, list):  # Handle Toppings separately
            selectedItemCount += sum([1 for v in var if v.get() != 0])
        else:
            if var.get() != "":
                selectedItemCount += 1
    requiredSelections = ["Size", "Crust", "Sauce", "Cheese"]
    missingSelections = [option for option in requiredSelections if selectedItems[option].get() == ""]
    
    if missingSelections:
        messagebox.showerror("Error", f"Please select an option for: {', '.join(missingSelections)}")
    else:
        showViewOrderWindow()

verifyButton = tk.Button(menuWindow, text = "Add to Oven", font = ("Times New Roman", 15, "bold"), command = verifySelection)
verifyButton.grid(row = rowIndex, column = 3, columnspan = 2, pady = 10, sticky = tk.NSEW)

viewOrderButton = tk.Button(menuWindow, text = "View Order", font = ("Times New Roman", 15, "bold"), command = showViewOrderWindow)
viewOrderButton.grid(row = rowIndex, column = 5, columnspan = 2, pady = 10, sticky = tk.NSEW)

# Add 25 rows of space below the buttons
rowIndex += 25

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