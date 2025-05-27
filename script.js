document.addEventListener('DOMContentLoaded', () => {
    const menuScreen = document.getElementById('menuScreen');
    const cartScreen = document.getElementById('cartScreen');
    const thankYouScreen = document.getElementById('thankYouScreen');

    const previewOrderBtn = document.getElementById('previewOrderBtn');
    const addToPanBtn = document.getElementById('addToPanBtn');
    const finishOrderBtn = document.getElementById('finishOrderBtn');

    const backToMenuBtn = document.getElementById('backToMenuBtn');
    const sendToOvenBtn = document.getElementById('sendToOvenBtn');
    const submitRewardsBtn = document.getElementById('submitRewardsBtn');

    const currentOrderPreviewModal = document.getElementById('currentOrderPreview');
    const previewText = document.getElementById('previewText');
    const closeButton = document.querySelector('.close-button');

    const cartItemsContainer = document.getElementById('cartItems');
    const thankYouMessage = document.getElementById('thankYouMessage');

    let currentOrder = {};
    let orderCart = {}; // Stores { pizzaSummary: count }

    // --- Helper Functions ---
    function getSelectedOptions() {
        const size = document.querySelector('input[name="size"]:checked');
        const crust = document.querySelector('input[name="crust"]:checked');
        const sauce = document.querySelector('input[name="sauce"]:checked');
        const cheese = document.querySelector('input[name="cheese"]:checked');
        const toppings = Array.from(document.querySelectorAll('input[name="toppings"]:checked'))
                               .map(cb => cb.value);

        return {
            Size: size ? size.value : null,
            Crust: crust ? crust.value : null,
            Sauce: sauce ? sauce.value : null,
            Cheese: cheese ? cheese.value : null,
            Toppings: toppings
        };
    }

    function generateOrderSummary(options) {
        let summary = "";
        if (options.Size) summary += `Size: ${options.Size}. `;
        if (options.Crust) summary += `Crust: ${options.Crust}. `;
        if (options.Sauce) summary += `Sauce: ${options.Sauce}. `;
        if (options.Cheese) summary += `Cheese: ${options.Cheese}. `;
        if (options.Toppings && options.Toppings.length > 0) {
            summary += `Toppings: ${options.Toppings.join(', ')}. `;
        }
        return summary.trim();
    }

    function resetSelections() {
        document.querySelectorAll('input[type="radio"]').forEach(rb => rb.checked = false);
        document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
    }

    function updateCartDisplay() {
        cartItemsContainer.innerHTML = ''; // Clear previous items
        if (Object.keys(orderCart).length === 0) {
            cartItemsContainer.innerHTML = '<p>Your cart is empty.</p>';
            return;
        }
        let itemNumber = 1;
        for (const [summary, count] of Object.entries(orderCart)) {
            const cartEntry = document.createElement('div');
            cartEntry.textContent = `${itemNumber}. ${summary} (${count})`;
            cartItemsContainer.appendChild(cartEntry);
            itemNumber++;
        }
    }

    // --- Event Listeners for Menu Screen ---
    previewOrderBtn.addEventListener('mousedown', () => {
        if (Object.keys(orderCart).length === 0) {
            previewText.textContent = "Your pan is currently empty."; // textContent is fine for a simple string
        } else {
            let cartSummaryHTML = "<b>Items in your pan:</b><br>";
            let itemNumber = 1;
            for (const [summary, count] of Object.entries(orderCart)) {
                cartSummaryHTML += `${itemNumber}. ${summary} (Quantity: ${count})<br>`;
                itemNumber++;
            }
            previewText.innerHTML = cartSummaryHTML; // Use innerHTML to render <br> tags
        }
        currentOrderPreviewModal.style.display = 'flex';
    });

    previewOrderBtn.addEventListener('mouseup', () => {
        currentOrderPreviewModal.style.display = 'none';
    });

    if(closeButton) {
        closeButton.addEventListener('click', () => {
            currentOrderPreviewModal.style.display = 'none';
        });
    }

    window.addEventListener('click', (event) => {
        if (event.target === currentOrderPreviewModal) {
            currentOrderPreviewModal.style.display = 'none';
        }
    });

    addToPanBtn.addEventListener('click', () => {
        const selected = getSelectedOptions();
        if (!selected.Size || !selected.Crust || !selected.Sauce || !selected.Cheese) {
            alert("Please select Size, Crust, Sauce, and Cheese options.");
            return;
        }
        const summary = generateOrderSummary(selected);
        if (summary) {
            orderCart[summary] = (orderCart[summary] || 0) + 1;
            alert("Pizza added to pan!");
            resetSelections();
        } else {
            alert("Please make your selections.");
        }
    });

    finishOrderBtn.addEventListener('click', () => {
        if (Object.keys(orderCart).length === 0) {
            alert("Your cart is empty. Please add some pizzas first.");
            return;
        }
        updateCartDisplay();
        menuScreen.style.display = 'none';
        cartScreen.style.display = 'block';
        thankYouScreen.style.display = 'none';
    });

    // --- Event Listeners for Cart Screen ---
    backToMenuBtn.addEventListener('click', () => {
        menuScreen.style.display = 'block';
        cartScreen.style.display = 'none';
    });

    submitRewardsBtn.addEventListener('click', async () => {
        console.log("Submit Rewards button clicked");
        const firstName = document.getElementById('firstName').value;
        const lastName = document.getElementById('lastName').value;
        const address = document.getElementById('address').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;

        if (!firstName || !lastName || !address || !email || !phone) {
            alert("All fields are required for rewards club.");
            console.warn("Rewards form validation failed: All fields required.");
            return;
        }

        const memberData = { firstName, lastName, address, email, phone };
        console.log("Attempting to submit loyalty data:", memberData);

        try {
            const response = await fetch('http://localhost:3000/api/loyalty', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(memberData),
            });

            console.log("Loyalty submission response status:", response.status);
            const responseText = await response.text(); // Get raw response text
            console.log("Loyalty submission raw response text:", responseText);

            let result;
            try {
                result = JSON.parse(responseText); // Try to parse as JSON
            } catch (e) {
                console.error("Failed to parse loyalty response as JSON:", e);
                alert("Received an invalid response from the server for loyalty signup.");
                return;
            }
            
            console.log("Loyalty submission parsed response:", result);

            if (response.ok) {
                alert(result.message || "Thank you for joining the rewards club!");
                document.getElementById('rewardsForm').reset();
                document.querySelector('.customer-info').style.display = 'none'; 
                const thankYouRewards = document.createElement('p');
                thankYouRewards.textContent = result.message || "Thank you for joining the rewards club!";
                thankYouRewards.style.textAlign = 'center';
                thankYouRewards.style.fontWeight = 'bold';
                document.querySelector('.customer-info').parentNode.insertBefore(thankYouRewards, document.querySelector('.cart-actions'));
            } else {
                alert(result.message || "Failed to join rewards club. Status: " + response.status);
                console.error("Failed to join rewards club:", result);
            }
        } catch (error) {
            console.error("Error submitting rewards info:", error);
            alert("An error occurred while submitting rewards info. Check the console for details.");
        }
    });

    sendToOvenBtn.addEventListener('click', async () => {
        console.log("Send to Oven button clicked");
        let totalPizzas = 0;
        const orderItems = [];

        for (const [summary, count] of Object.entries(orderCart)) {
            totalPizzas += count;
            orderItems.push({ description: summary, quantity: count });
        }

        if (totalPizzas === 0) {
            alert("Your cart is empty!");
            console.warn("Send to Oven validation failed: Cart is empty.");
            return;
        }

        const pizzaTime = 15 + (totalPizzas - 1) * 3;
        const pickUpTime = new Date(new Date().getTime() + pizzaTime * 60000);
        const pickUpTimeStr = pickUpTime.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });

        const orderData = {
            items: orderItems,
            totalAmount: null, 
            customerDetails: { 
                name: (document.getElementById('firstName').value + ' ' + document.getElementById('lastName').value).trim() || "Guest"
            }
        };
        console.log("Attempting to send order data:", orderData);

        try {
            const response = await fetch('http://localhost:3000/api/orders', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(orderData),
            });

            console.log("Order submission response status:", response.status);
            const responseText = await response.text(); // Get raw response text
            console.log("Order submission raw response text:", responseText);
            
            let result;
            try {
                result = JSON.parse(responseText); // Try to parse as JSON
            } catch (e) {
                console.error("Failed to parse order response as JSON:", e);
                alert("Received an invalid response from the server for order submission.");
                return;
            }

            console.log("Order submission parsed response:", result);

            if (response.ok && result.order) { // Check for result.order as well
                thankYouMessage.textContent = `Thank you for ordering with PizzaByU! Your order #${result.order.orderId} will be ready for pick up by ${pickUpTimeStr}.`;
                cartScreen.style.display = 'none';
                thankYouScreen.style.display = 'block';

                orderCart = {};
                resetSelections();
                document.getElementById('rewardsForm').reset();
                document.querySelector('.customer-info').style.display = 'block';
                const existingThankYouRewards = document.querySelector('.customer-info').parentNode.querySelector('p[style*="font-weight: bold"]');
                if (existingThankYouRewards) {
                    existingThankYouRewards.remove();
                }

                setTimeout(() => {
                    thankYouScreen.style.display = 'none';
                    menuScreen.style.display = 'block';
                }, 15000);
            } else {
                alert(result.message || "Failed to place order. Status: " + response.status);
                console.error("Failed to place order:", result);
            }
        } catch (error) {
            console.error("Error placing order:", error);
            alert("An error occurred while placing your order. Check the console for details.");
        }
    });

    // Initial setup
    menuScreen.style.display = 'block'; // Show menu screen by default

});
