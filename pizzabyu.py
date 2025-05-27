"""
Author: Harold Ligon
Date written: 12/11/2024
This program gathers the user's choice selection for a pizza then creates an order.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

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

loyaltyInfo = []
uniqueID = 1

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
    def createOptionMenu(optionName, optionValues, row, columnspan, columnshift=0, multiple=False):
        label = tk.Label(menuWindow, text=optionName, font=("Times New Roman", 20))
        label.grid(row=row, column=columnshift, columnspan=columnspan, pady=10, sticky=tk.NSEW)
        
        varList = []
        if multiple:
            for index, value in enumerate(optionValues):
                var = tk.IntVar()
                checkbutton = tk.Checkbutton(menuWindow, text=value, variable=var, font=("Times New Roman", 18))
                checkbutton.grid(row=row+1, column=index + columnshift, padx=10, pady=5, sticky=tk.NSEW)
                varList.append((value, var))
        else:
            ## Initialize the variable with an empty string to avoid the visual issue
            var = tk.StringVar(value="")
            for index, value in enumerate(optionValues):
                radiobutton = tk.Radiobutton(menuWindow, text=value, variable=var, value=value, font=("Times New Roman", 18))
                radiobutton.grid(row=row+1, column=index + columnshift, padx=10, pady=5, sticky=tk.NSEW)
            varList.append((optionName, var))
        
        pizzaVars[optionName] = varList

    # Create and display pizzaOptions
    row = 1
    createOptionMenu(optionKeys[0], optionValues[0], row, columnspan=7)  # Size options
    row += 3
    for i in range(1, 4):  # Crust, Sauce, Cheese options
        createOptionMenu(optionKeys[i], optionValues[i], row, columnspan=3, columnshift=2)
        row += 3
    createOptionMenu(optionKeys[4], optionValues[4], row, columnspan=7, multiple=True)  # Toppings options

    # Function to validate selections and prepare the order summary
    def addToPan():
        for key in ["Size", "Crust", "Sauce", "Cheese"]:
            if not pizzaVars[key][0][1].get():
                messagebox.showerror("Error", f"Please select one {key.lower()} option.")
                return
        
        # Prepare the order summary
        orderSummary = ""
        for key, items in pizzaVars.items():
            if key == "Toppings":
                selected = [name for name, var in items if var.get() == 1]
            else:
                selected = [items[0][1].get()]
            if selected:
                orderSummary += f"{key}: {', '.join(selected)}. "
        
        updateOrderSummary(orderSummary)

        # Reset all item values to default
        for key, items in pizzaVars.items():
            if key == "Toppings":
                for _, var in items:
                    var.set(0)
            else:
                items[0][1].set("")

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
    def previewOrderSummary(event):
        if 'currentOrderSummary' in globals() and currentOrderSummary:
            global summaryWindow
            summaryWindow = tk.Toplevel(menuWindow)
            summaryWindow.title("Order Summary")
            summaryWindow.resizable(True, True)
            
            ## Add heading saying "Preview Order" in the center of the very top row
            summaryHeading = tk.Label(summaryWindow, text="Preview Order", font=("Times New Roman", 24, "bold"))
            summaryHeading.pack(pady=10)
            
            summaryLabel = tk.Label(summaryWindow, text=currentOrderSummary, font=("Times New Roman", 14))
            summaryLabel.pack(expand=True, fill=tk.BOTH)
            
            # Adjust the window size to fit the content
            summaryWindow.update_idletasks()
            centerWindow(summaryWindow)

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
            centerWindow(cartWindow)
            
            ## Add heading saying "Order Cart" in the center of the very top row
            cartHeading = tk.Label(cartWindow, text="Order Cart", font=("Times New Roman", 24, "bold"))
            cartHeading.pack(pady=10)
            
            # Split the order summary into lines and display each line in a new row
            orderLines = currentOrderSummary.strip().split('\n')
            for line in orderLines:
                entryLabel = tk.Label(cartWindow, text=line, font=("Times New Roman", 14))
                entryLabel.pack(anchor=tk.W, padx=40, pady=2)

            # Form for user information
            formFrame = tk.Frame(cartWindow)
            formFrame.pack(pady=20)

            tk.Label(formFrame, text="First Name:", font=("Times New Roman", 14)).grid(row=0, column=0, padx=5, pady=5)
            firstNameEntry = tk.Entry(formFrame, font=("Times New Roman", 14))
            firstNameEntry.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(formFrame, text="Last Name:", font=("Times New Roman", 14)).grid(row=0, column=2, padx=5, pady=5)
            lastNameEntry = tk.Entry(formFrame, font=("Times New Roman", 14))
            lastNameEntry.grid(row=0, column=3, padx=5, pady=5)

            tk.Label(formFrame, text="Address:", font=("Times New Roman", 14)).grid(row=1, column=0, padx=5, pady=5)
            addressEntry = tk.Entry(formFrame, font=("Times New Roman", 14))
            addressEntry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)

            tk.Label(formFrame, text="Email:", font=("Times New Roman", 14)).grid(row=2, column=0, padx=5, pady=5)
            emailEntry = tk.Entry(formFrame, font=("Times New Roman", 14))
            emailEntry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)

            tk.Label(formFrame, text="Phone Number:", font=("Times New Roman", 14)).grid(row=3, column=0, padx=5, pady=5)
            phoneEntry = tk.Entry(formFrame, font=("Times New Roman", 14), width=12)
            phoneEntry.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)

            def formatPhoneNumber(event):
                phone = phoneEntry.get().replace("-", "")
                if len(phone) > 6:
                    phone = phone[:3] + "-" + phone[3:6] + "-" + phone[6:10]
                elif len(phone) > 3:
                    phone = phone[:3] + "-" + phone[3:6]
                phoneEntry.delete(0, tk.END)
                phoneEntry.insert(0, phone)

            phoneEntry.bind("<KeyRelease>", formatPhoneNumber)

            def submitForm():
                global uniqueID
                firstName = firstNameEntry.get()
                lastName = lastNameEntry.get()
                address = addressEntry.get()
                email = emailEntry.get()
                phone = phoneEntry.get()

                if not (firstName and lastName and address and email and phone):
                    messagebox.showerror("Error", "All fields are required.")
                    return

                loyaltyInfo.append({
                    "ID": uniqueID,
                    "First Name": firstName,
                    "Last Name": lastName,
                    "Address": address,
                    "Email": email,
                    "Phone": phone
                })
                uniqueID += 1

                messagebox.showinfo("Success", "Thank you for joining the rewards club!")
                firstNameEntry.delete(0, tk.END)
                lastNameEntry.delete(0, tk.END)
                addressEntry.delete(0, tk.END)
                emailEntry.delete(0, tk.END)
                phoneEntry.delete(0, tk.END)

                # Remove the form and display thank you message
                formFrame.pack_forget()
                thankYouLabel = tk.Label(cartWindow, text="Thank you for joining the rewards club!", font=("Times New Roman", 24, "bold"))
                thankYouLabel.pack(pady=20)

            submitButton = tk.Button(formFrame, text="Submit", command=submitForm, font=("Times New Roman", 14))
            submitButton.grid(row=4, column=0, columnspan=4, pady=10)

            # Back button to return to the menu window
            def backToMenu():
                cartWindow.destroy()
                openMenuWindow()

            # Back button
            backButton = tk.Button(cartWindow, text="Back", command=backToMenu, font=("Times New Roman", 20), activebackground="yellow")
            backButton.bind("<Enter>", onEnter)
            backButton.bind("<Leave>", onLeave)
            backButton.pack(side=tk.LEFT, padx=5, pady=5)

            # Send to Oven button
            def sendToOven():
                cartWindow.destroy()
                thankYouWindow = tk.Tk()
                thankYouWindow.title("Thank You")
                thankYouWindow.geometry("600x400")
                centerWindow(thankYouWindow)
                
                # Calculate the total number of pizzas
                totalPizzas = sum(int(line.split('(')[-1].strip(')')) for line in orderLines)
                
                # Calculate the pizzaTime
                pizzaTime = 15 + (totalPizzas - 1) * 3
                
                # Calculate the pick-up time
                pickUpTime = datetime.now() + timedelta(minutes=pizzaTime)
                pickUpTimeStr = pickUpTime.strftime("%I:%M %p")
                
                thankYouLabel = tk.Label(thankYouWindow, text=f"Thank you for ordering with PizzaByU!\nYour order will be ready for pick up by {pickUpTimeStr}.", font=("Times New Roman", 20))
                thankYouLabel.pack(expand=True, fill=tk.BOTH)
                
                # Close the thank you window after 15 seconds
                thankYouWindow.after(15000, thankYouWindow.destroy)

            sendToOvenButton = tk.Button(cartWindow, text="Send to Oven", command=sendToOven, font=("Times New Roman", 20), activebackground="orange")
            sendToOvenButton.bind("<Enter>", onEnter)
            sendToOvenButton.bind("<Leave>", onLeave)
            sendToOvenButton.pack(side=tk.RIGHT, padx=5, pady=5)

    # Function to add effect on hover
    def onEnter(event):
        event.widget.config(relief="raised", bd=2)

    def onLeave(event):
        event.widget.config(relief="raised", bd=1)

    row += 3  # Increment row for button placement

    # Preview Order button
    previewOrderButton = tk.Button(menuWindow, text="Preview Order", font=("Times New Roman", 20), activebackground="yellow")
    previewOrderButton.grid(row=row, column=0, columnspan=2, padx=20, pady=20, sticky=tk.NSEW)
    previewOrderButton.bind("<ButtonPress>", previewOrderSummary)
    previewOrderButton.bind("<ButtonRelease>", hideOrderSummary)
    previewOrderButton.bind("<Enter>", onEnter)
    previewOrderButton.bind("<Leave>", onLeave)

    # Add to Pan button
    addToPanButton = tk.Button(menuWindow, text="Add to Pan", command=addToPan, font=("Times New Roman", 20), activebackground="orange")
    addToPanButton.grid(row=row, column=2, columnspan=3, padx=20, pady=20, sticky=tk.NSEW)
    addToPanButton.bind("<Enter>", onEnter)
    addToPanButton.bind("<Leave>", onLeave)

    # Finish Order button
    finishOrderButton = tk.Button(menuWindow, text="Finish Order", command=lambda: showOrderCart(menuWindow), font=("Times New Roman", 20), activebackground="green")
    finishOrderButton.grid(row=row, column=5, columnspan=2, padx=20, pady=20, sticky=tk.NSEW)
    finishOrderButton.bind("<Enter>", onEnter)
    finishOrderButton.bind("<Leave>", onLeave)

    # Start the menu window main loop
    menuWindow.mainloop()

# Destroy opening window after 1.5 seconds and open the order screen window
greetingWindow.after(1500, lambda: (greetingWindow.destroy(), openMenuWindow()))

# Start the greeting window main loop
greetingWindow.mainloop()