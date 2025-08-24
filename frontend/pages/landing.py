import random
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from frontend.st_utils import initialize_st_page

initialize_st_page(layout="wide", show_readme=False, ms_icon="dashboard")

# Custom CSS for enhanced styling
st.markdown(
    """
<style>
    .hero {
        position: relative;
        padding: 2.25rem 0 1.25rem;
        text-align: center;
        overflow: hidden;
    }

    .hero h1 {
        font-size: 2.8rem;
        line-height: 1.1;
        margin: 0;
        color: var(--text);
        letter-spacing: -0.01em;
    }

    .hero p {
        color: var(--muted);
        margin-top: 0.75rem;
        font-size: 1.1rem;
    }

    .chip-row { margin-top: 1rem; display: inline-flex; gap: .5rem; }
    .chip {
        font-size: .85rem; color: var(--text); font-weight: 600;
        background: var(--card);
        border: 1px solid var(--border);
        padding: .35rem .6rem; border-radius: 999px;
    }

    .card {
        background: var(--surface-1);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1rem;
    }

    .section-title {
        font-weight: 700; font-size: 1.2rem; margin: 0 0 .75rem 0;
    }

    .kpi-card {
        background: linear-gradient(180deg, rgba(124,58,237,0.22) 0%, rgba(124,58,237,0.06) 100%);
        border: 1px solid rgba(139,92,246,0.35);
        border-radius: 14px; padding: 1rem;
    }
    .kpi-label { color: var(--muted); font-size: .95rem; }
    .kpi-value { font-size: 2rem; font-weight: 700; letter-spacing: -0.01em; }
    .kpi-delta { color: var(--success); font-weight: 600; font-size: .95rem; }

    .status-badge { font-weight: 700; }
    .status-active { color: var(--success); }
    .status-inactive { color: var(--danger); }

    .feature-card {
        background: var(--surface-1);
        border: 1px solid var(--border);
        border-radius: 14px; padding: 1.25rem;
        transition: transform .2s ease, border-color .2s ease;
    }
    .feature-card:hover { transform: translateY(-2px); border-color: rgba(139,92,246,0.6); }

    .quick-actions .qa-btn {
        display: block; width: 100%; text-align: center; text-decoration: none;
        background: linear-gradient(180deg, rgba(34,211,238,0.15) 0%, rgba(124,58,237,0.12) 100%);
        border: 1px solid var(--border); border-radius: 12px; padding: .9rem 1rem;
        color: var(--text); font-weight: 600;
    }

    .muted { color: var(--muted); }
</style>
""",
    unsafe_allow_html=True,
)

