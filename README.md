# Options Pricing and Volatility Calculator
This Python script allows users to calculate stock option prices using the Black-Scholes model and Monte Carlo simulation. It also provides the functionality to calculate implied volatility based on the market price of an option. The script fetches historical stock data and the current risk-free interest rate using the `yfinance` library.

## Features

* **Historical Stock Data:** Retrieves historical stock prices for a given ticker symbol from Yahoo Finance and displays a closing price chart.
* **Historical Volatility Calculation:** Estimates historical volatility based on the closing prices over a user-defined or dynamically determined time frame related to the option's time to maturity.
* **Risk-Free Rate Retrieval:** Fetches the current risk-free interest rate using short-term (13-week Treasury bill) or long-term (10-Year Treasury yield) data from Yahoo Finance, depending on the option's time to maturity.
* **Black-Scholes Option Pricing:** Implements the Black-Scholes model to calculate the theoretical prices of call and put options.
* **Monte Carlo Option Pricing:** Uses Monte Carlo simulation to estimate call and put option prices.
* **Implied Volatility Calculation:** Calculates the implied volatility of an option given its market price using the `mibian` library.

## Prerequisites

Before running the script, ensure you have the following Python libraries installed:

```bash
pip install yfinance mibian numpy pandas matplotlib scipy
```

How to Run the Script
1. Save the code: Save the provided Python code as a .py file (e.g., option_pricing.py).
2. Open a terminal or command prompt: Navigate to the directory where you saved the file.
3. Run the script: Execute the script using the Python interpreter:
```bash
python option_pricing.py
```
4. Follow the prompts: The script will guide you through the following steps:
    * **Enter Stock Ticker:** You will be asked to enter the ticker symbol of the stock you are interested in (e.g., AAPL for Apple). The script will then fetch and display the historical stock prices for the last 5 years.
    * **Enter Option Details:** You will be prompted to enter the strike price and the time to option maturity in weeks.
    * **Calculate Price or Implied Volatility:** You will be asked whether you want to calculate the option price or the implied volatility.
        * If you choose to calculate the option price:
            * You will be asked whether to use historical volatility or provide implied volatility.
            * If you choose historical volatility, the script will calculate it based on the historical data and the time to maturity.
            * If you choose implied volatility, you will need to enter it as a percentage.
            * The script will then calculate and display the call and put option prices using both the Black-Scholes model and Monte Carlo simulation.
        * If you choose to calculate implied volatility:
            * You will be asked whether it's for a call or a put option.
            * You will need to enter the current market price of the option.
            * The script will then calculate and display the implied volatility.

## Example Usage
Enter the stock ticker symbol (e.g., AAPL): AAPL
[Prints historical stock data and displays a chart]
Current stock price: 170.34
Enter the option strike price: 175
Enter the time to option maturity (in weeks): 8
Risk-free interest rate (short-term): 4.92%
Do you want to calculate the (1) option price or (2) implied volatility? Enter 1 or 2: 1
Do you want to use (1) historical volatility or (2) implied volatility? Enter 1 or 2: 1
Historical volatility: 22.56%
Call Option Price (Black-Scholes): 3.47
Put Option Price (Black-Scholes): 8.09
Call Option Price (Monte Carlo): 3.58
Put Option Price (Monte Carlo): 8.19

OR:

Enter the stock ticker symbol (e.g., AAPL): AAPL
[Prints historical stock data and displays a chart]
Current stock price: 170.34
Enter the option strike price: 175
Enter the time to option maturity (in weeks): 8
Risk-free interest rate (short-term): 4.92%
Do you want to calculate the (1) option price or (2) implied volatility? Enter 1 or 2: 2
Is this for a (1) Call option or (2) Put option? Enter 1 or 2: 1
Enter the market price of the option: 4.50
Implied Volatility: 25.67%

## Notes
* The historical volatility calculation is based on a simplified approach that considers different time frames relative to the option's maturity.
    * More sophisticated methods might involve different weighting schemes or models.
* The risk-free rate is approximated using the yields of Treasury bills or notes.
    * The most appropriate rate might depend on the specific context and the term structure of interest rates.
* The Monte Carlo simulation uses a fixed number of simulations and steps.
    * Increasing these values can improve the accuracy of the results but will also increase the computation time.
* The implied volatility calculation relies on the `mibian` library, which uses numerical methods to find the volatility that equates the Black-Scholes price to the market price.
* Ensure you have a stable internet connection to fetch data from Yahoo Finance.
          
