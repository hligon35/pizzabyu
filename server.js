const express = require('express');
const cors = require('cors'); // Import CORS middleware
const app = express();
const port = 3000;

app.use(cors()); // Enable CORS for all routes
app.use(express.json()); // Middleware to parse JSON bodies

// In-memory storage for demonstration purposes
let loyaltyInfo = [];
let orders = [];
let uniqueLoyaltyId = 1;
let uniqueOrderId = 1;

// --- Loyalty Routes ---
app.post('/api/loyalty', (req, res) => {
    const { firstName, lastName, address, email, phone } = req.body;
    if (!firstName || !lastName || !address || !email || !phone) {
        return res.status(400).json({ message: 'All fields are required for loyalty signup.' });
    }
    const newMember = {
        id: uniqueLoyaltyId++,
        firstName,
        lastName,
        address,
        email,
        phone,
        signupDate: new Date().toISOString()
    };
    loyaltyInfo.push(newMember);
    console.log('New loyalty member:', newMember);
    res.status(201).json({ message: 'Successfully signed up for loyalty program!', member: newMember });
});

app.get('/api/loyalty', (req, res) => {
    res.json(loyaltyInfo);
});

// --- Order Routes ---
app.post('/api/orders', (req, res) => {
    const { items, totalAmount, customerDetails } = req.body; // Assuming these fields in the request
    if (!items || items.length === 0) {
        return res.status(400).json({ message: 'Order must contain items.' });
    }
    const newOrder = {
        orderId: uniqueOrderId++,
        orderDate: new Date().toISOString(),
        items, // e.g., [{ description: "Large Pepperoni", quantity: 1, price: 15.99 }]
        totalAmount, // e.g., 15.99
        customerDetails, // e.g., { name: "John Doe", phone: "123-456-7890" } (optional)
        status: 'Received'
    };
    orders.push(newOrder);
    console.log('New order received:', newOrder);
    res.status(201).json({ message: 'Order placed successfully!', order: newOrder });
});

app.get('/api/orders', (req, res) => {
    res.json(orders);
});

app.get('/api/orders/:id', (req, res) => {
    const order = orders.find(o => o.orderId === parseInt(req.params.id));
    if (!order) {
        return res.status(404).json({ message: 'Order not found.' });
    }
    res.json(order);
});

// --- Basic Welcome Route ---
app.get('/', (req, res) => {
    res.send('PizzaByU Backend is running!');
});

app.listen(port, () => {
    console.log(`PizzaByU backend server listening at http://localhost:${port}`);
});
