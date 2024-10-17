document.getElementById('option-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent default form submission

    // Get form values
    const stockTicker = document.getElementById('stock-ticker').value;
    const strikePrice = parseFloat(document.getElementById('strike-price').value);
    const timeToMaturityWeeks = parseFloat(document.getElementById('time-to-maturity').value);
    const volatilityChoice = document.querySelector('input[name="volatility"]:checked').value;
    let impliedVolatility = null;

    if (volatilityChoice === 'implied') {
        impliedVolatility = parseFloat(document.getElementById('implied-volatility').value);
    }

    // Send POST request to the Flask API
    fetch('/api/options-pricing', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            stock_ticker: stockTicker,
            strike_price: strikePrice,
            time_to_maturity_weeks: timeToMaturityWeeks,
            volatility_choice: volatilityChoice,
            implied_volatility: impliedVolatility,
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Display results
        document.getElementById('call-price-bs').textContent = `Call Price (BS): ${data.call_price_bs.toFixed(2)}`;
        document.getElementById('put-price-bs').textContent = `Put Price (BS): ${data.put_price_bs.toFixed(2)}`;
        document.getElementById('call-price-mc').textContent = `Call Price (MC): ${data.call_price_mc.toFixed(2)}`;
        document.getElementById('put-price-mc').textContent = `Put Price (MC): ${data.put_price_mc.toFixed(2)}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
