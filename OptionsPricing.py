import yfinance as yf
import mibian
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import erf

# Function to get stock data and plot
def get_stock_data(ticker, period='5y'):
    ticker_data = yf.Ticker(ticker)
    historical_data = ticker_data.history(period=period)  # Retrieving historical data based on the specified period

    historical_data = historical_data.sort_index(ascending=False)
    print(historical_data.head())

    plt.figure(figsize=(10, 6))
    plt.plot(historical_data.index, historical_data['Close'], label='Close Price')
    plt.title(f'{ticker} Stock Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

    return historical_data

# Function to calculate historical volatility based on user-defined time frame
def calculate_historical_volatility(historical_data, weeks_to_maturity):
    # Calculate daily returns
    historical_data['Returns'] = historical_data['Close'].pct_change()

    # Determine the period for volatility calculation
    if weeks_to_maturity > 52:  # More than 1 year
        historical_data = historical_data.tail(3 * 252)  # Use the last 3 years of data
        period = len(historical_data)  # Use all available data for volatility calculation
    elif weeks_to_maturity < 4:
        # Short-term historical volatility (10-30 days)
        period = 20  # Average of 10-30 days
    elif 4 <= weeks_to_maturity <= 12:
        # Medium-term historical volatility (30-90 days)
        period = 60  # Average of 30-90 days
    else:
        # Long-term historical volatility (90-365 days)
        period = 180  # Average of 90-365 days

    # Calculate historical volatility
    volatility = historical_data['Returns'].tail(period).std() * np.sqrt(252)  # Annualized volatility
    return volatility

# Function to get risk-free rate based on time to maturity
def get_risk_free_rate(time_to_maturity_weeks):
    if time_to_maturity_weeks <= 12:
        bond_ticker = '^IRX'  # 13-week Treasury bill
    else:
        bond_ticker = '^TNX'  # 10-Year Treasury yield
    
    bond_data = yf.Ticker(bond_ticker)
    bond_history = bond_data.history(period='1d')
    risk_free_rate = bond_history['Close'].iloc[-1] / 100  # Convert percentage to decimal
    rate_type = "short-term" if time_to_maturity_weeks <= 12 else "long-term"
    
    print(f"Risk-free interest rate ({rate_type}): {risk_free_rate * 100:.2f}%")
    return risk_free_rate

# Class for the Black-Scholes Model
class BlackScholesModel:
    def __init__(self, spot_price, strike_price, risk_free_rate, volatility, time_to_maturity):
        self.S = spot_price
        self.K = strike_price
        self.r = risk_free_rate
        self.sigma = volatility
        self.T = time_to_maturity

    def calculate_d1(self):
        numerator = np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T
        denominator = self.sigma * np.sqrt(self.T)
        return numerator / denominator

    def calculate_d2(self, d1):
        return d1 - self.sigma * np.sqrt(self.T)

    def call_option_price(self):
        d1 = self.calculate_d1()
        d2 = self.calculate_d2(d1)
        option_price = (self.S * self.N(d1)) - (self.K * np.exp(-self.r * self.T) * self.N(d2))
        return option_price

    def put_option_price(self):
        d1 = self.calculate_d1()
        d2 = self.calculate_d2(d1)
        option_price = (self.K * np.exp(-self.r * self.T) * self.N(-d2)) - (self.S * self.N(-d1))
        return option_price

    def N(self, x):
        return (1 + erf(x / np.sqrt(2))) / 2

# Class for Monte Carlo Option Pricing
class MonteCarloOptionPricing:
    def __init__(self, spot_price, strike_price, risk_free_rate, volatility, time_to_maturity, num_simulations, num_steps):
        self.S = spot_price
        self.K = strike_price
        self.r = risk_free_rate
        self.sigma = volatility
        self.T = time_to_maturity
        self.N = num_simulations
        self.M = num_steps

    def generate_price_paths(self):
        dt = self.T / self.M
        price_matrix = np.zeros((self.M + 1, self.N))
        price_matrix[0] = self.S
        for t in range(1, self.M + 1):
            rand_values = np.random.randn(self.N)
            price_matrix[t] = price_matrix[t - 1] * np.exp((self.r - 0.5 * self.sigma ** 2) * dt + self.sigma * np.sqrt(dt) * rand_values)
        return price_matrix

    def call_option_monte_carlo(self):
        price_matrix = self.generate_price_paths()
        payoffs = np.maximum(price_matrix[-1] - self.K, 0)
        option_price = np.exp(-self.r * self.T) * 1/self.N * np.sum(payoffs)
        return option_price

    def put_option_monte_carlo(self):
        price_matrix = self.generate_price_paths()
        payoffs = np.maximum(self.K - price_matrix[-1], 0)
        option_price = np.exp(-self.r * self.T) * 1/self.N * np.sum(payoffs)
        return option_price

# Main script
if __name__ == "__main__":
    stock_ticker = input("Enter the stock ticker symbol (e.g., AAPL): ")
    historical_data = get_stock_data(stock_ticker)

    # Get current stock price
    ticker_data = yf.Ticker(stock_ticker)
    current_price = ticker_data.history(period='1d')['Close'].iloc[-1]
    print(f"Current stock price: {current_price}")

    # Ask for the strike price and time to maturity in weeks
    strike_price = float(input("Enter the option strike price: "))
    time_to_maturity_weeks = float(input("Enter the time to option maturity (in weeks): "))

    # Calculate the risk-free interest rate
    risk_free_rate = get_risk_free_rate(time_to_maturity_weeks)

    # Ask the user whether they want to calculate option price or implied volatility
    choice = input("Do you want to calculate the (1) option price or (2) implied volatility? Enter 1 or 2: ")

    if choice == '1':
        # Ask the user to choose between historical or implied volatility
        vol_choice = input("Do you want to use (1) historical volatility or (2) implied volatility? Enter 1 or 2: ")
        
        if vol_choice == '1':
            # Calculate historical volatility
            historical_volatility = calculate_historical_volatility(historical_data, time_to_maturity_weeks)
            volatility = historical_volatility * 100  # Historical volatility
            print(f"Historical volatility: {volatility:.2f}%")
        else:
            # Ask the user to provide implied volatility
            implied_volatility = float(input("Enter the implied volatility (as a percentage, e.g., 25 for 25%): "))
            volatility = implied_volatility

        # Convert volatility to decimal and time to years
        volatility_decimal = volatility / 100
        time_to_maturity_years = time_to_maturity_weeks * 7 / 365

        # Calculate option prices using Black-Scholes model
        bs_model = BlackScholesModel(current_price, strike_price, risk_free_rate, volatility_decimal, time_to_maturity_years)
        call_price_bs = bs_model.call_option_price()
        put_price_bs = bs_model.put_option_price()
        print(f"Call Option Price (Black-Scholes): {call_price_bs:.2f}")
        print(f"Put Option Price (Black-Scholes): {put_price_bs:.2f}")

        # Calculate option prices using Monte Carlo simulation
        mc_model = MonteCarloOptionPricing(current_price, strike_price, risk_free_rate, volatility_decimal, time_to_maturity_years, num_simulations=10000, num_steps=365)
        call_price_mc = mc_model.call_option_monte_carlo()
        put_price_mc = mc_model.put_option_monte_carlo()
        print(f"Call Option Price (Monte Carlo): {call_price_mc:.2f}")
        print(f"Put Option Price (Monte Carlo): {put_price_mc:.2f}")

    elif choice == '2':
        # Ask the user to provide either the call or put price
        option_type = input("Is this for a (1) Call option or (2) Put option? Enter 1 or 2: ")
        market_price = float(input("Enter the market price of the option: "))
        
        if option_type == '1':
            option = mibian.BS([current_price, strike_price, risk_free_rate * 100, time_to_maturity_weeks * 7], callPrice=market_price)
        else:
            option = mibian.BS([current_price, strike_price, risk_free_rate * 100, time_to_maturity_weeks * 7], putPrice=market_price)
        
        implied_volatility = option.impliedVolatility
        print(f"Implied Volatility: {implied_volatility:.2f}%")
