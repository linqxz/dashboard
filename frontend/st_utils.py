import inspect
import os.path
from pathlib import Path
from typing import Optional, Union

import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit.commands.page_config import InitialSideBarState, Layout
from yaml import SafeLoader

from CONFIG import AUTH_SYSTEM_ENABLED
from frontend.pages.permissions import main_page, private_pages, public_pages


def _inject_global_theme():
    """Inject a global dark theme and typography for consistent styling across pages."""
    st.markdown(
        """
        <style>
            /* Using self-hosted Inter via theme.fontFaces; no external import needed */
            @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
            @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,300..700,0..1,-50..200');
            :root {
                --bg: #0b0f17;
                --surface: #0f172a;
                --surface-1: rgba(255,255,255,0.04);
                --surface-2: rgba(255,255,255,0.06);
                --card: rgba(255,255,255,0.03);
                --border: rgba(148,163,184,0.15);
                --text: #e5e7eb;
                --muted: #94a3b8;
                --primary: #7c3aed;
                --primary-600: #8b5cf6;
                --success: #10b981;
                --danger: #ef4444;
                --accent: #22d3ee;
                /* Themed header/background accents */
                --bg-gradient-1: rgba(124,58,237,0.12);
                --bg-gradient-2: rgba(34,211,238,0.10);
                --header-bg: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0)) , var(--surface-1);
                --header-border: var(--border);
                --elevation-1-shadow: 0 1px 0 rgba(0,0,0,0.25);
            }
            /* Light theme via system preference */
            @media (prefers-color-scheme: light) {
                :root {
                    --bg: #f8fafc;
                    --surface: #ffffff;
                    --surface-1: rgba(0,0,0,0.02);
                    --surface-2: rgba(0,0,0,0.04);
                    --card: rgba(0,0,0,0.03);
                    --border: rgba(2,6,23,0.08);
                    --text: #0f172a;
                    --muted: #475569;
                    --primary: #7c3aed;
                    --primary-600: #6d28d9;
                    --success: #059669;
                    --danger: #dc2626;
                    --accent: #0891b2;
                    --bg-gradient-1: rgba(124,58,237,0.06);
                    --bg-gradient-2: rgba(34,211,238,0.06);
                    --header-bg: linear-gradient(180deg, rgba(0,0,0,0.03), rgba(0,0,0,0)) , var(--surface-1);
                    --header-border: var(--border);
                    --elevation-1-shadow: 0 1px 0 rgba(0,0,0,0.06);
                }
            }
            html, body, [class^="css"], .stApp {
                /* Typography is controlled by the Streamlit theme; only keep visuals here */
                background-image: radial-gradient(1000px 600px at 10% -10%, var(--bg-gradient-1), transparent),
                                  radial-gradient(800px 500px at 90% 0%, var(--bg-gradient-2), transparent);
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
                text-rendering: optimizeLegibility;
                line-height: 1.6;
            }
            html { font-size: 16.5px; }
            /* Code font uses Streamlit defaults */
            /* No icon or text font overrides here */
            /* Avoid overriding text or icon fonts here */
            .main, .block-container { background: transparent !important; }
            /* Top bar/header styling: connect visually with page */
            [data-testid="stHeader"] {
                background: var(--header-bg) !important;
                border-bottom: 1px solid var(--header-border);
                backdrop-filter: blur(6px);
                -webkit-backdrop-filter: blur(6px);
                box-shadow: var(--elevation-1-shadow);
            }
            /* Header inherits font from theme */
                         /* Preserve icon ligatures in header buttons */
             [data-testid="stHeader"] [class*="material-icons"],
             [data-testid="stHeader"] [class*="material-symbols"] {
                 font-family: 'Material Symbols Outlined', 'Material Icons' !important;
                 -webkit-font-feature-settings: 'liga';
                 font-feature-settings: 'liga';
             }
             /* Fix sidebar toggle in header when sidebar is collapsed */
             [data-testid="stHeader"] button,
             [data-testid="stHeader"] button *,
             [data-testid="stHeaderActionElements"] button,
             [data-testid="stHeaderActionElements"] button * {
                 font-family: 'Material Symbols Outlined', 'Material Icons' !important;
                 -webkit-font-feature-settings: 'liga';
                 font-feature-settings: 'liga';
             }
            h1, h2, h3 { letter-spacing: -0.01em; margin: 0 0 .5rem 0; }
            h1 { font-size: 2.4rem; }
            h2 { font-size: 1.7rem; }
            h3 { font-size: 1.5rem; }
            p, li { font-size: 1.1rem; line-height: 1.75; }
            label, span { font-size: 1.05rem; }
            small { font-size: 0.95rem; }
            /* Sidebar cohesion */
            [data-testid="stSidebar"] {
                background: var(--surface-1) !important;
                border-right: 1px solid var(--border);
                box-shadow: var(--elevation-1-shadow);
            }
            /* Buttons */
            .stButton > button {
                border-radius: 10px !important;
                border: 1px solid var(--border) !important;
                background: var(--card) !important;
                font-weight: 600 !important;
                transition: border-color .15s ease, transform .05s ease;
            }
            .stButton > button:hover { border-color: rgba(139,92,246,0.6) !important; }
            /* Primary button */
            [data-testid="baseButton-primary"] > button,
            .stButton > button[kind="primary"] {
                background: linear-gradient(180deg, var(--primary-600), var(--primary)) !important;
                border: 1px solid rgba(139,92,246,0.65) !important;
                color: #fff !important;
            }
            /* Alerts */
            [data-testid="stAlert"] {
                    border: 1px solid var(--border);
                    border-radius: 12px;
            }
            /* Metrics */
            [data-testid="metric-container"] {
                padding: .5rem .75rem;
                    border-radius: 12px;
                    border: 1px solid var(--border);
                background: var(--card);
            }
            /* Divider spacing */
            hr { opacity: .35; margin: 1.25rem 0; }
            /* Card utility */
            .rs-card {
                border: 1px solid var(--border);
                border-radius: 14px;
                background: var(--card);
                padding: 1rem 1.25rem;
            }
            .rs-page-title {
                display: flex; align-items: center; gap: .55rem; margin: 0 0 1rem 0;
                font-size: 2.1rem; font-weight: 700; letter-spacing: -0.01em;
            }
            .rs-title-icon { font-size: 1.8rem; color: var(--primary-600); }

            /* Sidebar navigation: inject Material Symbols before links */
            [data-testid="stSidebar"] a[href*="landing"]::before { content: "dashboard"; }
            [data-testid="stSidebar"] a[href*="instances"]::before { content: "hub"; }
            [data-testid="stSidebar"] a[href*="launch_bot_v2"]::before { content: "rocket_launch"; }
            [data-testid="stSidebar"] a[href*="credentials"]::before { content: "vpn_key"; }
            [data-testid="stSidebar"] a[href*="portfolio"]::before { content: "finance"; }
            [data-testid="stSidebar"] a[href*="trading"]::before { content: "show_chart"; }
            [data-testid="stSidebar"] a[href*="archived_bots"]::before { content: "inventory_2"; }
            [data-testid="stSidebar"] a[href*="file_manager"]::before { content: "folder"; }
            [data-testid="stSidebar"] a[href*="download_candles"]::before { content: "download"; }
            [data-testid="stSidebar"] a[href*="tvl_vs_mcap"]::before { content: "stacked_bar_chart"; }
            [data-testid="stSidebar"] a[href*="assignment_manager_v1"]::before { content: "task"; }
            [data-testid="stSidebar"] a[href*="grid_strike"]::before { content: "grid_view"; }
            [data-testid="stSidebar"] a[href*="pmm_simple"]::before { content: "settings"; }
            [data-testid="stSidebar"] a[href*="pmm_dynamic"]::before { content: "settings"; }
            [data-testid="stSidebar"] a[href*="dman_maker_v2"]::before { content: "auto_awesome"; }
            [data-testid="stSidebar"] a[href*="bollinger_v1"]::before { content: "show_chart"; }
            [data-testid="stSidebar"] a[href*="macd_bb_v1"]::before { content: "query_stats"; }
            [data-testid="stSidebar"] a[href*="supertrend_v1"]::before { content: "insights"; }
            [data-testid="stSidebar"] a[href*="kalman_filter_v1"]::before { content: "monitoring"; }
            [data-testid="stSidebar"] a[href*="xemm_controller"]::before { content: "tune"; }
            [data-testid="stSidebar"] a[href*="bot_performance"]::before { content: "trending_up"; }

            [data-testid="stSidebar"] a[href*="/"]::before {
                font-family: 'Material Symbols Outlined' !important;
                font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
                display: inline-block; margin-right: .55rem; vertical-align: middle; color: var(--muted);
            }
            .stApp { font-family: "Inter", system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }

            </style>
            """,
        unsafe_allow_html=True,
    )


