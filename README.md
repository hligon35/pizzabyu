# PizzaByU Web Application

## Description

PizzaByU is a web application that allows users to customize and order pizzas. It features an HTML/CSS/JavaScript frontend for selecting pizza options, managing an order cart, and submitting orders. A Node.js backend handles order and loyalty program data persistence (currently using in-memory storage).

## Project Structure

- `index.html`: The main HTML file for the user interface.
- `style.css`: Contains the styles for the application.
- `script.js`: Handles the frontend logic, including pizza customization, cart management, and API interactions.
- `server.js`: The Node.js Express backend server that manages API endpoints for orders and loyalty program signups.
- `package.json`: Defines project dependencies and scripts for the backend.
- `README.md`: This file.

## Setup and Running the Application

### Frontend

1.  Open the `index.html` file in a web browser.

### Backend

1.  Ensure you have Node.js and npm installed on your system.
2.  Navigate to the project directory in a terminal or command prompt:
    ```sh
    cd path/to/your/project/pizzabyu
    ```
3.  Install the necessary dependencies:
    ```sh
    npm install
    ```
4.  Start the backend server:
    ```sh
    npm start
    ```
    The server will typically run on `http://localhost:3000`.

## How to Use the Web Application

### 1. Landing Page (`index.html`)

- The application opens to the "Customize Your Pizza" screen.

### 2. Customize Your Pizza

- **Select Pizza Options:**
  - **Size:** Choose one (e.g., Personal, Small, Medium, Large, XLarge).
  - **Crust:** Choose one (e.g., Thin, Hand Tossed, Stuffed).
  - **Sauce:** Choose one (e.g., Light, Regular, Extra).
  - **Cheese:** Choose one (e.g., Light, Regular, Extra).
  - **Toppings:** Select one or more (e.g., Three Cheese, Pepperoni, Sausage, Ham, Onions, Peppers, Mushrooms).
- **Buttons:**
  - **Preview Order:** Click this button to see a summary of the current pizza being customized in a modal.
  - **Add to Pan:** Adds the currently customized pizza to your order cart. The selections will reset.
  - **Finish Order:** Takes you to the Order Cart screen to review and submit your order.

### 3. Order Cart Screen

- **Order Summary:** Displays all pizzas added to your cart with their details and quantities.
- **Loyalty Club Signup (Optional):**
  - A form to enter First Name, Last Name, Address, Email, and Phone Number.
  - Click "Submit" to join the loyalty club. This will send your information to the backend.
- **Navigation and Order Finalization Buttons:**
  - **Back:** Returns to the "Customize Your Pizza" screen.
  - **Send to Oven:** Submits your complete order to the backend. A "Thank You" message will appear.

## API Endpoints (Backend - `server.js`)

The backend server provides the following API endpoints:

- **POST `/api/loyalty`**
  - Description: Submits loyalty club signup information.
  - Request Body: `{ firstName, lastName, address, email, phone }`
  - Response: Confirmation message or error.
- **GET `/api/loyalty`**
  - Description: Retrieves all loyalty club member information (for demonstration).
  - Response: Array of loyalty member objects.
- **POST `/api/orders`**
  - Description: Submits a new pizza order.
  - Request Body: `{ cart: orderCart }` (where `orderCart` is an object containing pizza summaries and quantities)
  - Response: Confirmation message with an order ID or error.
- **GET `/api/orders`**
  - Description: Retrieves all submitted orders (for demonstration).
  - Response: Array of order objects.
- **GET `/api/orders/:id`**
  - Description: Retrieves a specific order by its ID (for demonstration).
  - Response: The order object or a "not found" message.

Enjoy your pizza from PizzaByU!
