"""
Dashboard Visual Effects Module
Applies cyberpunk-themed visual effects including animated backgrounds, particles, and neon styling.
"""

# app/theme/dashboard_effects.py
import streamlit as st
from streamlit.components.v1 import html


def apply_dashboard_effects():
    """
    Apply all dashboard visual effects to create immersive cyberpunk aesthetic.
    
    Effects include:
    - Animated gradient background with smooth transitions
    - Floating particles for depth and movement
    - Glass/blur UI feel with backdrop filters
    - Neon buttons with glow effects
    - Holographic TSParticles sphere for interactive background
    - Floating neon orbiting circles for ambient animation
    """

    # ----------------------------------
    # GLOBAL BACKGROUND + ANIMATION
    # ----------------------------------
    # Inject CSS for animated gradient background and container styling
    st.markdown(
        """
    <style>
    /* Remove default padding for full-width layout */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }

    /* Main animated background with gradient shift animation */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(
            135deg,
            #1a0026,  /* Deep purple */
            #0f0017,  /* Darker purple */
            #050009,  /* Very dark purple */
            #000000   /* Black */
        );
        background-size: 300% 300%;  /* Larger size for smooth animation */
        animation: bgShift 18s ease infinite;  /* Continuous background animation */
        color: white !important;  /* Ensure text is visible */
    }

    /* Keyframe animation for background position shift */
    @keyframes bgShift {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 70%; }
        100% { background-position: 0% 0%; }
    }

    /* Floating particles */
    .particle {
        position: fixed;
        top: 0;
        width: 4px;
        height: 4px;
        background: #bb00ff;
        border-radius: 50%;
        opacity: 0.7;
        animation: floating 12s linear infinite;
    }

    @keyframes floating {
        0% { transform: translateY(0px); opacity: 0.4; }
        50% { opacity: 1; }
        100% { transform: translateY(100vh); opacity: 0.2; }
    }

    /* Glass containers */
    .glass-box {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 25px rgba(160,0,255,0.2);
    }

    /* Neon buttons */
    .stButton>button {
        background: linear-gradient(135deg, #8b00ff, #ff00d4);
        border: none;
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.2s ease;
        box-shadow: 0 0 12px rgba(255,0,255,0.4);
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(255,0,255,0.8);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # ----------------------------------
    # Floating particles (25 dots)
    # ----------------------------------
    # Create 25 floating particles with staggered animation delays
    for i in range(25):
        st.markdown(
            f"<div class='particle' style='left:{i * 4}%; animation-delay:{i * 0.5}s;'></div>",
            unsafe_allow_html=True,
        )

    # ----------------------------------
    # Floating orbiting neon circles
    # ----------------------------------
    # Create floating neon circles with different colors and positions
    colors = ["#bb00ff", "#ff33ff", "#ffffff"]  # Purple, pink, white
    for i, color in enumerate(colors):
        html(
            f"""
        <div style="
            position:fixed;
            top:{10 + i*25}%;
            left:{5 + i*30}%;
            width:{30 + i*10}px;
            height:{30 + i*10}px;
            border-radius:50%;
            background:{color};
            opacity:0.2;
            animation: float{i} {6 + i*2}s ease-in-out infinite alternate;
            z-index:0;
            pointer-events:none;
        "></div>
        """,
            height=0,
        )

    html(
        """
    <style>
    @keyframes float0 { 0%{transform:translateY(0);} 50%{transform:translateY(25px) translateX(10px);} 100%{transform:translateY(0);} }
    @keyframes float1 { 0%{transform:translateY(0);} 50%{transform:translateY(-35px) translateX(-15px);} 100%{transform:translateY(0);} }
    @keyframes float2 { 0%{transform:translateY(0);} 50%{transform:translateY(20px) translateX(-10px);} 100%{transform:translateY(0);} }
    </style>
    """,
        height=0,
    )
