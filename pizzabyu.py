"""
Author: Harold Ligon
Date written: 12/11/2024
This program gathers the user's choice selection for a pizza then creates an order.
"""

import tkinter as tk
from tkinter import messagebox

# Function to center a window
def centerWindow(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Initialize the order summary and order counts
currentOrderSummary = ""
orderCounts = {}

# Create the main window
greetingWindow = tk.Tk()
greetingWindow.title("PizzaByU")
greetingWindow.geometry("1500x900")
centerWindow(greetingWindow)

# Display "PizzaByU" in the center
titleLabel = tk.Label(greetingWindow, text="PizzaByU", font=("Times New Roman", 100))
titleLabel.pack(expand=True, fill=tk.BOTH)

# Function to open the menu window
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
    centerWindow(menuWindow)

    # Create and display heading
    headingLabel = tk.Label(menuWindow, text="Customize Your Pizza", font=("Times New Roman", 40, "bold"))
    headingLabel.grid(row=0, column=0, columnspan=7, pady=0, sticky=tk.NSEW)

    # Dictionary to store IntVar instances for each option
    pizzaVars = {}

    # Arrays to store keys and items
    optionKeys = ["Size", "Crust", "Sauce", "Cheese", "Toppings"]
    sizeOptions = ["Personal", "Small", "Medium", "Large", "XLarge"]
    crustOptions = ["Thin", "Hand Tossed", "Stuffed"]
    sauceOptions = ["Light", "Regular", "Extra"]
    cheeseOptions = ["Light", "Regular", "Extra"]
    toppingsOptions = ["Three Cheese", "Pepperoni", "Sausage", "Ham", "Onions", "Peppers", "Mushrooms"]

    # Array of arrays for the items
    optionValues = [sizeOptions, crustOptions, sauceOptions, cheeseOptions, toppingsOptions]

    # Center all pizzaOptions horizontally and evenly space them
    def createOptionMenu(optionName, optionValues, row, columnspan, columnshift=0):
        label = tk.Label(menuWindow, text=optionName, font=("Times New Roman", 20))
        label.grid(row=row, column=columnshift, columnspan=columnspan, pady=10, sticky=tk.NSEW)
        
        varList = []
        for index, value in enumerate(optionValues):
            var = tk.IntVar()
            checkbutton = tk.Checkbutton(menuWindow, text=value, variable=var, font=("Times New Roman", 18))
            checkbutton.grid(row=row+1, column=index + columnshift, padx=10, pady=5, sticky=tk.NSEW)
            varList.append((value, var))
        
        pizzaVars[optionName] = varList

    # Create and display pizzaOptions
    row = 1
    createOptionMenu(optionKeys[0], optionValues[0], row, columnspan=7)  # Size options
    row += 3
    for i in range(1, 4):  # Crust, Sauce, Cheese options
        createOptionMenu(optionKeys[i], optionValues[i], row, columnspan=5, columnshift=2)
        row += 3
    createOptionMenu(optionKeys[4], optionValues[4], row, columnspan=7)  # Toppings options

    # Function to validate selections and prepare the order summary
    def addToOven():
        for key in ["Size", "Crust", "Sauce", "Cheese"]:
            if not any(var.get() for _, var in pizzaVars[key]):
                messagebox.showerror("Error", f"Please select ONLY one {key.lower()}.")
                return
        
        # Prepare the order summary
        orderSummary = ""
        for key, items in pizzaVars.items():
            selected = [name for name, var in items if var.get() == 1]
            if selected or key == "Toppings":
                orderSummary += f"{key}: {', '.join(selected)}. "
        
        updateOrderSummary(orderSummary)

    # Function to update the order summary
    def updateOrderSummary(summary):
        global currentOrderSummary, orderCounts
        if summary in orderCounts:
            orderCounts[summary] += 1
        else:
            orderCounts[summary] = 1
        
        # Rebuild the current order summary
        currentOrderSummary = ""
        for idx, (order, count) in enumerate(orderCounts.items(), start=1):
            currentOrderSummary += f"{idx}. {order} ({count})\n"

    # Function to show the order summary
    def showOrderSummary(event):
        if 'currentOrderSummary' in globals() and currentOrderSummary:
            global summaryWindow
            summaryWindow = tk.Toplevel(menuWindow)
            summaryWindow.title("Order Summary")
            summaryWindow.resizable(True, True)
            
            summaryLabel = tk.Label(summaryWindow, text=currentOrderSummary, font=("Times New Roman", 14))
            summaryLabel.pack(expand=True, fill=tk.BOTH)
            
            # Adjust the window size to fit the content
            summaryWindow.update_idletasks()
            width = summaryLabel.winfo_reqwidth() + 20
            height = summaryLabel.winfo_reqheight() + 20
            summaryWindow.geometry(f"{width}x{height}")

    # Function to hide the order summary pop-up window
    def hideOrderSummary(event):
        if 'summaryWindow' in globals():
            summaryWindow.destroy()

    # Function to show the order summary in a table format
    def showOrderCart(menuWindow):
        if 'currentOrderSummary' in globals() and currentOrderSummary:
            menuWindow.destroy()
            cartWindow = tk.Tk()
            cartWindow.title("Order Cart")
            cartWindow.geometry("900x600")
            cartWindow.resizable(True, True)

            cartLabel = tk.Label(cartWindow, text="Order Cart", font=("Times New Roman", 20, "bold"))
            cartLabel.pack(pady=10)
            
            # Split the order summary into lines and display each line in a new row
            orderLines = currentOrderSummary.strip().split('\n')
            for line in orderLines:
                entryLabel = tk.Label(cartWindow, text=line, font=("Times New Roman", 14))
                entryLabel.pack(anchor=tk.W, padx=40, pady=2)

    # Function to add shadow effect on hover
    def onEnter(event):
        event.widget.config(relief="raised", bd=2)

    def onLeave(event):
        event.widget.config(relief="flat", bd=1)

    row += 3  # Increment row for button placement

    # View Order button
    previewOrderButton = tk.Button(menuWindow, text="View Order", font=("Times New Roman", 20), activebackground="yellow")
    previewOrderButton.grid(row=row, column=0, columnspan=2, padx=40, pady=20, sticky=tk.NSEW)
    previewOrderButton.bind("<ButtonPress>", showOrderSummary)
    previewOrderButton.bind("<ButtonRelease>", hideOrderSummary)
    previewOrderButton.bind("<Enter>", onEnter)
    previewOrderButton.bind("<Leave>", onLeave)

    # Add to Oven button
    addToOvenButton = tk.Button(menuWindow, text="Add to Oven", command=addToOven, font=("Times New Roman", 20), activebackground="orange")
    addToOvenButton.grid(row=row, column=2, columnspan=3, padx=40, pady=20, sticky=tk.NSEW)
    addToOvenButton.bind("<Enter>", onEnter)
    addToOvenButton.bind("<Leave>", onLeave)

    # Finish button
    finishButton = tk.Button(menuWindow, text="Finish", command=lambda: showOrderCart(menuWindow), font=("Times New Roman", 20), activebackground="green")
    finishButton.grid(row=row, column=5, columnspan=2, padx=40, pady=20, sticky=tk.NSEW)
    finishButton.bind("<Enter>", onEnter)
    finishButton.bind("<Leave>", onLeave)

    # Start the menu window main loop
    menuWindow.mainloop()

# Destroy opening window after 1.5 seconds and open the order screen window
greetingWindow.after(1500, lambda: (greetingWindow.destroy(), openMenuWindow()))

# Start the greeting window main loop
greetingWindow.mainloop()