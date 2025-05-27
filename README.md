# PizzaByU Application

## Description

PizzaByU is a desktop application built with Python and Tkinter that allows users to customize and order pizzas. It features a graphical user interface for selecting pizza options, managing an order, and simulating the order process.

## Prerequisites

- Python 3.x
- Tkinter library (typically included with standard Python installations)

## How to Run the Application

1.  Ensure you have Python 3 installed on your system.
2.  Save the `pizzabyu.py` file to a directory on your computer.
3.  Open a terminal or command prompt.
4.  Navigate to the directory where you saved the file.
    ```sh
    cd path\to\your\directory
    ```
5.  Run the application using the Python interpreter:
    ```sh
    python pizzabyu.py
    ```

## How to Use the Application

### 1. Greeting Screen

- Upon launching the application, a "PizzaByU" greeting screen will appear.
- This screen will automatically transition to the main menu after 1.5 seconds.

### 2. Customize Your Pizza (Menu Screen)

This is where you build your pizza(s).

- **Select Pizza Options:**
  - **Size:** Choose one option (Personal, Small, Medium, Large, XLarge).
  - **Crust:** Choose one option (Thin, Hand Tossed, Stuffed).
  - **Sauce:** Choose one option for sauce amount (Light, Regular, Extra).
  - **Cheese:** Choose one option for cheese amount (Light, Regular, Extra).
  - **Toppings:** Select one or more toppings (Three Cheese, Pepperoni, Sausage, Ham, Onions, Peppers, Mushrooms).
- **Buttons:**
  - **Preview Order:**
    - Click and hold this button to see a pop-up window displaying a summary of the pizza you are currently customizing.
    - The preview window will disappear when you release the mouse button.
  - **Add to Pan:**
    - Once you are satisfied with your pizza customization, click this button.
    - The selected pizza will be added to your order.
    - The selections on the menu screen will reset, allowing you to customize another pizza if desired.
    - If you try to add to pan without selecting a size, crust, sauce, or cheese, an error message will appear prompting you to make a selection.
  - **Finish Order:**
    - When you have added all desired pizzas to your pan, click this button to proceed to the Order Cart.

### 3. Order Cart Screen

This screen displays your complete order and allows you to finalize it.

- **Order Summary:**
  - The top section of this screen shows a list of all pizzas you've added to your order, along with their quantities.
- **Customer Information Form (Optional Rewards Club):**
  - Below the order summary, there is a form to join the PizzaByU rewards club.
  - Fill in your First Name, Last Name, Address, Email, and Phone Number.
  - The phone number field will automatically format the number as you type (e.g., XXX-XXX-XXXX).
  - **Submit Button (for rewards form):** Click this after filling in your details to join the rewards club. A confirmation message will appear, and the form will be cleared and hidden.
  - All fields in the rewards form are required if you choose to submit it.
- **Navigation and Order Finalization Buttons:**
  - **Back Button:**
    - If you need to make changes to your order (e.g., add another pizza, modify an existing concept by re-adding), click this button.
    - It will take you back to the "Customize Your Pizza" menu screen. Your current order cart contents will be preserved.
  - **Send to Oven Button:**
    - When you are ready to place your order, click this button.
    - A "Thank You" window will appear, displaying a confirmation message and an estimated pick-up time for your order.
    - The pick-up time is calculated based on the number of pizzas (15 minutes for the first pizza + 3 minutes for each additional pizza).
    - This "Thank You" window will automatically close after 15 seconds. The main application will also close after the cart window is destroyed by this action.

Enjoy your pizza from PizzaByU!