def initialize_st_page(
    title: Optional[str] = None,
    icon: Optional[str] = None,
    layout: Layout = "wide",
    initial_sidebar_state: InitialSideBarState = "expanded",
    show_readme: bool = True,
    ms_icon: Optional[str] = None,
):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout=layout,
        initial_sidebar_state=initial_sidebar_state,
    )

    # Inject global theme
    _inject_global_theme()

    # Add page title
    if title:
        if ms_icon:
            st.markdown(
                f"""
                <div class='rs-page-title'>
                    <span class='material-symbols-outlined rs-title-icon'>{ms_icon}</span>
                    <span>{title}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.title(title)

    # Get caller frame info safely
    frame: Optional[Union[inspect.FrameInfo, inspect.Traceback]] = None
    try:
        caller_frame = inspect.currentframe()
        if caller_frame is not None:
            caller_frame = caller_frame.f_back
            if caller_frame is not None:
                frame = inspect.getframeinfo(caller_frame)
    except Exception:
        pass

    if frame is not None and show_readme:
        current_directory = Path(os.path.dirname(frame.filename))
        readme_path = current_directory / "README.md"
        if readme_path.exists():
            with st.expander("About This Page"):
                st.write(readme_path.read_text())
        else:
            # Only show expander if README exists
            pass


def download_csv_button(df: pd.DataFrame, filename: str, key: str):
    csv = df.to_csv(index=False).encode("utf-8")
    return st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{filename}.csv",
        mime="text/csv",
        key=key,
    )


def style_metric_cards():
    # Removed custom metric styling to use default Streamlit styling
    pass


def get_backend_api_client():
    import atexit

    from hummingbot_api_client import SyncHummingbotAPIClient

    from CONFIG import BACKEND_API_HOST, BACKEND_API_PASSWORD, BACKEND_API_PORT, BACKEND_API_USERNAME

    # Use Streamlit session state to store singleton instance
    if (
        "backend_api_client" not in st.session_state
        or st.session_state.backend_api_client is None
    ):
        try:
            # Create and enter the client context
            # Ensure URL has proper protocol
            if not BACKEND_API_HOST.startswith(("http://", "https://")):
                base_url = f"http://{BACKEND_API_HOST}:{BACKEND_API_PORT}"
            else:
                base_url = f"{BACKEND_API_HOST}:{BACKEND_API_PORT}"

            client = SyncHummingbotAPIClient(
                base_url=base_url,
                username=BACKEND_API_USERNAME,
                password=BACKEND_API_PASSWORD,
            )
            # Initialize the client using context manager
            client.__enter__()

            # Register cleanup function to properly exit the context manager
            def cleanup_client():
                try:
                    if (
                        "backend_api_client" in st.session_state
                        and st.session_state.backend_api_client is not None
                    ):
                        st.session_state.backend_api_client.__exit__(None, None, None)
                        st.session_state.backend_api_client = None
                except Exception:
                    pass  # Ignore cleanup errors

            # Register cleanup with atexit and session state
            atexit.register(cleanup_client)
            if "cleanup_registered" not in st.session_state:
                st.session_state.cleanup_registered = True
                # Also register cleanup for session state changes
                st.session_state.backend_api_client_cleanup = cleanup_client

            # Check Docker after initialization
            if not client.docker.is_running():
                st.error("Docker is not running. Please make sure Docker is running.")
                cleanup_client()  # Clean up before stopping
                st.stop()

            st.session_state.backend_api_client = client
        except Exception as e:
            st.error(f"Failed to initialize API client: {str(e)}")
            st.stop()

    return st.session_state.backend_api_client


def auth_system():
    if not AUTH_SYSTEM_ENABLED:
        return {
            "Main": main_page(),
            **private_pages(),
            **public_pages(),
        }
    else:
        with open("credentials.yml") as file:
            config = yaml.load(file, Loader=SafeLoader)
        if (
            "authenticator" not in st.session_state
            or "authentication_status" not in st.session_state
            or not st.session_state.get("authentication_status", False)
        ):
            st.session_state.authenticator = stauth.Authenticate(
                config["credentials"],
                config["cookie"]["name"],
                config["cookie"]["key"],
                config["cookie"]["expiry_days"],
            )
            # Show only public pages for non-authenticated users
            st.session_state.authenticator.login()
            if st.session_state["authentication_status"] is False:
                st.error("Username/password is incorrect")
            elif st.session_state["authentication_status"] is None:
                st.warning("Please enter your username and password")
            return {"Main": main_page(), **public_pages()}
        else:
            st.session_state.authenticator.logout(location="sidebar")
            st.sidebar.write(f"Welcome *{st.session_state['name']}*")
            # Show all pages for authenticated users
            return {
                "Main": main_page(),
                **private_pages(),
                **public_pages(),
            }
