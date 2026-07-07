"""
Reusable UI component helpers for rendering uniform footers, empty states, and branding.
"""
import streamlit as st
import os

def render_page_header(title: str, description: str):
    """
    Renders a consistent page title, subtitle, and injects professional global CSS styling.

    Args:
        title (str): Title text with emoji prefix.
        description (str): Subtitle description text.
    """
    # Load professional custom CSS styling from external stylesheet
    style_path = "assets/style.css"
    if os.path.exists(style_path):
        try:
            with open(style_path, "r", encoding="utf-8") as f:
                css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        except Exception:
            pass
    
    # Styled header layout
    st.markdown(
        f"""
        <div style="margin-bottom: 25px;">
            <h1 style="font-size: 2.5rem; font-weight: 700; background: linear-gradient(to right, #FFFFFF, #60A5FA); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</h1>
            <p style="color: #94A3B8; font-size: 1.1rem; margin-top: -5px;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<hr>", unsafe_allow_html=True)

def render_logo(sidebar: bool = False):
    """
    Displays the HireReady logo if available in the assets folder.

    Args:
        sidebar (bool): True if rendering inside the sidebar container.
    """
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        if sidebar:
            # Render a smaller logo at the top of the sidebar
            st.sidebar.image(logo_path, width="stretch")
            st.sidebar.markdown(
                "<h3 style='text-align: center; color: #1E3A8A; margin-top: -10px;'>HireReady</h3>",
                unsafe_allow_html=True
            )
            st.sidebar.markdown("---")
        else:
            # Render logo on main pages
            st.image(logo_path, width=120)
    else:
        if sidebar:
            st.sidebar.markdown("### 💼 HireReady")
            st.sidebar.markdown("---")

def render_empty_state(message: str, suggestions: list | None = None):
    """
    Renders a standardized professional empty state panel with icons and helpful suggestions.

    Args:
        message (str): Custom description of the missing state.
        suggestions (list): Bullet items suggesting how to resolve the empty state.
    """
    st.warning(f"⚠️ **Notice**: {message}")
    if suggestions:
        st.info(
            "💡 **Action Recommended**:\n" +
            "\n".join([f"- {item}" for item in suggestions])
        )

def render_footer():
    """
    Renders a unified footer section across all multipage endpoints.
    """
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #9CA3AF; font-size: 0.85em; padding-top: 15px;'>
            <strong>HireReady</strong> | Placement Readiness Intelligence Dashboard<br>
            <span style='font-size: 0.9em;'>Built using: Streamlit • Pandas • Plotly • Folium</span>
        </div>
        """,
        unsafe_allow_html=True
    )

