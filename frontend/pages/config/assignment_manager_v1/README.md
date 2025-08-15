# Assignment Manager v1 Configuration

This module provides a Streamlit-based configuration interface for the Assignment Manager v1 controller.

## Overview

The Assignment Manager v1 controller monitors exchanges for position assignments (such as option assignments) and automatically creates executors to close those positions using configurable risk management parameters.

## Files

- `app.py`: Main Streamlit application page
- `user_inputs.py`: User input components and configuration logic
- `README.md`: This documentation file

## Features

### Exchange Configuration
- **Connector Selection**: Choose from supported exchanges (Kraken Perpetual, Binance Perpetual, OKX Perpetual, Bybit Perpetual)
- **Trading Pair Monitoring**: Monitor all trading pairs or specify specific pairs
- **Flexible Setup**: Configure for various trading scenarios

### Order Management
- **Order Types**: Market or Limit orders for closing positions
- **Position Control**: Configure what percentage of assigned positions to close
- **Slippage Protection**: Built-in slippage buffer for market orders
- **Order Age Limits**: Prevent stale order execution

### Risk Management (Triple Barriers)
- **Time Limits**: Immediate close or time-based position management
- **Stop Loss**: Configurable loss protection
- **Take Profit**: Automated profit-taking at target levels
- **Trailing Stops**: Dynamic profit protection that follows favorable price movements

## Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `connector_name` | str | "kraken_perpetual" | Exchange connector to monitor |
| `trading_pairs` | List[str] | ["BTC-USD", "ETH-USD", "SOL-USD"] | Specific trading pairs to monitor |
| `all_trading_pairs` | bool | False | Monitor all available trading pairs |
| `order_type` | str | "MARKET" | Order type for closing positions |
| `close_percent` | float | 100.0 | Percentage of assigned position to close |
| `slippage_buffer` | float | 0.001 | Slippage buffer for order execution |
| `max_order_age` | int | 60 | Maximum order age in seconds |
| `time_limit` | int | 0 | Time limit for position (0 = immediate close) |
| `stop_loss_pct` | float/None | None | Stop loss percentage |
| `take_profit_pct` | float/None | None | Take profit percentage |
| `trailing_stop_activation_pct` | float/None | None | Trailing stop activation percentage |
| `trailing_stop_trailing_delta_pct` | float/None | None | Trailing stop delta percentage |

## Usage

1. Navigate to the Assignment Manager v1 configuration page in the dashboard
2. Configure exchange and trading pair settings
3. Set order management parameters
4. Configure risk management (triple barriers)
5. Review the configuration summary
6. Save the configuration to the backend

## Risk Management Modes

### Immediate Close (time_limit = 0)
- Positions are closed immediately upon assignment
- No barriers are used
- Fastest response to assignments

### Barrier-Based Management (time_limit > 0)
- Enables stop loss, take profit, and trailing stop functionality
- Provides sophisticated risk management
- Allows for profit optimization

## Best Practices

1. **Start Conservative**: Begin with tight stop losses and conservative settings
2. **Test Thoroughly**: Use small position sizes when testing new configurations
3. **Monitor Activity**: Keep an eye on the dashboard for assignment events
4. **Maintain Margins**: Ensure sufficient balance for margin requirements
5. **Review Performance**: Regularly assess the effectiveness of your settings

## Support

For issues or questions about the Assignment Manager v1 configuration:
1. Check the dashboard logs for assignment activity
2. Verify exchange connectivity and credentials
3. Review trading pair availability on your selected exchange
4. Ensure proper risk management configuration