<script>
    import { onMount } from 'svelte';
    let userInput = '';
    let totals = { burger: 0, fries: 0, drink: 0 };
    let orders = [];

    async function fetchSummary() {
        try {
            const res = await fetch('http://localhost:8000/get_summary');
            const data = await res.json();
            console.log('Fetched Data:', data); // Log the fetched data
            totals = data.totals;              // Update totals
            orders = data.orders;              // Update orders
        } catch (error) {
            console.error('Error fetching summary:', error);
        }
    }

    async function handleRequest() {
        await fetch('http://localhost:8000/parse_request', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userInput }),
        });

        await fetchSummary();
        userInput = '';
    }

    onMount(() => {
        console.log('Fetching summary...');
        fetchSummary().then(() => {
            console.log('Updated orders:', orders);
        });
    }); 
</script>


<style>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        height: 100vh; /* Full viewport height */
        display: flex;
        justify-content: center; /* Horizontally center */
        align-items: center; /* Vertically center */
        background-color: #f9f9f9; /* Optional background color */
    }

    main {
        width: 80%;
        max-width: 800px;
        background: #fff; /* Optional white background */
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optional shadow */
        padding: 20px;
        text-align: center; /* Center text inside elements */
    }

    .totals-container {
        display: flex;
        justify-content: space-between;
        width: 80%;
        margin-bottom: 20px;
    }

    .total-box {
        width: 30%;
        padding: 20px;
        border: 2px solid #ccc;
        border-radius: 8px;
        text-align: center;
        font-size: 18px;
        background-color: #f9f9f9;
    }

    .input-container {
        width: 80%;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
    }

    .input-container textarea {
        flex: 1;
        padding: 10px;
        font-size: 16px;
        border: 2px solid #ccc;
        border-radius: 8px;
        resize: none;
        height: 60px;
    }

    .input-container button {
        margin-left: 10px;
        padding: 10px 20px;
        font-size: 16px;
        border: 2px solid #ccc;
        border-radius: 50%;
        background-color: #eee;
        cursor: pointer;
    }

    .input-container button:hover {
        background-color: #ddd;
    }

    .order-history {
        width: 80%;
        margin-top: 20px;
    }

    .order-history h3 {
        font-size: 20px;
        margin-bottom: 10px;
    }

    .order {
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #ccc;
        border-radius: 8px;
        background-color: #f9f9f9;
        display: flex;
        justify-content: space-between;
    }

    .order span {
        font-size: 16px;
    }
</style>

<main>
    <!-- Totals Section -->
    <div class="totals-container">
        <div class="total-box">Total Burgers: {totals.burger}</div>
        <div class="total-box">Total Fries: {totals.fries}</div>
        <div class="total-box">Total Drinks: {totals.drink}</div>
    </div>

    <!-- Input Section -->
    <div class="input-container">
        <textarea
            placeholder="Drive thru message:&#10;Ex: 'I would like one burger and an order of fries',&#10;'Cancel order #2'"
            bind:value={userInput}></textarea>
        <button on:click={handleRequest}>Run</button>
    </div>

    <!-- Order History -->
    <div class="order-history">
        <h3>Order History</h3>
        {#if orders && orders.length > 0}
            {#each orders as orderGroup}
                <div>
                    {#each orderGroup.items as order}
                        <div class="order">
                            <span>Order #{orderGroup.id}</span>
                            <span>
                                {order.items.map(item => `${item.quantity} ${item.item}`).join(', ')}
                            </span>
                        </div>
                    {/each}
                </div>
            {/each}
        {:else}
            <p>No orders found.</p>
        {/if}
    </div>
</main>
