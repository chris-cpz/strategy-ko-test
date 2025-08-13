#!/usr/bin/env python3
"""
KO TEST - Custom Trading Strategy

Strategy Type: custom
Description: KO TEST
Created: 2025-08-13T16:05:56.584Z

WARNING: This is a template implementation. Thoroughly backtest before live trading.
"""

import os
import sys
import logging
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('strategy.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class KOTESTStrategy:
    """
    KO TEST Implementation
    
    Strategy Type: custom
    Risk Level: Monitor drawdowns and position sizes carefully
    """
    
    def __init__(self, config=None):
        self.config = config or self.get_default_config()
        self.positions = {}
        self.performance_metrics = {}
        logger.info(f"Initialized KO TEST strategy")
        
    def get_default_config(self):
        """Default configuration parameters"""
        return {
            'max_position_size': 0.05,  # 5% max position size
            'stop_loss_pct': 0.05,      # 5% stop loss
            'lookback_period': 20,       # 20-day lookback
            'rebalance_freq': 'daily',   # Rebalancing frequency
            'transaction_costs': 0.001,  # 0.1% transaction costs
        }
    
    def load_data(self, symbols, start_date, end_date):
        """Load market data for analysis"""
        try:
            import yfinance as yf
            data = yf.download(symbols, start=start_date, end=end_date)
            logger.info(f"Loaded data for {len(symbols)} symbols")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None

# =============================================================================
# USER'S STRATEGY IMPLEMENTATION
# =============================================================================

#!/usr/bin/env python3
"""
Simplest strategy.py — single-run, no inputs, paper by default (alpaca-py)

Rules (US/Eastern):
- Before 10:00 AM ET  -> BUY  1 KO (market, DAY)
- After  10:00 AM ET  -> SELL 1 KO (market, DAY)
- Exactly 10:00 AM ET -> no action

Requires env vars:
  APCA_API_KEY_ID, APCA_API_SECRET_KEY
"""

import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# --- Configuration (no user inputs) ---
SYMBOL = "KO"
QTY = 1
TZ_ET = ZoneInfo("US/Eastern")

API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")

if not API_KEY or not API_SECRET:
    sys.exit("Missing API credentials. Set APCA_API_KEY_ID and APCA_API_SECRET_KEY in your environment.")

# Always paper trading
client = TradingClient(API_KEY, API_SECRET, paper=True)

def market_is_open() -> bool:
    try:
        return bool(client.get_clock().is_open)
    except Exception as e:
        print(f"Could not read market clock: {e}")
        return False

def place(side: OrderSide):
    order = MarketOrderRequest(
        symbol=SYMBOL,
        qty=QTY,
        side=side,
        time_in_force=TimeInForce.DAY,  # market order -> market price
    )
    submitted = client.submit_order(order)
    print(f"{datetime.now(TZ_ET).isoformat()}  {side.name} {QTY} {SYMBOL}  order_id={submitted.id}")

def main():
    now_et = datetime.now(TZ_ET)
    ten_am = now_et.replace(hour=10, minute=0, second=0, microsecond=0).time()

    if not market_is_open():
        print(f"[{now_et}] Market is closed. No action.")
        return

    if now_et.time() < ten_am:
        print(f"[{now_et}] Before 10:00 AM ET -> BUY")
        place(OrderSide.BUY)
    elif now_et.time() > ten_am:
        print(f"[{now_et}] After 10:00 AM ET -> SELL")
        place(OrderSide.SELL)
    else:
        print(f"[{now_et}] Exactly 10:00 AM ET -> no action")

if __name__ == "__main__":
    main()


# =============================================================================
# STRATEGY EXECUTION AND TESTING
# =============================================================================

if __name__ == "__main__":
    # Example usage and testing
    strategy = KOTESTStrategy()
    print(f"Strategy '{strategyName}' initialized successfully!")
    
    # Example data loading
    symbols = ['SPY', 'QQQ', 'IWM']
    start_date = '2020-01-01'
    end_date = '2023-12-31'
    
    print(f"Loading data for symbols: {symbols}")
    data = strategy.load_data(symbols, start_date, end_date)
    
    if data is not None:
        print(f"Data loaded successfully. Shape: {data.shape}")
        print("Strategy ready for backtesting!")
    else:
        print("Failed to load data. Check your internet connection.")
