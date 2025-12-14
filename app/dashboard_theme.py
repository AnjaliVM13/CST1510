"""
Dashboard Theme Module (Legacy)
Applies cyberpunk-themed dashboard styling with animated backgrounds and particle effects.
Note: This module is maintained for backward compatibility.
"""

import streamlit as st
from streamlit.components.v1 import html

def apply_cyberpunk_dashboard_theme():
    """
    Applies a cyberpunk-themed dashboard style with dark backgrounds, neon accents, and animated elements.
    Creates animated gradient background, floating particles, and holographic sphere effects.
    """
# ======================================================
# BACKGROUND PULSE
# ======================================================
# Inject CSS for animated background with pulsing gradient effect
st.markdown("""
<style>
body {
    margin: 0;
    padding: 0;
    background: radial-gradient(circle at 30% 30%, #000000, #1a0b3c);
    background-size: 400% 400%;
    animation: bgPulse 25s ease infinite;
}
@keyframes bgPulse {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* FLOATING PARTICLES */
.particle {
    position: fixed;
    width: 6px;
    height: 6px;
    background: #bb00ff33;
    border-radius: 50%;
    animation: floatUp 12s infinite ease-in;
    z-index: -1; /* behind content */
}
@keyframes floatUp {
    0% { transform: translateY(0); opacity: 0; }
    20% { opacity: 1; }
    100% { transform: translateY(-1000px); opacity: 0; }
}

/* FLOATING NEON SHAPES */
@keyframes float0 {0%{transform:translateY(0);}50%{transform:translateY(25px) translateX(10px);}100%{transform:translateY(0);}}
@keyframes float1 {0%{transform:translateY(0);}50%{transform:translateY(-35px) translateX(-15px);}100%{transform:translateY(0);}}
@keyframes float2 {0%{transform:translateY(0);}50%{transform:translateY(20px) translateX(-10px);}100%{transform:translateY(0);}}
#networkSphere {
    animation: rotateSphere 20s linear infinite;
}
@keyframes rotateSphere {
    0% { transform: translateX(-50%) rotateY(0deg); }
    100% { transform: translateX(-50%) rotateY(360deg); }
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# CREATE FLOATING PARTICLES
# ---------------------------
# Generate 25 floating particles with distributed positions and animation delays
for i in range(25):
    st.markdown(
        f"<div class='particle' style='left:{i*4}%; animation-delay:{i*0.4}s'></div>",
        unsafe_allow_html=True
    )

# ---------------------------
# CREATE FLOATING NEON SHAPES
# ---------------------------
# Create floating neon circles in purple, pink, and white colors
for i, color in enumerate(["#bb00ff", "#ff33ff", "#ffffff"]):
    st.markdown(
        f"<div style='position:fixed; top:{10+i*25}%; left:{5+i*30}%; width:{30+i*10}px; height:{30+i*10}px; border-radius:50%; background:{color}; opacity:0.2; animation: float{i} {6+i*2}s ease-in-out infinite alternate;'></div>",
        unsafe_allow_html=True
    )

# ---------------------------
# HOLOGRAPHIC SPHERE + TS PARTICLES
# ---------------------------
# Initialize TSParticles library for interactive particle network effects
html("""
<div id="networkSphere" style="position:fixed; top:20%; left:50%; transform:translateX(-50%); width:300px; height:300px; z-index:-1;"></div>
<div id="tsparticles"></div>
<script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
<script>
tsParticles.load("tsparticles", {
  fullScreen: { enable: true },
  particles: { 
    number: { value: 60 },
    color: { value: ["#bb00ff","#ff33ff","#ffffff"] },
    shape: { type: "circle" },
    opacity: { value: 0.6 },
    size: { value: { min: 1, max: 3 } },
    links: { enable: true, distance: 120, color: "#bb00ff", opacity: 0.3, width: 1 },
    move: { enable: true, speed: 0.4 }
  },
  interactivity: { events: { onHover: { enable: true, mode: "repulse" }, onClick: { enable: true, mode: "push" } } }
});

tsParticles.load("networkSphere", {
    fullScreen: false,
    background: { color: "transparent" },
    particles: {
        number: { value: 60 },
        color: { value: ["#bb00ff","#ff33ff"] },
        shape: { type: "circle" },
        size: { value: { min: 2, max: 5 } },
        links: { enable: true, distance: 80, color: "#bb00ff", opacity: 0.3, width: 1 },
        move: { enable: true, speed: 1, direction: "none", outModes: "bounce" }
    },
    interactivity: { events: { onHover: { enable: true, mode: "repulse" } } }
});
</script>
""", height=300)