# Hero Section
st.markdown(
    """
<div class="hero">
    <h1>Hummingbot Dashboard</h1>
    <p>Your command center for algorithmic trading and bot orchestration</p>
    <div class="chip-row">
        <span class="chip">Open Source</span>
        <span class="chip">Strategy Builder</span>
        <span class="chip">Performance Analytics</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# Generate sample data for demonstration
def generate_sample_data():
    """Generate sample trading data for visualization"""
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=30), end=datetime.now(), freq="D"
    )

    # Sample portfolio performance
    portfolio_values = []
    base_value = 10000
    for i in range(len(dates)):
        change = random.uniform(-0.02, 0.03)  # -2% to +3% daily change
        base_value *= 1 + change
        portfolio_values.append(base_value)

    return pd.DataFrame(
        {
            "date": dates,
            "portfolio_value": portfolio_values,
            "daily_return": [random.uniform(-0.05, 0.08) for _ in range(len(dates))],
        }
    )


# Quick Stats Dashboard
st.markdown("### Live Dashboard Overview")

# Mock data warning
st.warning("""
⚠️ **Demo Data Notice**: The metrics, charts, and statistics shown below are
simulated/mocked data for demonstration purposes.
This showcases how real trading data would be presented in the dashboard once connected to live trading bots.
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-label">Active Bots</div>
            <div class="kpi-value">3</div>
            <div class="kpi-delta">● Currently trading</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
    <div class="kpi-card">
        <div class="kpi-label">Total Portfolio</div>
        <div class="kpi-value">$12,847</div>
        <div class="kpi-delta">+2.3% Today</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
    <div class="kpi-card">
        <div class="kpi-label">Win Rate</div>
        <div class="kpi-value">74.2%</div>
        <div class="muted">Last 30 days</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
    <div class="kpi-card">
        <div class="kpi-label">Total Trades</div>
        <div class="kpi-value">1,247</div>
        <div class="muted">This month</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.divider()

# Performance Chart
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        "<div class='section-title'>Portfolio Performance (30 days)</div>",
        unsafe_allow_html=True,
    )

    # Generate and display sample performance chart
    df = generate_sample_data()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["portfolio_value"],
            mode="lines",
            line=dict(color="#8b5cf6", width=3, shape="spline", smoothing=1.2),
            fill="tozeroy",
            fillcolor="rgba(139, 92, 246, 0.12)",
            name="Portfolio Value",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        showlegend=False,
        margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", title=None),
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(
        "<div class='section-title'>Strategy status</div>", unsafe_allow_html=True
    )

    strategies = [
        {"name": "Market Making", "status": "active", "pnl": "+$342"},
        {"name": "Arbitrage", "status": "active", "pnl": "+$156"},
        {"name": "Grid Trading", "status": "active", "pnl": "+$89"},
        {"name": "DCA Bot", "status": "inactive", "pnl": "+$234"},
    ]

    for strategy in strategies:
        status_class = (
            "status-active" if strategy["status"] == "active" else "status-inactive"
        )

        st.markdown(
            f"""
        <div class="card" style="margin: .5rem 0;">
            <div style="display: flex; justify-content: space-between; align-items: center; gap: .75rem;">
                <div>
                    <div style="font-weight: 700;">{strategy["name"]}</div>
                    <div class="status-badge {status_class}">{strategy["status"].title()}</div>
                </div>
                <div style="text-align: right; color: var(--success); font-weight: 700;">{strategy["pnl"]}</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

st.divider()

# Feature Showcase
st.markdown("### Platform Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
    <div class="feature-card">
        <div style="text-align: left; margin-bottom: .5rem;">
            <div class="section-title" style="margin:0;">Strategy Development</div>
        </div>
        <ul style="list-style: none; padding: 0; margin: 0; line-height: 1.9;">
            <li>✓ Visual strategy builder</li>
            <li>✓ Advanced configuration</li>
            <li>✓ Custom parameters</li>
            <li>✓ Sandbox testing</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
    <div class="feature-card">
        <div style="text-align: left; margin-bottom: .5rem;">
            <div class="section-title" style="margin:0;">Analytics & Insights</div>
        </div>
        <ul style="list-style: none; padding: 0; margin: 0; line-height: 1.9;">
            <li>✓ Real-time performance</li>
            <li>✓ Advanced backtesting</li>
            <li>✓ Detailed reports</li>
            <li>✓ Interactive charts</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
    <div class="feature-card">
        <div style="text-align: left; margin-bottom: .5rem;">
            <div class="section-title" style="margin:0;">Live Trading</div>
        </div>
        <ul style="list-style: none; padding: 0; margin: 0; line-height: 1.9;">
            <li>✓ Automated execution</li>
            <li>✓ Real-time monitoring</li>
            <li>✓ Risk management</li>
            <li>✓ Smart alerts</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.divider()

# Quick Actions
st.markdown("### Quick Actions")

# Alert for mocked navigation
st.info("ℹ️ This is a mocked landing page. Quick Actions are demonstrative only.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Deploy Strategy", use_container_width=True, type="primary"):
        st.error("Navigation unavailable - mocked landing page.")

with col2:
    if st.button("View Performance", use_container_width=True):
        st.error("Navigation unavailable - mocked landing page.")

with col3:
    if st.button("Backtesting", use_container_width=True):
        st.error("Navigation unavailable - mocked landing page.")

with col4:
    if st.button("Archived Bots", use_container_width=True):
        st.error("Navigation unavailable - mocked landing page.")

st.divider()

# Community & Resources
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Learn & Explore")

    st.video("https://youtu.be/7eHiMPRBQLQ?si=PAvCq0D5QDZz1h1D")

with col2:
    st.markdown("### Join Our Community")

    st.markdown(
        """
    <div class="card" style="background: linear-gradient(135deg, rgba(124,58,237,0.35) 0%, rgba(34,211,238,0.25) 100%);
                padding: 1.5rem; border-radius: 15px; color: white; border: 1px solid rgba(255,255,255,0.25)">
        <h4 style="margin-top:0;">Connect with Traders</h4>
        <p style="color: #f3f4f6;">Join thousands of algorithmic traders sharing strategies and insights.</p>
        <div style="display:flex; gap:.5rem;">
            <a href="https://discord.gg/hummingbot" target="_blank"
               style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem;
                      border-radius: 8px; text-decoration: none; color: white; font-weight: 700;">
               Join Discord
            </a>
            <a href="https://github.com/hummingbot/dashboard" target="_blank"
               style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem;
                      border-radius: 8px; text-decoration: none; color: white; font-weight: 700;">
               Report Issues
            </a>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Footer stats
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Global Users", "10,000+")

with col2:
    st.metric("Exchanges", "20+")

with col3:
    st.metric("Daily Volume", "$2.5M+")

with col4:
    st.metric("GitHub Stars", "7,800+")
