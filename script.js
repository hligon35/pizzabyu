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
        currentOrder = getSelectedOptions();
        const summary = generateOrderSummary(currentOrder);
        if (!summary) {
            alert("Please make some selections first.");
            return;
        }
        previewText.textContent = summary;
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

    sendToOvenBtn.addEventListener('click', () => {
        let totalPizzas = 0;
        for (const count of Object.values(orderCart)) {
            totalPizzas += count;
        }

        if (totalPizzas === 0) {
            alert("Your cart is empty!");
            return;
        }

        const pizzaTime = 15 + (totalPizzas - 1) * 3;
        const pickUpTime = new Date(new Date().getTime() + pizzaTime * 60000);
        const pickUpTimeStr = pickUpTime.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });

        thankYouMessage.textContent = `Thank you for ordering with PizzaByU! Your order will be ready for pick up by ${pickUpTimeStr}.`;
        
        cartScreen.style.display = 'none';
        thankYouScreen.style.display = 'block';

        // Reset for next order
        orderCart = {};
        resetSelections();
        document.getElementById('rewardsForm').reset();

        setTimeout(() => {
            thankYouScreen.style.display = 'none';
            menuScreen.style.display = 'block'; // Or a greeting screen if you add one
        }, 15000);
    });

    submitRewardsBtn.addEventListener('click', () => {
        const firstName = document.getElementById('firstName').value;
        const lastName = document.getElementById('lastName').value;
        const address = document.getElementById('address').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;

        if (!firstName || !lastName || !address || !email || !phone) {
            alert("All fields are required for rewards club.");
            return;
        }

        // In a real app, you'd send this data to a server
        console.log("Rewards Info:", { firstName, lastName, address, email, phone });
        alert("Thank you for joining the rewards club!");
        document.getElementById('rewardsForm').reset();
        document.querySelector('.customer-info').style.display = 'none'; // Hide form
        const thankYouRewards = document.createElement('p');
        thankYouRewards.textContent = "Thank you for joining the rewards club!";
        thankYouRewards.style.textAlign = 'center';
        thankYouRewards.style.fontWeight = 'bold';
        document.querySelector('.customer-info').parentNode.insertBefore(thankYouRewards, document.querySelector('.cart-actions'));
    });

    // Initial setup
    menuScreen.style.display = 'block'; // Show menu screen by default

});
