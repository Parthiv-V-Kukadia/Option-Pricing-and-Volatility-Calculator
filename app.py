from flask import Flask, request, jsonify
import OptionsPricing  # Import the OptionsPricing.py script

app = Flask(__name__)

@app.route('/api/options-pricing', methods=['POST'])
def options_pricing():
    data = request.json
    stock_ticker = data['stock_ticker']
    strike_price = data['strike_price']
    time_to_maturity_weeks = data['time_to_maturity_weeks']
    volatility_choice = data['volatility_choice']
    implied_volatility = data.get('implied_volatility', None)

    # Get historical data
    historical_data = OptionsPricing.get_stock_data(stock_ticker)

    # Get current stock price
    current_price = historical_data['Close'].iloc[-1]

    # Get risk-free rate
    risk_free_rate = OptionsPricing.get_risk_free_rate(time_to_maturity_weeks)

    if volatility_choice == 'historical':
        historical_volatility = OptionsPricing.calculate_historical_volatility(historical_data, time_to_maturity_weeks)
        volatility = historical_volatility
    else:
        volatility = implied_volatility

    # Calculate option prices using Black-Scholes model
    bs_model = OptionsPricing.BlackScholesModel(current_price, strike_price, risk_free_rate, volatility, time_to_maturity_weeks * 7 / 365)
    call_price_bs = bs_model.call_option_price()
    put_price_bs = bs_model.put_option_price()

    # Calculate option prices using Monte Carlo simulation
    mc_model = OptionsPricing.MonteCarloOptionPricing(current_price, strike_price, risk_free_rate, volatility, time_to_maturity_weeks * 7 / 365, num_simulations=10000, num_steps=365)
    call_price_mc = mc_model.call_option_monte_carlo()
    put_price_mc = mc_model.put_option_monte_carlo()

    return jsonify({
        'call_price_bs': call_price_bs,
        'put_price_bs': put_price_bs,
        'call_price_mc': call_price_mc,
        'put_price_mc': put_price_mc
    })

if __name__ == '__main__':
    app.run(debug=True)
