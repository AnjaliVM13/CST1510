"""
Ultimate Dark Theme Module
Applies full-page dark theme with animated gradients, glass-morphism effects,
and interactive particle systems for immersive cyberpunk aesthetic.
"""

# app/theme.py
import streamlit as st
from streamlit.components.v1 import html


def apply_ultimate_dark_theme():
    """
    Apply full-page 4K dark theme with black + deep violet gradient and neon cyberpunk accents.
    Includes animated background, glass sidebar, neon buttons, and floating particle effects.
    """

    # ---------------------------
    # CSS: background, sidebar, buttons
    # ---------------------------
    # Inject comprehensive CSS for dark theme styling
    css = """
    <style>
    /* FULL PAGE BLACK + DEEP VIOLET GRADIENT */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #000000 0%, #4b0082 100%);
        background-size: 400% 400%;
        animation: bgPulse 25s ease infinite;
        height: 100vh;
        color: #ffffff;
        overflow: hidden;
    }
    @keyframes bgPulse {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* GLASS SIDEBAR */
    [data-testid="stSidebar"] {
        background: rgba(0,0,0,0.6);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(0,255,255,0.3);
        box-shadow: 0 0 25px rgba(0,255,255,0.2);
        animation: sidebarGlow 3s ease-in-out infinite alternate;
    }
    @keyframes sidebarGlow {
        0% { box-shadow: 0 0 10px rgba(0,255,255,0.2); }
        100% { box-shadow: 0 0 30px rgba(0,255,255,0.5); }
    }

    /* NEON BUTTONS */
    .glow-button {
        color: #00fff7;
        background-color: #0d0d2b;
        border: 2px solid #00fff7;
        border-radius: 12px;
        padding: 15px 35px;
        font-size: 24px;
        font-weight: bold;
        text-transform: uppercase;
        box-shadow: 0 0 15px #00fff7;
        transition: all 0.3s ease-in-out;
        cursor: pointer;
    }
    .glow-button:hover {
        box-shadow: 0 0 25px #00fff7, 0 0 50px #ff00ff;
        color: #ffffff;
        transform: scale(1.07);
    }

    /* HEADINGS */
    h1, h2, h3, p {
        color: #ffffff;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # ------------------------------------------------------
    # FLOATING PARTICLES
    # ------------------------------------------------------
    # Create 25 floating particles with distributed positions and staggered animations
    for i in range(25):
        st.markdown(
            f"<div class='particle' style='left:{i*4}%; animation-delay:{i*0.4}s'></div>",
            unsafe_allow_html=True,
        )

    # ---------------------------
    # PARTICLES: neon network style
    # ---------------------------
    # Initialize TSParticles library for interactive particle network
    html(
        """
    <div id="tsparticles"></div>
    <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
    <script>
    tsParticles.load("tsparticles", {
      fullScreen: { enable: true },
      particles: { 
        number: { value: 60 },
        color: { value: ["#00fff7","#ff00ff","#ffffff"] },
        shape: { type: "circle" },
        opacity: { value: 0.7 },
        size: { value: { min: 1, max: 3 } },
        links: { enable: true, distance: 130, color: "#00fff7", opacity: 0.3, width: 1.2 },
        move: { enable: true, speed: 0.4, direction: "none", outModes: { default: "out" } }
      },
      interactivity: {
        events: {
          onHover: { enable: true, mode: "repulse" },
          onClick: { enable: true, mode: "push" }
        },
        modes: {
          repulse: { distance: 140 },
          push: { quantity: 4 }
        }
      }
    });
    </script>
    """,
        height=0,
    )

    # ---------------------------
    # FLOATING NEON SHAPES
    # ---------------------------
    # Create floating neon circles with animation effects
    html(
        """
    <div style="position:fixed; top:15%; left:15%; width:60px; height:60px; background:#ff00ff; border-radius:50%; opacity:0.3; animation: float1 7s ease-in-out infinite alternate;"></div>
    <div style="position:fixed; top:65%; left:75%; width:100px; height:100px; background:#00fff7; border-radius:50%; opacity:0.2; animation: float2 9s ease-in-out infinite alternate;"></div>
    <style>
    @keyframes float1 {
        0% { transform: translateY(0px); }
        50% { transform: translateY(25px) translateX(10px); }
        100% { transform: translateY(0px); }
    }
    @keyframes float2 {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-35px) translateX(-15px); }
        100% { transform: translateY(0px); }
    }
    </style>
    """,
        height=0,
    )
