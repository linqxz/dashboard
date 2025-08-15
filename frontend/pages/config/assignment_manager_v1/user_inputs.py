import streamlit as st


def user_inputs():
    """
    Create user input components for Assignment Manager Controller configuration.
    Returns a configuration dictionary with all the necessary parameters.
    """
    default_config = st.session_state.get("default_config", {})

    # Get default values from config or set sensible defaults
    connector_name = default_config.get("connector_name", "kraken_perpetual")
    trading_pairs = default_config.get("trading_pairs", ["BTC-USD", "ETH-USD", "SOL-USD"])
    all_trading_pairs = default_config.get("all_trading_pairs", False)
    order_type = default_config.get("order_type", "MARKET")
    close_percent = default_config.get("close_percent", 100.0)
    slippage_buffer = default_config.get("slippage_buffer", 0.1)
    max_order_age = default_config.get("max_order_age", 60)

    # Triple barrier defaults
    time_limit = default_config.get("time_limit", 0)
    stop_loss_pct = default_config.get("stop_loss_pct", None)
    take_profit_pct = default_config.get("take_profit_pct", None)
    trailing_stop_activation_pct = default_config.get("trailing_stop_activation_pct", None)
    trailing_stop_trailing_delta_pct = default_config.get("trailing_stop_trailing_delta_pct", None)

    # Basic Configuration
    with st.expander("📊 Exchange & Trading Configuration", expanded=True):
        c1, c2 = st.columns([1, 1])

        with c1:
            connector_name = st.selectbox(
                "Exchange Connector",
                ["kraken_perpetual", "binance_perpetual", "okx_perpetual", "bybit_perpetual", "kraken_perpetual_testnet"],
                index=0 if connector_name == "kraken_perpetual" else 0,
                help="Select the exchange connector for monitoring assignments"
            )

            order_type = st.selectbox(
                "Close Order Type",
                ["MARKET", "LIMIT"],
                index=0 if order_type == "MARKET" else 1,
                help="Order type for closing assigned positions"
            )

        with c2:
            all_trading_pairs = st.checkbox(
                "Monitor All Trading Pairs",
                value=all_trading_pairs,
                help="Monitor all trading pairs on the exchange (overrides specific pairs)"
            )

            close_percent = st.number_input(
                "Close Percentage (%)",
                min_value=1.0,
                max_value=100.0,
                value=close_percent,
                step=1.0,
                help="Percentage of assigned position to close (default: 100%)"
            )

    # Trading Pairs Configuration (only show if not monitoring all pairs)
    if not all_trading_pairs:
        with st.expander("🎯 Specific Trading Pairs", expanded=True):
            st.write("Configure specific trading pairs to monitor for assignments:")

            # Convert trading_pairs list to comma-separated string for easier input
            trading_pairs_str = ", ".join(trading_pairs) if trading_pairs else "BTC-USD, ETH-USD, SOL-USD"

            trading_pairs_input = st.text_area(
                "Trading Pairs (comma-separated)",
                value=trading_pairs_str,
                help="Enter trading pairs separated by commas (e.g., BTC-USD, ETH-USD, SOL-USD)",
                height=100
            )

            # Parse the input back to a list
            if trading_pairs_input.strip():
                trading_pairs = [pair.strip() for pair in trading_pairs_input.split(",") if pair.strip()]
            else:
                trading_pairs = []

            st.info(f"Monitoring {len(trading_pairs)} trading pairs: {', '.join(trading_pairs[:5])}"
                    f"{', ...'if len(trading_pairs) > 5 else ''}")

    # Order Management Configuration
    with st.expander("⚙️ Order Management", expanded=True):
        c1, c2 = st.columns([1, 1])

        with c1:
            slippage_buffer = st.number_input(
                "Slippage Buffer (%)",
                min_value=0.0,
                max_value=10.0,
                value=slippage_buffer,
                step=0.01,
                help="Slippage buffer for order execution (as percentage)"
            )

        with c2:
            max_order_age = st.number_input(
                "Max Order Age (seconds)",
                min_value=1,
                max_value=3600,
                value=max_order_age,
                step=1,
                help="Maximum age for orders before they're considered stale"
            )

    # Risk Management / Triple Barrier Configuration
    with st.expander("🛡️ Risk Management (Triple Barriers)", expanded=True):
        st.write("Configure risk management parameters for closing assigned positions:")

        c1, c2, c3 = st.columns([1, 1, 1])

        with c1:
            time_limit = st.number_input(
                "Time Limit (seconds)",
                min_value=0,
                value=time_limit,
                step=1,
                help="Time limit for position (0 = immediate close, >0 = enable barriers)"
            )

            # Stop Loss Configuration
            use_stop_loss = st.checkbox(
                "Enable Stop Loss",
                value=stop_loss_pct is not None and stop_loss_pct > 0,
                help="Enable stop loss protection"
            )

            if use_stop_loss:
                stop_loss_pct = st.number_input(
                    "Stop Loss (%)",
                    min_value=0.1,
                    max_value=100.0,
                    value=stop_loss_pct if stop_loss_pct is not None else 5.0,
                    step=0.1,
                    help="Stop loss percentage (e.g., 5.0 for 5% loss)"
                )
            else:
                stop_loss_pct = None

        with c2:
            # Take Profit Configuration
            use_take_profit = st.checkbox(
                "Enable Take Profit",
                value=take_profit_pct is not None and take_profit_pct > 0,
                help="Enable take profit target"
            )

            if use_take_profit:
                take_profit_pct = st.number_input(
                    "Take Profit (%)",
                    min_value=0.1,
                    max_value=100.0,
                    value=take_profit_pct if take_profit_pct is not None else 10.0,
                    step=0.1,
                    help="Take profit percentage (e.g., 10.0 for 10% profit)"
                )
            else:
                take_profit_pct = None

        with c3:
            # Trailing Stop Configuration
            use_trailing_stop = st.checkbox(
                "Enable Trailing Stop",
                value=(trailing_stop_activation_pct is not None and
                       trailing_stop_trailing_delta_pct is not None and
                       trailing_stop_activation_pct > 0 and
                       trailing_stop_trailing_delta_pct > 0),
                help="Enable trailing stop functionality"
            )

            if use_trailing_stop:
                trailing_stop_activation_pct = st.number_input(
                    "Activation (%)",
                    min_value=0.1,
                    max_value=100.0,
                    value=trailing_stop_activation_pct if trailing_stop_activation_pct is not None else 8.0,
                    step=0.1,
                    help="Profit percentage to activate trailing stop"
                )

                trailing_stop_trailing_delta_pct = st.number_input(
                    "Trailing Delta (%)",
                    min_value=0.1,
                    max_value=100.0,
                    value=trailing_stop_trailing_delta_pct if trailing_stop_trailing_delta_pct is not None else 2.0,
                    step=0.1,
                    help="Trailing stop delta percentage"
                )
            else:
                trailing_stop_activation_pct = None
                trailing_stop_trailing_delta_pct = None

    # Configuration Summary
    with st.expander("📋 Configuration Summary", expanded=False):
        st.write("**Exchange Configuration:**")
        st.write(f"- Connector: `{connector_name}`")
        st.write(f"- Monitor All Pairs: `{all_trading_pairs}`")
        if not all_trading_pairs:
            st.write(f"- Trading Pairs: `{', '.join(trading_pairs)}`")

        st.write("**Order Configuration:**")
        st.write(f"- Order Type: `{order_type}`")
        st.write(f"- Close Percentage: `{close_percent}%`")
        st.write(f"- Slippage Buffer: `{slippage_buffer}%`")
        st.write(f"- Max Order Age: `{max_order_age}s`")

        st.write("**Risk Management:**")
        st.write(f"- Time Limit: `{time_limit}s` ({'Immediate close' if time_limit == 0 else 'Barriers enabled'})")
        st.write(f"- Stop Loss: `{stop_loss_pct}%`" if stop_loss_pct else "- Stop Loss: `Disabled`")
        st.write(f"- Take Profit: `{take_profit_pct}%`" if take_profit_pct else "- Take Profit: `Disabled`")
        if trailing_stop_activation_pct and trailing_stop_trailing_delta_pct:
            st.write(f"- Trailing Stop: `{trailing_stop_activation_pct}%` / `{trailing_stop_trailing_delta_pct}%`")
        else:
            st.write("- Trailing Stop: `Disabled`")

    # Create the configuration dictionary
    config = {
        "controller_name": "assignment_manager_v1",
        "controller_type": "generic",
        "connector_name": connector_name,
        "trading_pairs": trading_pairs,
        "all_trading_pairs": all_trading_pairs,
        "order_type": order_type,
        "close_percent": close_percent,
        "slippage_buffer": slippage_buffer / 100.0,  # Convert to decimal
        "max_order_age": max_order_age,
        "time_limit": time_limit,
        "stop_loss_pct": stop_loss_pct,
        "take_profit_pct": take_profit_pct,
        "trailing_stop_activation_pct": trailing_stop_activation_pct,
        "trailing_stop_trailing_delta_pct": trailing_stop_trailing_delta_pct,
    }

    return config
