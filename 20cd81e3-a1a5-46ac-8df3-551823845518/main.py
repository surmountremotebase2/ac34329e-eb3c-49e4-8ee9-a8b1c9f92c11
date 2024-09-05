from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the stock ticker to be traded.
        self.ticker = "AAPL"
    
    @property
    def interval(self):
        # Define the interval for data collection.
        return "1day"
    
    @property
    def assets(self):
        # Define the asset being traded.
        return [self.ticker]
    
    def run(self, data):
        # Define the allocation object with initial no holdings.
        allocation_dict = {self.ticker: 0}
        
        # Calculate the 14-day RSI for the stock.
        rsi_values = RSI(self.ticker, data["ohlcv"], 14)
        
        if rsi_values is not None and len(rsi_values) > 0:
            # Check the current RSI value.
            current_rsi = rsi_values[-1]
            
            # Define oversold and overbought thresholds.
            oversold_threshold = 30
            overbought_threshold = 70
            
            # If the stock is oversold, buy (1 = 100% of portfolio).
            if current_rsi < oversold_threshold:
                allocation_dict[self.ticker] = 1
                log(f"Buying {self.ticker}, RSI is oversold at {current_rsi}")
            
            # If the stock is overbought, sell (0 = 0% of portfolio).
            elif current_rsi > overbought_threshold:
                allocation_dict[self.ticker] = 0
                log(f"Selling {self.ticker}, RSI is overbought at {current_rsi}")
            else:
                # Hold if the RSI is between the two thresholds.
                log(f"RSI is neutral at {current_rsi}, holding position.")
        else:
            # If RSI data is not available, log a message.
            log(f"RSI data not available for {self.ticker}")
        
        # Return the target allocation based on RSI signal.
        return TargetAllocation(allocation_dict)