import streamlit as st

from frontend.components.config_loader import get_default_config_loader
from frontend.components.save_config import render_save_config

# Import submodules
from frontend.pages.config.assignment_manager_v1.user_inputs import user_inputs
from frontend.st_utils import get_backend_api_client, initialize_st_page

# Initialize the Streamlit page
initialize_st_page(title="Assignment Manager v1", icon=None, ms_icon="task")
backend_api_client = get_backend_api_client()

# Page content
st.title("Assignment Manager v1 Configuration")
st.markdown("""
This tool lets you create and manage configurations for the **Assignment Manager Controller**.

The Assignment Manager monitors your exchange for position assignments (like option assignments)
and automatically creates executors to close those positions using configurable risk management parameters.

**Key Features:**
- Exchange monitoring across supported exchanges
- Automated position closing on assignment
- Risk management: stop loss, take profit, trailing stops
- Flexible configuration for specific pairs or all pairs
""")

st.write("---")

# Load default configuration for this controller type
get_default_config_loader("assignment_manager_v1")

# Get user inputs
inputs = user_inputs()

# Update the session state with current inputs
st.session_state["default_config"].update(inputs)

# Display configuration visualization/summary
with st.expander("Live Configuration Preview", expanded=True):
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Exchange Setup")
        st.code(
            f"""
Connector: {inputs["connector_name"]}
Monitor All Pairs: {inputs["all_trading_pairs"]}
"""
            + (
                f"Specific Pairs: {len(inputs['trading_pairs'])} pairs"
                if not inputs["all_trading_pairs"]
                else ""
            ),
            language="yaml",
        )

        st.subheader("Order Management")
        st.code(
            f"""
Order Type: {inputs["order_type"]}
Close Percentage: {inputs["close_percent"]}%
Slippage Buffer: {inputs["slippage_buffer"] * 100:.3f}%
Max Order Age: {inputs["max_order_age"]}s
""",
            language="yaml",
        )

    with col2:
        st.subheader("Risk Management")

        # Show risk management configuration
        risk_config = f"Time Limit: {inputs['time_limit']}s"
        if inputs["time_limit"] == 0:
            risk_config += " (Immediate close)"
        else:
            risk_config += " (Barriers enabled)"

        risk_config += "\nStop Loss: "
        risk_config += (
            f"{inputs['stop_loss_pct']}%" if inputs["stop_loss_pct"] else "Disabled"
        )

        risk_config += "\nTake Profit: "
        risk_config += (
            f"{inputs['take_profit_pct']}%" if inputs["take_profit_pct"] else "Disabled"
        )

        risk_config += "\nTrailing Stop: "
        if (
            inputs["trailing_stop_activation_pct"]
            and inputs["trailing_stop_trailing_delta_pct"]
        ):
            risk_config += f"{inputs['trailing_stop_activation_pct']}% / {inputs['trailing_stop_trailing_delta_pct']}%"
        else:
            risk_config += "Disabled"

        st.code(risk_config, language="yaml")

        # Show trading pairs if not monitoring all
        if not inputs["all_trading_pairs"] and inputs["trading_pairs"]:
            st.subheader("Monitored Pairs")
            pairs_text = "\n".join(
                [f"- {pair}" for pair in inputs["trading_pairs"][:10]]
            )
            if len(inputs["trading_pairs"]) > 10:
                pairs_text += f"\n... and {len(inputs['trading_pairs']) - 10} more"
            st.code(pairs_text, language="yaml")

# Configuration warnings and validation
warning_messages = []
info_messages = []

# Validate configuration
if not inputs["all_trading_pairs"] and not inputs["trading_pairs"]:
    warning_messages.append(
        "No trading pairs specified. Please enable 'Monitor All Trading Pairs' or specify specific pairs."
    )

if inputs["time_limit"] == 0:
    info_messages.append(
        "Time limit is set to 0 - positions will be closed immediately upon assignment."
    )

if inputs["close_percent"] < 100:
    info_messages.append(
        f"Only {inputs['close_percent']}% of assigned positions will be closed."
    )

# Risk management validation
if inputs["time_limit"] > 0:
    risk_features = []
    if inputs["stop_loss_pct"]:
        risk_features.append("Stop Loss")
    if inputs["take_profit_pct"]:
        risk_features.append("Take Profit")
    if (
        inputs["trailing_stop_activation_pct"]
        and inputs["trailing_stop_trailing_delta_pct"]
    ):
        risk_features.append("Trailing Stop")

    if risk_features:
        info_messages.append(f"Risk management active: {', '.join(risk_features)}")
    else:
        warning_messages.append(
            "Time limit is enabled but no risk management features are configured."
        )

# Display warnings and info
if warning_messages:
    for msg in warning_messages:
        st.warning(msg)

if info_messages:
    for msg in info_messages:
        st.info(msg)

# Usage instructions
with st.expander("Usage Instructions", expanded=False):
    st.markdown("""
    ### How the Assignment Manager Works

    1. **Exchange Monitoring**: The controller connects to your specified exchange and listens for assignment events
    2. **Assignment Detection**: When an assignment occurs (e.g., option assignment), it's automatically detected
    3. **Executor Creation**: An executor is created to close the assigned position according to your configuration
    4. **Risk Management**: The executor uses your configured barriers (stop loss, take profit, trailing stop)
    to manage the position

    ### Configuration Tips

    #### Exchange Configuration
    - **Monitor All Trading Pairs**: Enable this if you want to monitor all available pairs on the exchange
    - **Specific Trading Pairs**: Use this for targeted monitoring of specific instruments

    #### Order Management
    - **Market Orders**: Faster execution but potential slippage
    - **Limit Orders**: Better price control but risk of non-execution
    - **Close Percentage**: Set to less than 100% if you want to keep part of the assigned position

    #### Risk Management
    - **Time Limit = 0**: Positions close immediately (market conditions permitting)
    - **Time Limit > 0**: Enables barrier-based position management
    - **Stop Loss**: Protects against losses beyond your tolerance
    - **Take Profit**: Locks in profits at your target level
    - **Trailing Stop**: Follows profitable positions while protecting gains

    ### Supported Exchanges
    - Kraken Perpetual (primary)
    - Binance Perpetual
    - OKX Perpetual
    - Bybit Perpetual

    ### Best Practices
    - Start with conservative risk management settings
    - Test with smaller position sizes first
    - Monitor the dashboard for assignment activity
    - Ensure sufficient balance for margin requirements
    """)

st.write("---")

# Render the save configuration section
render_save_config(
    st.session_state["default_config"]["id"], st.session_state["default_config"]
)
