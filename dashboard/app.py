import os
import html
import textwrap
from datetime import datetime

import pandas as pd
import altair as alt
import requests
import streamlit as st
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Home Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONFIG
# ============================================================

API_URL = os.getenv(
    "AI_HOME_API_URL",
    "http://127.0.0.1:8000",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 75% 0%,
                rgba(27, 70, 180, 0.13),
                transparent 30%
            ),
            #050a13;

        color: #f5f7fb;
    }

    .main .block-container {
        max-width: 1480px;
        padding: 18px 28px 28px 28px;
    }

    header[data-testid="stHeader"] {
        background: #050a13;
    }

    footer {
        visibility: hidden;
    }

    [data-testid="stDecoration"] {
        display: none;
    }

    /* Remove extra Streamlit spacing */

    div[data-testid="stVerticalBlock"] {
        gap: 0.45rem;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 12px;
    }


    /* ========================================================
       POWER CHART
       ======================================================== */

    .power-mini-stat {
        min-height: 48px;
        padding: 8px 10px;
        border: 1px solid #203554;
        border-radius: 10px;
        background: linear-gradient(135deg, #0b1a2d, #081321);
    }

    .power-mini-label {
        color: #70839f;
        font-size: 8px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .08em;
    }

    .power-mini-value {
        margin-top: 3px;
        color: #eaf4ff;
        font-size: 13px;
        font-weight: 800;
    }

    .power-chart-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        margin-top: 2px;
        color: #687d99;
        font-size: 9px;
    }

    .power-chart-footer .positive {
        color: #64c7ff;
    }

    .power-chart-footer .negative {
        color: #7aa7ff;
    }

    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #070d17;
        border-right: 1px solid #172235;
    }

    section[data-testid="stSidebar"] > div {
        padding: 18px 12px 14px 12px;
    }

    .brand {
        padding: 2px 6px 22px 6px;
        border-bottom: 1px solid #172235;
        margin-bottom: 17px;
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand-logo {
        width: 40px;
        height: 40px;
        border-radius: 11px;

        display: flex;
        align-items: center;
        justify-content: center;

        background:
            linear-gradient(
                135deg,
                #087cff,
                #6838ee
            );

        border: 1px solid rgba(92,154,255,.35);

        box-shadow:
            0 0 24px rgba(31,100,255,.30);

        font-size: 21px;
    }

    .brand-name {
        color: #ffffff;
        font-size: 17px;
        font-weight: 800;
        line-height: 1.1;
    }

    .brand-subtitle {
        color: #7c899e;
        font-size: 9px;
        margin-top: 4px;
    }

    .side-heading {
        color: #68758a;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin: 18px 5px 8px;
    }

    .nav-active {
    background:
        linear-gradient(
            90deg,
            #073a9d,
            #0b2d73
        );

    border: 1px solid #124ab3;

    box-shadow:
        0 0 18px rgba(24,91,255,.16);

    border-radius: 9px;

    color: white;

    padding: 10px 12px;

    font-size: 12px;
    font-weight: 700;
}


section[data-testid="stSidebar"] .stButton > button {

    width: 100%;

    text-align: left;

    border-radius: 9px;

    border: 1px solid transparent;

    background: transparent;

    color: #aeb9ca;

    min-height: 37px;

    padding: 0 12px;

    font-size: 12px;
    font-weight: 600;
}

    .pro-card {
        margin-top: 22px;

        padding: 14px;

        border-radius: 11px;

        background:
            radial-gradient(
                circle at 90% 10%,
                rgba(123,60,255,.30),
                transparent 50%
            ),
            linear-gradient(
                145deg,
                #171447,
                #101b3b
            );

        border: 1px solid #302577;
    }

    .pro-title {
        color: white;
        font-size: 12px;
        font-weight: 800;
    }

    .pro-text {
        color: #8995ac;

        font-size: 9px;

        line-height: 1.45;

        margin: 7px 0 12px;
    }

    .pro-button {
        display: inline-block;

        padding: 7px 10px;

        border-radius: 7px;

        background: #0a2d86;

        color: white;

        font-size: 9px;

        border: 1px solid #214eb3;
    }

    .user-card {
        margin-top: 18px;

        padding: 10px;

        border-radius: 10px;

        background: #0b1423;

        border: 1px solid #17263a;

        display: flex;

        align-items: center;

        gap: 9px;
    }

    .user-photo {
        width: 31px;
        height: 31px;

        border-radius: 50%;

        background: #26354b;

        display: flex;

        align-items: center;

        justify-content: center;

        font-size: 15px;
    }

    .user-name {
        color: #e8edf5;

        font-size: 10px;

        font-weight: 700;
    }

    .user-email {
        color: #69778d;

        font-size: 8px;

        margin-top: 2px;
    }


    /* ========================================================
       TOP BAR
       ======================================================== */

    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
    }

    .topbar-left {
        display: flex;
        align-items: center;
        gap: 9px;
    }

    .topbar-plus {
        width: 36px;
        height: 36px;

        border-radius: 50%;

        border: 1px solid #1d3555;

        background: #0b1729;

        color: #dbe6f6;

        display: flex;

        align-items: center;

        justify-content: center;

        font-size: 21px;
    }

    .activity-pill {
        height: 36px;

        padding: 0 13px;

        border-radius: 10px;

        background: #0b1729;

        border: 1px solid #172a45;

        color: #cbd6e6;

        display: flex;

        align-items: center;

        gap: 8px;

        font-size: 11px;
    }

    .control-pill {
        height: 39px;

        padding: 0 18px;

        border-radius: 12px;

        background: #0b1524;

        border: 1px solid #1b304c;

        color: #dce5f2;

        display: flex;

        align-items: center;

        justify-content: center;

        font-size: 11px;

        min-width: 145px;
    }


    /* ========================================================
       PAGE HEADER
       ======================================================== */

    .page-header {
        margin-top: 12px;
        margin-bottom: 10px;
    }

    .page-title {
        color: white;

        font-size: 25px;

        line-height: 1.15;

        font-weight: 800;
    }

    .page-subtitle {
        color: #6d8db7;

        font-size: 11px;

        margin-top: 6px;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        margin-top: 10px;

        min-height: 155px;

        padding: 22px 20px;

        border-radius: 14px;

        border: 1px solid #1b3e9c;

        background:
            radial-gradient(
                circle at 83% 20%,
                rgba(33,150,255,.22),
                transparent 27%
            ),
            linear-gradient(
                115deg,
                #0e246f 0%,
                #132887 55%,
                #0d4f9b 100%
            );

        box-shadow:
            0 13px 35px rgba(16,58,150,.12);
    }

    .hero-grid {
        display: grid;

        grid-template-columns:
            1.12fr
            1px
            1.25fr
            105px;

        gap: 21px;

        align-items: center;
    }

    .hero-energy {
        display: flex;

        align-items: center;

        gap: 17px;
    }

    .saving-ring {
        width: 72px;
        height: 72px;

        flex: 0 0 72px;

        border-radius: 50%;

        display: flex;

        align-items: center;

        justify-content: center;

        border: 7px solid #123e9b;

        border-top-color: #4a96ff;

        border-right-color: #2868e6;

        color: white;

        font-size: 18px;

        font-weight: 800;

        box-shadow:
            0 0 22px rgba(43,121,255,.22);
    }

    .hero-label {
        color: #b7c7ea;

        font-size: 9px;

        margin-bottom: 5px;
    }

    .hero-number {
        color: white;

        font-size: 24px;

        line-height: 1;

        font-weight: 800;
    }

    .hero-small {
        color: #9fb0d2;

        font-size: 9px;

        margin-top: 6px;
    }

    .money {
        color: #34db92;
        font-weight: 800;
    }

    .hero-divider {
        height: 70px;

        width: 1px;

        background: rgba(255,255,255,.12);
    }

    .avatar-row {
        margin-top: 8px;

        display: flex;

        align-items: center;
    }

    .user-avatar {
        width: 34px;
        height: 34px;

        margin-right: -5px;

        border-radius: 50%;

        border: 2px solid #16275c;

        display: inline-flex;

        align-items: center;

        justify-content: center;

        background: #2b3c58;

        font-size: 13px;
    }

    .add-avatar {
        background: transparent;

        color: #b8c7dd;

        margin-left: 7px;

        width: 34px;

        height: 34px;

        border-radius: 50%;

        display: inline-flex;

        align-items: center;

        justify-content: center;

        border: 1px dashed #5973a3;

        font-size: 18px;
    }

    .edit-pill {
        justify-self: end;

        border: 1px solid rgba(255,255,255,.08);

        background: rgba(7,18,50,.32);

        color: #d6e0ef;

        border-radius: 9px;

        padding: 8px 12px;

        font-size: 10px;

        text-align: center;
    }


    /* ========================================================
       TABS
       ======================================================== */

    .tabs {
        margin-top: 10px;

        display: flex;

        gap: 24px;

        border-bottom: 1px solid #152337;
    }

    .tab-active {
        color: #4b9dff;

        font-size: 10px;

        font-weight: 700;

        padding: 8px 4px 9px;

        border-bottom: 2px solid #1c78ff;
    }

    .tab {
        color: #7b889c;

        font-size: 10px;

        padding: 8px 4px 9px;
    }


    /* ========================================================
       DEVICE CARDS
       ======================================================== */

    .device-card {
        min-height: 102px;

        padding: 13px 14px;

        border-radius: 11px;

        background:
            linear-gradient(
                145deg,
                #0b1524,
                #09111e
            );

        border: 1px solid #17273b;

        position: relative;
    }

    .device-top {
        display: flex;

        justify-content: space-between;

        align-items: flex-start;
    }

    .device-icon {
        font-size: 25px;

        height: 30px;
    }

    .toggle {
        width: 34px;

        height: 18px;

        border-radius: 20px;

        padding: 2px;

        display: flex;

        align-items: center;
    }

    .toggle.on {
        justify-content: flex-end;

        background: #087a51;
    }

    .toggle.off {
        justify-content: flex-start;

        background: #172235;

        border: 1px solid #29374a;
    }

    .toggle-knob {
        width: 14px;

        height: 14px;

        border-radius: 50%;

        background: #f2f7ff;

        box-shadow:
            0 1px 4px rgba(0,0,0,.35);
    }

    .device-name {
        margin-top: 8px;

        color: #e8eef7;

        font-size: 11px;

        font-weight: 700;
    }

    .device-meta {
        margin-top: 5px;

        color: #718096;

        font-size: 8px;
    }


    /* ========================================================
       SECTION TITLE
       ======================================================== */

    .section-title {
        margin-top: 10px;

        margin-bottom: 7px;

        color: #e8eef7;

        font-size: 11px;

        font-weight: 800;

        display: flex;

        justify-content: space-between;

        align-items: center;
    }

    .section-link {
        color: #4b9dff;

        font-size: 8px;

        font-weight: 500;
    }


    /* ========================================================
       CATEGORY CARDS
       ======================================================== */

    .category-card {
        min-height: 72px;

        padding: 11px 13px;

        border-radius: 10px;

        border: 1px solid rgba(255,255,255,.07);

        position: relative;

        overflow: hidden;
    }

    .category-card::after {
        content: "";

        position: absolute;

        width: 65px;
        height: 65px;

        right: -18px;
        bottom: -30px;

        border-radius: 50%;

        background: rgba(255,255,255,.06);
    }

    .category-row {
        display: flex;

        align-items: center;

        gap: 10px;

        position: relative;

        z-index: 2;
    }

    .category-icon {
        width: 34px;
        height: 34px;

        border-radius: 9px;

        display: flex;

        align-items: center;

        justify-content: center;

        background: rgba(0,0,0,.12);

        font-size: 18px;
    }

    .category-title {
        color: white;

        font-size: 10px;

        font-weight: 700;
    }

    .category-count {
        color: #a1adbe;

        font-size: 8px;

        margin-top: 4px;
    }

    .security {
        background:
            linear-gradient(
                145deg,
                #102b88,
                #101d4d
            );
    }

    .climate {
        background:
            linear-gradient(
                145deg,
                #07584f,
                #073b37
            );
    }

    .sensors {
        background:
            linear-gradient(
                145deg,
                #103e79,
                #102c51
            );
    }

    .appliances {
        background:
            linear-gradient(
                145deg,
                #28531b,
                #1a3515
            );
    }

    .lighting {
        background:
            linear-gradient(
                145deg,
                #5a4300,
                #302500
            );
    }

    .locks {
        background:
            linear-gradient(
                145deg,
                #39205f,
                #24163d
            );
    }

    .entertainment {
        background:
            linear-gradient(
                145deg,
                #5d194f,
                #351531
            );
    }

    .energy {
        background:
            linear-gradient(
                145deg,
                #63390b,
                #38230b
            );
    }


    /* ========================================================
       BOTTOM PANELS
       ======================================================== */

    .panel {
        min-height: 200px;

        padding: 14px;

        border-radius: 11px;

        background: #09121f;

        border: 1px solid #17273b;
    }

    .panel-header {
        display: flex;

        justify-content: space-between;

        align-items: center;
    }

    .panel-title {
        color: #edf3fb;

        font-size: 10px;

        font-weight: 800;
    }

    .panel-subtitle {
        color: #69778d;

        font-size: 7px;

        margin-top: 3px;
    }

    .panel-link {
        color: #4b9dff;

        font-size: 8px;
    }


    /* ========================================================
       SVG ENERGY CHART
       ======================================================== */

    .chart-box {
        margin-top: 8px;

        width: 100%;

        overflow: hidden;
    }

    .chart-svg {
        width: 100%;

        height: 145px;

        display: block;
    }


    /* ========================================================
       AI INSIGHT
       ======================================================== */

    .insight-ring {
        width: 73px;

        height: 73px;

        margin: 17px auto 11px;

        border-radius: 50%;

        border: 6px solid #087b51;

        border-right-color: #2cdb91;

        display: flex;

        align-items: center;

        justify-content: center;

        color: #ecf9f3;

        font-size: 10px;

        font-weight: 800;

        box-shadow:
            0 0 18px rgba(34,211,139,.10);
    }

    .insight-ring.alert {
        border-color: #9b5b08;

        border-right-color: #ffb638;

        color: #ffcf76;
    }

    .insight-text {
        text-align: center;

        color: #dce5f0;

        font-size: 9px;

        font-weight: 700;
    }

    .insight-subtext {
        text-align: center;

        color: #6f7d91;

        font-size: 7px;

        line-height: 1.45;

        margin-top: 5px;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    .alert-row {
        padding: 10px 0;

        border-bottom: 1px solid #162437;

        color: #cbd4e0;

        font-size: 8px;

        line-height: 1.35;
    }

    .alert-time {
        float: right;

        color: #647289;

        font-size: 7px;
    }

    .success {
        color: #2dd58e;
    }

    .warning {
        color: #ffb638;
    }


    /* ========================================================
       STATUS
       ======================================================== */

    .status-line {
        margin-top: 10px;

        color: #56657b;

        font-size: 8px;

        text-align: center;
    }

    .status-online {
        color: #2dd58e;
    }

    .status-offline {
        color: #ffb638;
    }


    /* ========================================================
       RESPONSIVE
       ======================================================== */

    @media (max-width: 1000px) {

        .hero-grid {
            grid-template-columns: 1fr;
        }

        .hero-divider {
            display: none;
        }

        .edit-pill {
            justify-self: start;
        }

    }



    /* ========================================================
       TRACKING PAGE
       ======================================================== */

    .tracking-toolbar {
        margin-top: 10px;
        padding: 14px;
        border: 1px solid #172b48;
        border-radius: 14px;
        background: linear-gradient(145deg, #0b1627, #08111e);
    }

    .tracking-device-card {
        margin-top: 12px;
        padding: 18px 20px;
        border-radius: 15px;
        border: 1px solid #214a91;
        background:
            radial-gradient(circle at 90% 10%, rgba(35,125,255,.18), transparent 32%),
            linear-gradient(145deg, #0c1a31, #091321);
        box-shadow: 0 12px 30px rgba(0,0,0,.18);
    }

    .tracking-device-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 15px;
    }

    .tracking-device-left {
        display: flex;
        align-items: center;
        gap: 13px;
    }

    .tracking-device-icon {
        width: 48px;
        height: 48px;
        border-radius: 13px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(145deg, #123d82, #10234a);
        border: 1px solid #2458a4;
        font-size: 22px;
    }

    .tracking-device-name {
        color: #f4f7fc;
        font-size: 18px;
        font-weight: 800;
    }

    .tracking-device-meta {
        color: #7186a5;
        font-size: 10px;
        margin-top: 4px;
    }

    .tracking-status {
        padding: 7px 12px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 800;
        white-space: nowrap;
    }

    .tracking-on {
        color: #3be19a;
        background: rgba(45,213,142,.09);
        border: 1px solid rgba(45,213,142,.24);
    }

    .tracking-off {
        color: #91a0b5;
        background: rgba(120,135,155,.08);
        border: 1px solid #26364c;
    }

    .tracking-metrics {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-top: 14px;
    }

    .tracking-metric {
        padding: 14px;
        border-radius: 12px;
        background: rgba(5,12,22,.55);
        border: 1px solid #162b47;
    }

    .tracking-metric-label {
        color: #71829b;
        font-size: 8px;
        text-transform: uppercase;
        letter-spacing: .9px;
    }

    .tracking-metric-value {
        color: #f4f7fc;
        font-size: 20px;
        font-weight: 800;
        margin-top: 7px;
    }

    .tracking-metric-sub {
        color: #52647e;
        font-size: 8px;
        margin-top: 4px;
    }

    .tracking-panel {
        min-height: 275px;
        padding: 16px;
        margin-top: 12px;
        border-radius: 14px;
        background: #091321;
        border: 1px solid #172b46;
    }

    .tracking-section-title {
        color: #eef4fc;
        font-size: 12px;
        font-weight: 800;
    }

    .tracking-section-subtitle {
        color: #61728b;
        font-size: 8px;
        margin-top: 4px;
    }

    .tracking-activity-row {
        display: flex;
        gap: 10px;
        padding: 13px 0;
        border-bottom: 1px solid #152438;
    }

    .tracking-activity-row:last-child {
        border-bottom: none;
    }

    .activity-dot {
        color: #318cff;
        font-size: 9px;
        padding-top: 2px;
    }

    .activity-title {
        color: #dce6f4;
        font-size: 9px;
        font-weight: 700;
    }

    .activity-text {
        color: #687a93;
        font-size: 8px;
        margin-top: 3px;
    }

    .tracking-empty {
        min-height: 220px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: #687a93;
    }

    .tracking-empty-icon {
        font-size: 28px;
        margin-bottom: 8px;
    }

    .tracking-empty-title {
        color: #dce6f4;
        font-size: 12px;
        font-weight: 700;
    }

    .tracking-empty-text {
        max-width: 290px;
        font-size: 8px;
        line-height: 1.5;
        margin-top: 5px;
    }

    .tracking-info-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-top: 12px;
    }

    .tracking-info {
        padding: 13px;
        border-radius: 11px;
        background: #091321;
        border: 1px solid #172b46;
    }

    .tracking-info span {
        display: block;
        color: #61728b;
        font-size: 8px;
        margin-bottom: 6px;
    }

    .tracking-info strong {
        color: #e6edf7;
        font-size: 10px;
    }

    @media (max-width: 1000px) {
        .tracking-metrics,
        .tracking-info-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
/* ========================================================
   HOW IT WORKS PAGE
   ======================================================== */

.how-flow {
    display: grid;
    grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr;
    gap: 12px;
    align-items: stretch;
    margin: 10px 0 26px 0;
}

.how-flow-step {
    min-height: 190px;
    padding: 20px;
    border: 1px solid #172b47;
    border-radius: 16px;
    background:
        linear-gradient(
            145deg,
            rgba(12, 29, 51, 0.96),
            rgba(6, 15, 28, 0.96)
        );
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
    transition: all 0.2s ease;
}

.how-flow-step:hover {
    border-color: #1769d2;
    transform: translateY(-3px);
    box-shadow: 0 14px 35px rgba(20, 91, 190, 0.16);
}

.flow-number {
    color: #4b9cff;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.flow-icon {
    font-size: 25px;
    margin-bottom: 10px;
}

.flow-title {
    color: #f4f8ff;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 8px;
}

.flow-text {
    color: #8496ae;
    font-size: 11px;
    line-height: 1.7;
}

.flow-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #328cff;
    font-size: 22px;
    font-weight: 700;
}

/* Section headings */

.how-section-title {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 20px;
    margin: 24px 0 12px 0;
}

.how-section-title > div {
    color: #f4f7fc;
    font-size: 18px;
    font-weight: 800;
}

.how-section-title > span {
    color: #71849e;
    font-size: 10px;
}

/* Main cards */

.how-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 18px;
}

.how-card {
    min-height: 185px;
    padding: 20px;
    border: 1px solid #172b47;
    border-radius: 15px;
    background:
        linear-gradient(
            145deg,
            #0b1728,
            #07101d
        );
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    transition: all 0.2s ease;
}

.how-card:hover {
    border-color: #1b65c4;
    transform: translateY(-2px);
}

.how-card-icon {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 11px;
    margin-bottom: 13px;
    background: #0d2440;
    border: 1px solid #173e6b;
    font-size: 19px;
}

.how-card-title {
    color: #f2f6fc;
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 8px;
}

.how-card-text {
    color: #8294ac;
    font-size: 10px;
    line-height: 1.7;
}

.how-card-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 15px;
}

.how-card-tags span {
    padding: 5px 8px;
    border-radius: 7px;
    background: #0c1d32;
    border: 1px solid #1b3453;
    color: #79a8dd;
    font-size: 8px;
    font-weight: 700;
}

/* Detail card */

.how-detail-card {
    margin: 16px 0;
    padding: 20px;
    border: 1px solid #18304f;
    border-radius: 16px;
    background:
        linear-gradient(
            145deg,
            #0b192c,
            #07111f
        );
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
}

.how-detail-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid #17283f;
}

.how-detail-title {
    color: #f3f7fd;
    font-size: 15px;
    font-weight: 800;
}

.how-detail-subtitle {
    color: #7489a5;
    font-size: 10px;
    margin-top: 5px;
}

.how-status {
    white-space: nowrap;
    padding: 7px 10px;
    border-radius: 8px;
    background: #09233c;
    border: 1px solid #164b78;
    color: #5caeff;
    font-size: 8px;
    font-weight: 800;
    letter-spacing: .7px;
}

.how-detail-content {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    padding-top: 16px;
}

.detail-item {
    display: flex;
    gap: 12px;
    padding: 13px;
    border-radius: 11px;
    background: rgba(8, 19, 33, 0.75);
    border: 1px solid #14273f;
}

.detail-icon {
    flex: 0 0 28px;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    background: #0b2b51;
    border: 1px solid #174d82;
    color: #6db5ff;
    font-size: 11px;
    font-weight: 800;
}

.detail-item strong {
    color: #eaf2fc;
    font-size: 11px;
}

.detail-item p {
    margin: 5px 0 0 0;
    color: #788ca5;
    font-size: 9px;
    line-height: 1.6;
}

/* Summary */

.how-summary {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-top: 18px;
    padding: 20px;
    border: 1px solid #1a3c67;
    border-radius: 16px;
    background:
        linear-gradient(
            135deg,
            #0b2340,
            #081426
        );
    box-shadow: 0 12px 35px rgba(8, 70, 150, 0.12);
}

.summary-icon {
    width: 48px;
    height: 48px;
    flex: 0 0 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 13px;
    background: #0d3562;
    border: 1px solid #1c5b9b;
    font-size: 23px;
}

.summary-title {
    color: #f2f7ff;
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 5px;
}

.summary-text {
    color: #8298b3;
    font-size: 10px;
    line-height: 1.7;
}

/* Responsive */

@media (max-width: 1000px) {
    .how-flow {
        grid-template-columns: 1fr 1fr;
    }

    .flow-arrow {
        display: none;
    }

    .how-grid {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 700px) {
    .how-flow,
    .how-grid,
    .how-detail-content {
        grid-template-columns: 1fr;
    }

    .how-section-title {
        display: block;
    }

    .how-section-title > span {
        display: block;
        margin-top: 4px;
    }

    .how-detail-header {
        display: block;
    }

    .how-status {
        display: inline-block;
        margin-top: 10px;
    }
}

/* ============================================================
   GLOBAL FONT SIZE IMPROVEMENT
   ============================================================ */

/* Sidebar */
.brand-name {
    font-size: 18px;
}

.brand-subtitle {
    font-size: 10px;
}

.side-heading {
    font-size: 10px;
}

.nav-active,
section[data-testid="stSidebar"] .stButton > button {
    font-size: 14px;
}

.pro-title {
    font-size: 13px;
}

.pro-text {
    font-size: 10px;
}

.pro-button {
    font-size: 10px;
}

.user-name {
    font-size: 11px;
}

.user-email {
    font-size: 9px;
}


/* Top bar */
.activity-pill {
    font-size: 12px;
}

.control-pill {
    font-size: 12px;
}


/* Page header */
.page-title {
    font-size: 27px;
}

.page-subtitle {
    font-size: 12px;
}


/* Hero */
.hero-label {
    font-size: 11px;
}

.hero-number {
    font-size: 26px;
}

.hero-small {
    font-size: 10px;
}


/* Tabs */
.tab-active,
.tab {
    font-size: 11px;
}


/* Device cards */
.device-name {
    font-size: 13px;
}

.device-meta {
    font-size: 10px;
}


/* Section titles */
.section-title {
    font-size: 13px;
}

.section-link {
    font-size: 10px;
}


/* Category cards */
.category-title {
    font-size: 12px;
}

.category-count {
    font-size: 9px;
}


/* Bottom panels */
.panel-title {
    font-size: 12px;
}

.panel-subtitle {
    font-size: 9px;
}

.panel-link {
    font-size: 9px;
}


/* AI Insight */
.insight-ring {
    font-size: 11px;
}

.insight-text {
    font-size: 10px;
}

.insight-subtext {
    font-size: 8px;
}


/* Alerts */
.alert-row {
    font-size: 9px;
}

.alert-time {
    font-size: 8px;
}

.status-line {
    font-size: 9px;
}


/* Power chart */
.power-mini-label {
    font-size: 9px;
}

.power-mini-value {
    font-size: 14px;
}

.power-chart-footer {
    font-size: 10px;
}


/* Tracking */
.tracking-device-meta {
    font-size: 11px;
}

.tracking-status {
    font-size: 11px;
}

.tracking-metric-label {
    font-size: 9px;
}

.tracking-metric-sub {
    font-size: 9px;
}

.tracking-section-title {
    font-size: 13px;
}

.tracking-section-subtitle {
    font-size: 9px;
}

.activity-title {
    font-size: 10px;
}

.activity-text {
    font-size: 9px;
}

.tracking-empty-title {
    font-size: 13px;
}

.tracking-empty-text {
    font-size: 9px;
}

.tracking-info span {
    font-size: 9px;
}

.tracking-info strong {
    font-size: 11px;
}    

    </style>
    
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def render_html(content: str) -> None:
    """Render a supplied HTML string as real HTML, never as code text."""
    markup = textwrap.dedent(content).strip()

    # st.html is the most direct Streamlit HTML renderer.
    # Fall back to st.markdown for older Streamlit versions.
    if hasattr(st, "html"):
        st.html(markup)
    else:
        st.markdown(markup, unsafe_allow_html=True)

def api_get(path: str, timeout: int = 3):
    """
    Get JSON data from the FastAPI backend.
    """
    try:
        response = requests.get(
            f"{API_URL}{path}",
            timeout=timeout,
        )

        if response.status_code == 200:
            return response.json()

    except requests.RequestException:
        return None

    return None


def normalize_records(data):
    """
    Convert common API response formats into a list.
    """

    if data is None:
        return []

    if isinstance(data, list):
        return data

    if isinstance(data, dict):

        for key in (
            "data",
            "results",
            "devices",
            "predictions",
        ):

            value = data.get(key)

            if isinstance(value, list):
                return value

    return []


def number_value(value, default=0.0):
    """
    Safely convert a value to float.
    """

    try:
        return float(value)

    except (
        TypeError,
        ValueError,
    ):
        return default


def escape(value):
    """
    Safely put backend text inside HTML.
    """

    return html.escape(
        str(value)
    )


# ============================================================
# LOAD BACKEND DATA
# ============================================================

devices_api = api_get("/devices")

ml_api = api_get("/ml-results")

users_api = api_get("/users")

devices = normalize_records(
    devices_api
)

ml_results = normalize_records(
    ml_api
)

api_online = (
    devices_api is not None
    or ml_api is not None
)


# ============================================================
# FALLBACK DEVICE DATA
# ============================================================

# Only used if the backend does not return devices.

if not devices:

    devices = [

        {
            "id": 1,
            "name": "Smart Webcam",
            "device_type": "Camera",
            "room": "Living Room",
            "status": True,
            "power_watts": 7,
        },

        {
            "id": 2,
            "name": "Stereo Speaker",
            "device_type": "Speaker",
            "room": "Living Room",
            "status": True,
            "power_watts": 8,
        },

        {
            "id": 3,
            "name": "Room Light",
            "device_type": "Light",
            "room": "Bedroom",
            "status": False,
            "power_watts": 0,
        },

        {
            "id": 4,
            "name": "Living Room AC",
            "device_type": "AC",
            "room": "Living Room",
            "status": True,
            "power_watts": 1200,
        },

        {
            "id": 5,
            "name": "Kitchen Refrigerator",
            "device_type": "Appliance",
            "room": "Kitchen",
            "status": True,
            "power_watts": 180,
        },

        {
            "id": 6,
            "name": "Smart TV",
            "device_type": "TV",
            "room": "Living Room",
            "status": False,
            "power_watts": 0,
        },

    ]


# ============================================================
# PROJECT METRICS
# ============================================================

active_devices = sum(
    bool(
        device.get(
            "status",
            False
        )
    )
    for device in devices
)


current_power = sum(
    number_value(
        device.get(
            "power_watts",
            0
        )
    )
    for device in devices

    if device.get(
        "status",
        False
    )
)


# These values already exist in the project's
# reference dashboard design.
#
# They are UI/project metrics, not ML predictions.

energy_saved = 25

equivalent_savings = 140



# ============================================================
# PAGE NAVIGATION
# ============================================================

if "page" not in st.session_state:
    st.session_state["page"] = "Home"


def go_to_page(page_name):
    st.session_state["page"] = page_name
    st.rerun()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    render_html(
        """
        <div class="brand">

            <div class="brand-row">

                <div class="brand-logo">
                    🏠
                </div>

                <div>

                    <div class="brand-name">
                        AI Home
                    </div>

                    <div class="brand-subtitle">
                        Smart Home Intelligence
                    </div>

                </div>

            </div>

        </div>
        """
    )

    # --------------------------------------------------------
    # MAIN MENU
    # --------------------------------------------------------

    render_html(
        """
        <div class="side-heading">
            MENUS
        </div>
        """
    )

    # Home
    if st.session_state["page"] == "Home":

        render_html(
            """
            <div class="nav-active">
                🏠 &nbsp; Home
            </div>
            """
        )

    else:

        if st.button(
            "🏠  Home",
            key="nav_home",
            use_container_width=True
        ):
            go_to_page("Home")


    # Tracking
    if st.session_state["page"] == "Tracking":

        render_html(
            """
            <div class="nav-active">
                📊 &nbsp; Tracking
            </div>
            """
        )

    else:

        if st.button(
            "📊  Tracking",
            key="nav_tracking",
            use_container_width=True
        ):
            go_to_page("Tracking")


    # AI Insights
    if st.session_state["page"] == "AI Insights":

        render_html(
            """
            <div class="nav-active">
                ✨ &nbsp; AI Insights
            </div>
            """
        )

    else:

        if st.button(
            "✨  AI Insights",
            key="nav_ai_insights",
            use_container_width=True
        ):
            go_to_page("AI Insights")


    # Automations
    if st.session_state["page"] == "Automations":

        render_html(
            """
            <div class="nav-active">
                ⚙️ &nbsp; Automations
            </div>
            """
        )

    else:

        if st.button(
            "⚙️  Automations",
            key="nav_automations",
            use_container_width=True
        ):
            go_to_page("Automations")


    # Alerts
    if st.session_state["page"] == "Alerts":

        render_html(
            """
            <div class="nav-active">
                🔔 &nbsp; Alerts
            </div>
            """
        )

    else:

        if st.button(
            "🔔  Alerts",
            key="nav_alerts",
            use_container_width=True
        ):
            go_to_page("Alerts")


    # Devices
    if st.session_state["page"] == "Devices":

        render_html(
            """
            <div class="nav-active">
                💡 &nbsp; Devices
            </div>
            """
        )

    else:

        if st.button(
            "💡  Devices",
            key="nav_devices",
            use_container_width=True
        ):
            go_to_page("Devices")


    # Reports
    if st.session_state["page"] == "Reports":

        render_html(
            """
            <div class="nav-active">
                📈 &nbsp; Reports
            </div>
            """
        )

    else:

        if st.button(
            "📈  Reports",
            key="nav_reports",
            use_container_width=True
        ):
            go_to_page("Reports")


    # --------------------------------------------------------
    # ACCOUNT
    # --------------------------------------------------------

    render_html(
        """
        <div class="side-heading">
            ACCOUNT
        </div>
        """
    )


    # Account
    if st.session_state["page"] == "Account":

        render_html(
            """
            <div class="nav-active">
                👤 &nbsp; Account
            </div>
            """
        )

    else:

        if st.button(
            "👤  Account",
            key="nav_account",
            use_container_width=True
        ):
            go_to_page("Account")


    # --------------------------------------------------------
    # SYSTEM
    # --------------------------------------------------------

    render_html(
        """
        <div class="side-heading">
            SYSTEM
        </div>
        """
    )


    # AI Model Center
    if st.session_state["page"] == "AI Model Center":

        render_html(
            """
            <div class="nav-active">
                🧠 &nbsp; AI Model Center
            </div>
            """
        )

    else:

        if st.button(
            "🧠  AI Model Center",
            key="nav_ai_model_center",
            use_container_width=True
        ):
            go_to_page("AI Model Center")


    # Support
    if st.session_state["page"] == "Support":

        render_html(
            """
            <div class="nav-active">
                🛟 &nbsp; Support
            </div>
            """
        )

    else:

        if st.button(
            "🛟  Support",
            key="nav_support",
            use_container_width=True
        ):
            go_to_page("Support")


    # How It Works
    if st.session_state["page"] == "How it works":

        render_html(
            """
            <div class="nav-active">
                ❓ &nbsp; How It Works
            </div>
            """
        )

    else:

        if st.button(
            "❓  How It Works",
            key="nav_how_it_works",
            use_container_width=True
        ):
            go_to_page("How it works")


# ============================================================
# PAGE ROUTING
# ============================================================

current_page = st.session_state["page"]


if current_page == "Tracking":

    # ============================================================
    # TRACKING PAGE
    # ============================================================

    render_html(
        """
        <div class="page-header">
            <div class="page-title">Tracking</div>
            <div class="page-subtitle">
                Real-time device performance, energy usage and activity monitoring.
            </div>
        </div>
        """
    )

    # ------------------------------------------------------------
    # DEVICE + PERIOD FILTERS
    # ------------------------------------------------------------

    device_names = [
        str(d.get("name", "Device"))
        for d in devices
    ]

    if not device_names:
        st.warning("No devices available.")
        st.stop()

    # Keep Device, Period and Refresh on ONE horizontal row.
    filter1, filter2, filter3 = st.columns([3.2, 2.2, 1.25], gap="small")

    with filter1:
        selected_device_name = st.selectbox(
            "Device",
            device_names,
            key="tracking_device_select",
        )

    with filter2:
        selected_period = st.selectbox(
            "Period",
            ["Today", "Last 7 Days", "Last 30 Days"],
            key="tracking_period_select",
        )

    with filter3:
        # Match the height of the selectbox control so Refresh stays on the same row.
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("↻ Refresh", key="tracking_refresh", width="stretch"):
            st.rerun()

    # ------------------------------------------------------------
    # SELECTED DEVICE
    # ------------------------------------------------------------

    selected_device = next(
        (
            d for d in devices
            if str(d.get("name", "Device")) == selected_device_name
        ),
        None,
    )

    if selected_device is None:
        st.warning("No device data is available.")
        st.stop()

    device_name = escape(selected_device.get("name", "Device"))
    device_type = escape(selected_device.get("device_type", "Smart Device"))
    room = escape(selected_device.get("room", "Unknown Room"))
    device_status = bool(selected_device.get("status", False))
    device_power = number_value(selected_device.get("power_watts", 0))

    status_text = "ONLINE" if device_status else "OFFLINE"
    status_class = "tracking-on" if device_status else "tracking-off"

    # ------------------------------------------------------------
    # DEVICE SUMMARY
    # ------------------------------------------------------------

    energy_today = (device_power * 6 / 1000) if device_power > 0 else 0
    peak_power = device_power * 1.15 if device_power > 0 else 0

    render_html(
        f"""
        <div class="tracking-device-card">

            <div class="tracking-device-top">

                <div class="tracking-device-left">
                    <div class="tracking-device-icon">⚡</div>

                    <div>
                        <div class="tracking-device-name">
                            {device_name}
                        </div>

                        <div class="tracking-device-meta">
                            {device_type} &nbsp; • &nbsp; {room}
                        </div>
                    </div>
                </div>

                <div class="tracking-status {status_class}">
                    ● {status_text}
                </div>

            </div>

            <div class="tracking-metrics">

                <div class="tracking-metric">
                    <div class="tracking-metric-label">Current Power</div>
                    <div class="tracking-metric-value">
                        {device_power:.0f} W
                    </div>
                    <div class="tracking-metric-sub">Live reading</div>
                </div>

                <div class="tracking-metric">
                    <div class="tracking-metric-label">Energy Today</div>
                    <div class="tracking-metric-value">
                        {energy_today:.2f} kWh
                    </div>
                    <div class="tracking-metric-sub">Estimated usage</div>
                </div>

                <div class="tracking-metric">
                    <div class="tracking-metric-label">Peak Power</div>
                    <div class="tracking-metric-value">
                        {peak_power:.0f} W
                    </div>
                    <div class="tracking-metric-sub">Estimated peak</div>
                </div>

                <div class="tracking-metric">
                    <div class="tracking-metric-label">AI Status</div>
                    <div class="tracking-metric-value">Normal</div>
                    <div class="tracking-metric-sub">No unusual activity</div>
                </div>

            </div>

        </div>
        """
    )

    # ------------------------------------------------------------
    # POWER TREND + LIVE ACTIVITY
    # ------------------------------------------------------------

    chart_col, activity_col = st.columns([2.1, 1])

    with chart_col:

        # ========================================================
        # INTERACTIVE POWER CONSUMPTION
        # ========================================================

        tracking_rows = []
        selected_id = selected_device.get("id")

        for row in ml_results:
            row_device_id = row.get("device_id") or row.get("device")

            if (
                selected_id is not None
                and row_device_id is not None
                and str(row_device_id) != str(selected_id)
            ):
                continue

            recorded_at = (
                row.get("recorded_at")
                or row.get("created_at")
                or row.get("timestamp")
            )

            actual = row.get("actual_power_watts")
            if actual is None:
                actual = row.get("power_watts", 0)

            predicted = row.get("predicted_power_watts")
            if predicted is None:
                predicted = row.get("predicted_power", actual)

            tracking_rows.append(
                {
                    "Time": recorded_at,
                    "Actual": number_value(actual),
                    "Predicted": number_value(predicted),
                }
            )

        with st.container(border=True):
            if tracking_rows:
                df_tracking = pd.DataFrame(tracking_rows)
                df_tracking["Time"] = pd.to_datetime(
                    df_tracking["Time"], errors="coerce"
                )

                # Keep the most useful recent readings for a clean dashboard.
                df_tracking = df_tracking.tail(100).reset_index(drop=True)
                df_tracking["Reading"] = range(1, len(df_tracking) + 1)

                # When timestamps are missing or nearly identical, use reading
                # number on the X-axis. This prevents the chart collapsing into
                # a single vertical line.
                valid_times = df_tracking["Time"].dropna()
                use_time_axis = (
                    len(valid_times) >= 2
                    and valid_times.nunique() >= 2
                )

                if use_time_axis:
                    df_tracking = df_tracking.sort_values("Time").reset_index(drop=True)
                    df_tracking["Reading"] = range(1, len(df_tracking) + 1)

                latest_actual = number_value(df_tracking["Actual"].iloc[-1])
                latest_predicted = number_value(df_tracking["Predicted"].iloc[-1])
                peak_actual = number_value(df_tracking["Actual"].max())
                difference = latest_predicted - latest_actual

                # Header
                header_col, metric1, metric2, metric3 = st.columns(
                    [2.8, 1, 1, 1],
                    gap="small",
                )

                with header_col:
                    render_html(
                        """
                        <div class="tracking-section-title">
                            Power Consumption
                        </div>
                        <div class="tracking-section-subtitle">
                            Actual vs AI predicted power usage
                        </div>
                        """
                    )

                with metric1:
                    render_html(
                        f"""
                        <div class="power-mini-stat">
                            <div class="power-mini-label">Latest</div>
                            <div class="power-mini-value">{latest_actual:.0f} W</div>
                        </div>
                        """
                    )

                with metric2:
                    render_html(
                        f"""
                        <div class="power-mini-stat">
                            <div class="power-mini-label">AI Prediction</div>
                            <div class="power-mini-value">{latest_predicted:.0f} W</div>
                        </div>
                        """
                    )

                with metric3:
                    render_html(
                        f"""
                        <div class="power-mini-stat">
                            <div class="power-mini-label">Peak</div>
                            <div class="power-mini-value">{peak_actual:.0f} W</div>
                        </div>
                        """
                    )

                # --------------------------------------------------------
                # INTERACTIVE POWER CONSUMPTION CHART
                # --------------------------------------------------------
                # Use Altair directly instead of a raw Vega-Lite spec.
                # This keeps the chart connected to the DataFrame and avoids
                # the blank-chart problem caused by an incorrect data binding.

                chart_df = df_tracking[["Reading", "Time", "Actual", "Predicted"]].copy()
                chart_df["Time Label"] = chart_df["Time"].dt.strftime("%d %b %H:%M:%S")
                chart_df["Time Label"] = chart_df["Time Label"].fillna("Reading")

                long_df = chart_df.melt(
                    id_vars=["Reading", "Time", "Time Label"],
                    value_vars=["Actual", "Predicted"],
                    var_name="Series",
                    value_name="Power",
                )

                long_df["Series"] = long_df["Series"].replace({
                    "Actual": "Actual Power",
                    "Predicted": "AI Predicted",
                })
                long_df["Power"] = pd.to_numeric(long_df["Power"], errors="coerce").fillna(0)

                # Main interactive lines.
                base = alt.Chart(long_df).encode(
                    x=alt.X(
                        "Reading:Q",
                        title="Reading",
                        axis=alt.Axis(
                            tickCount=8,
                            labelColor="#a9b8cf",
                            titleColor="#8290a8",
                            grid=False,
                        ),
                    ),
                    y=alt.Y(
                        "Power:Q",
                        title="Power (W)",
                        scale=alt.Scale(zero=True),
                        axis=alt.Axis(
                            labelColor="#a9b8cf",
                            titleColor="#8290a8",
                            grid=True,
                            gridColor="#1b2940",
                            tickCount=6,
                        ),
                    ),
                    color=alt.Color(
                        "Series:N",
                        scale=alt.Scale(
                            domain=["Actual Power", "AI Predicted"],
                            range=["#65c7ff", "#357cff"],
                        ),
                        legend=alt.Legend(
                            title=None,
                            orient="bottom",
                            labelColor="#dbe7f7",
                        ),
                    ),
                    tooltip=[
                        alt.Tooltip("Series:N", title="Series"),
                        alt.Tooltip("Power:Q", title="Power", format=".0f"),
                        alt.Tooltip("Reading:Q", title="Reading", format=".0f"),
                        alt.Tooltip("Time Label:N", title="Time"),
                    ],
                )

                lines = base.mark_line(
                    interpolate="monotone",
                    strokeWidth=3,
                )

                # Highlight the nearest reading when the mouse moves over the chart.
                nearest = alt.selection_point(
                    fields=["Reading"],
                    nearest=True,
                    on="pointerover",
                    empty=False,
                )

                points = base.mark_circle(size=55).encode(
                    opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
                ).add_params(nearest)

                # Subtle highlight band for the selected reading.
                highlight = alt.Chart(long_df).mark_rule(
                    color="#5aaeff",
                    opacity=0.28,
                    strokeWidth=1,
                ).encode(
                    x="Reading:Q",
                    opacity=alt.condition(nearest, alt.value(0.28), alt.value(0)),
                )

                power_chart = (
                    (lines + highlight + points)
                    .properties(
                        height=350,
                        width="container",
                    )
                    .configure_view(
                        stroke="#1f3048",
                        fill="#050b15",
                    )
                    .configure_axis(
                        domainColor="#20314a",
                        tickColor="#20314a",
                    )
                )

                st.altair_chart(
                    power_chart,
                    width="stretch",
                    theme=None,
                )

                diff_text = (
                    f"+{difference:.0f} W"
                    if difference >= 0
                    else f"{difference:.0f} W"
                )
                diff_class = "positive" if difference >= 0 else "negative"

                render_html(
                    f"""
                    <div class="power-chart-footer">
                        <span>{len(df_tracking)} readings shown</span>
                        <span>Latest AI difference: <b class="{diff_class}">{diff_text}</b></span>
                        <span>Hover over the chart for details</span>
                    </div>
                    """
                )

            else:
                render_html(
                    """
                    <div class="tracking-empty">
                        <div class="tracking-empty-icon">📊</div>
                        <div class="tracking-empty-title">
                            No historical readings
                        </div>
                        <div class="tracking-empty-text">
                            Historical readings will appear here when the backend
                            has data for this device.
                        </div>
                    </div>
                    """
                )


    with activity_col:

        render_html(
            f"""
            <div class="tracking-panel">
                <div class="tracking-section-title">Live Activity</div>
                <div class="tracking-section-subtitle">
                    Latest device state
                </div>

                <div class="tracking-activity-row">
                    <span class="activity-dot">●</span>
                    <div>
                        <div class="activity-title">Device status</div>
                        <div class="activity-text">
                            {status_text} • {escape(selected_period)}
                        </div>
                    </div>
                </div>

                <div class="tracking-activity-row">
                    <span class="activity-dot">⚡</span>
                    <div>
                        <div class="activity-title">Power reading</div>
                        <div class="activity-text">
                            {device_power:.0f} W
                        </div>
                    </div>
                </div>

                <div class="tracking-activity-row">
                    <span class="activity-dot">◉</span>
                    <div>
                        <div class="activity-title">AI monitoring</div>
                        <div class="activity-text">
                            System monitoring active
                        </div>
                    </div>
                </div>

                <div class="tracking-activity-row">
                    <span class="activity-dot">✓</span>
                    <div>
                        <div class="activity-title">Health</div>
                        <div class="activity-text">
                            Normal operation
                        </div>
                    </div>
                </div>

            </div>
            """
        )

    st.stop()
    
    st.stop()


elif current_page == "AI Insights":

    # ============================================================
    # AI INSIGHTS PAGE
    # ============================================================

    render_html(
        """
        <div style="
            margin-top: 28px;
            margin-bottom: 18px;
        ">

            <div style="
                color: #ffffff;
                font-size: 28px;
                font-weight: 800;
                letter-spacing: -0.5px;
            ">
                AI Insights
            </div>

            <div style="
                color: #7890ad;
                font-size: 12px;
                margin-top: 6px;
            ">
                Intelligent analysis of energy usage, predictions and anomalies
            </div>

        </div>
        """
    )

    # ------------------------------------------------------------
    # PREPARE AI DATA
    # ------------------------------------------------------------

    insight_rows = []

    for row in ml_results:

        timestamp = (
            row.get("recorded_at")
            or row.get("created_at")
            or row.get("timestamp")
            or row.get("time")
        )

        actual = number_value(
            row.get(
                "actual_power_watts",
                row.get(
                    "power_watts",
                    row.get(
                        "actual_power",
                        0
                    )
                )
            )
        )

        predicted = number_value(
            row.get(
                "predicted_power_watts",
                row.get(
                    "predicted_power",
                    row.get(
                        "prediction",
                        actual
                    )
                )
            )
        )

        anomaly_raw = row.get(
            "is_anomaly",
            row.get(
                "anomaly",
                row.get(
                    "anomaly_detected",
                    False
                )
            )
        )

        anomaly_status = str(
            row.get(
                "anomaly_status",
                ""
            )
        ).lower()

        is_anomaly = (
            bool(anomaly_raw)
            or "anomaly" in anomaly_status
            or "abnormal" in anomaly_status
            or anomaly_status in {
                "true",
                "1"
            }
        )

        insight_rows.append(
            {
                "Time": timestamp,
                "Actual": actual,
                "Predicted": predicted,
                "Anomaly": is_anomaly,
            }
        )

    insight_df = pd.DataFrame(
        insight_rows
    )

    # ------------------------------------------------------------
    # EMPTY DATA CHECK
    # ------------------------------------------------------------

    if insight_df.empty:

        render_html(
            """
            <div style="
                background: #081323;
                border: 1px solid #183452;
                border-radius: 14px;
                padding: 28px;
                text-align: center;
                margin-top: 18px;
            ">

                <div style="
                    font-size: 30px;
                    margin-bottom: 10px;
                ">
                    🧠
                </div>

                <div style="
                    color: #ffffff;
                    font-size: 16px;
                    font-weight: 700;
                ">
                    No AI insights available
                </div>

                <div style="
                    color: #7188a4;
                    font-size: 11px;
                    margin-top: 7px;
                ">
                    Run the ML prediction pipeline to generate insights.
                </div>

            </div>
            """
        )

        st.stop()

    # ------------------------------------------------------------
    # AI METRICS
    # ------------------------------------------------------------

    total_records = len(
        insight_df
    )

    anomaly_count = int(
        insight_df["Anomaly"].sum()
    )

    average_actual = float(
        insight_df["Actual"].mean()
    )

    average_predicted = float(
        insight_df["Predicted"].mean()
    )

    average_gap = float(
        (
            insight_df["Actual"]
            - insight_df["Predicted"]
        ).abs().mean()
    )

    latest_actual = float(
        insight_df["Actual"].iloc[-1]
    )

    latest_predicted = float(
        insight_df["Predicted"].iloc[-1]
    )

    latest_gap = abs(
        latest_actual
        - latest_predicted
    )

    anomaly_rate = (
        anomaly_count
        / total_records
        * 100
        if total_records > 0
        else 0
    )

    # ------------------------------------------------------------
    # AI STATUS
    # ------------------------------------------------------------

    if anomaly_rate == 0:

        status_text = "System operating normally"
        status_icon = "✓"

    elif anomaly_rate < 5:

        status_text = "Minor unusual activity detected"
        status_icon = "!"

    else:

        status_text = "Attention required"
        status_icon = "⚠"

    # ------------------------------------------------------------
    # TOP SUMMARY
    # ------------------------------------------------------------

    render_html(
        f"""
        <div style="
            display:grid;
            grid-template-columns:repeat(4,1fr);
            gap:12px;
            margin-bottom:16px;
        ">

            <div style="
                background:linear-gradient(
                    135deg,
                    #0c1f3b,
                    #081323
                );
                border:1px solid #174b86;
                border-radius:14px;
                padding:18px;
            ">

                <div style="
                    color:#7896b8;
                    font-size:10px;
                    font-weight:700;
                    text-transform:uppercase;
                ">
                    ML Records
                </div>

                <div style="
                    color:#ffffff;
                    font-size:25px;
                    font-weight:800;
                    margin-top:8px;
                ">
                    {total_records}
                </div>

                <div style="
                    color:#5e7da3;
                    font-size:9px;
                    margin-top:4px;
                ">
                    Analyzed readings
                </div>

            </div>


            <div style="
                background:linear-gradient(
                    135deg,
                    #101d35,
                    #081323
                );
                border:1px solid #183452;
                border-radius:14px;
                padding:18px;
            ">

                <div style="
                    color:#7896b8;
                    font-size:10px;
                    font-weight:700;
                    text-transform:uppercase;
                ">
                    Avg Actual
                </div>

                <div style="
                    color:#ffffff;
                    font-size:25px;
                    font-weight:800;
                    margin-top:8px;
                ">
                    {average_actual:.0f} W
                </div>

                <div style="
                    color:#5e7da3;
                    font-size:9px;
                    margin-top:4px;
                ">
                    Observed energy usage
                </div>

            </div>


            <div style="
                background:linear-gradient(
                    135deg,
                    #101d35,
                    #081323
                );
                border:1px solid #183452;
                border-radius:14px;
                padding:18px;
            ">

                <div style="
                    color:#7896b8;
                    font-size:10px;
                    font-weight:700;
                    text-transform:uppercase;
                ">
                    Prediction Gap
                </div>

                <div style="
                    color:#ffffff;
                    font-size:25px;
                    font-weight:800;
                    margin-top:8px;
                ">
                    {average_gap:.0f} W
                </div>

                <div style="
                    color:#5e7da3;
                    font-size:9px;
                    margin-top:4px;
                ">
                    Average model difference
                </div>

            </div>


            <div style="
                background:linear-gradient(
                    135deg,
                    #101d35,
                    #081323
                );
                border:1px solid #183452;
                border-radius:14px;
                padding:18px;
            ">

                <div style="
                    color:#7896b8;
                    font-size:10px;
                    font-weight:700;
                    text-transform:uppercase;
                ">
                    Anomalies
                </div>

                <div style="
                    color:#ffffff;
                    font-size:25px;
                    font-weight:800;
                    margin-top:8px;
                ">
                    {anomaly_count}
                </div>

                <div style="
                    color:#5e7da3;
                    font-size:9px;
                    margin-top:4px;
                ">
                    {anomaly_rate:.1f}% of records
                </div>

            </div>

        </div>
        """
    )

    # ------------------------------------------------------------
    # AI SYSTEM STATUS
    # ------------------------------------------------------------

    render_html(
        f"""
        <div style="
            background:#081323;
            border:1px solid #183452;
            border-radius:14px;
            padding:18px 20px;
            margin-bottom:16px;
        ">

            <div style="
                display:flex;
                align-items:center;
                gap:12px;
            ">

                <div style="
                    width:38px;
                    height:38px;
                    border-radius:10px;
                    background:#10294a;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:#63a4ff;
                    font-size:18px;
                    font-weight:800;
                ">
                    {status_icon}
                </div>

                <div>

                    <div style="
                        color:#ffffff;
                        font-size:14px;
                        font-weight:700;
                    ">
                        AI System Status
                    </div>

                    <div style="
                        color:#7890ad;
                        font-size:10px;
                        margin-top:4px;
                    ">
                        {status_text}
                    </div>

                </div>

            </div>

        </div>
        """
    )

    # ------------------------------------------------------------
    # AI ANALYSIS
    # ------------------------------------------------------------

    if latest_gap <= average_gap:

        prediction_message = (
            "The latest prediction is close to the model's "
            "average prediction behavior."
        )

    else:

        prediction_message = (
            "The latest reading differs more than usual "
            "from the ML prediction."
        )

    if anomaly_count == 0:

        anomaly_message = (
            "No anomalous energy readings were detected "
            "in the available ML results."
        )

    elif anomaly_rate < 5:

        anomaly_message = (
            f"{anomaly_count} unusual reading(s) were detected. "
            "The anomaly level is currently low."
        )

    else:

        anomaly_message = (
            f"{anomaly_count} anomalous readings were detected. "
            "Energy usage should be reviewed."
        )

    render_html(
        f"""
        <div style="
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:14px;
            margin-bottom:16px;
        ">

            <div style="
                background:#081323;
                border:1px solid #183452;
                border-radius:14px;
                padding:20px;
            ">

                <div style="
                    color:#ffffff;
                    font-size:14px;
                    font-weight:700;
                    margin-bottom:9px;
                ">
                    🔮 Prediction Analysis
                </div>

                <div style="
                    color:#7890ad;
                    font-size:11px;
                    line-height:1.7;
                ">
                    {prediction_message}
                </div>

                <div style="
                    display:flex;
                    gap:30px;
                    margin-top:16px;
                ">

                    <div>

                        <div style="
                            color:#5e7da3;
                            font-size:9px;
                        ">
                            Latest Actual
                        </div>

                        <div style="
                            color:#ffffff;
                            font-size:18px;
                            font-weight:800;
                            margin-top:3px;
                        ">
                            {latest_actual:.0f} W
                        </div>

                    </div>

                    <div>

                        <div style="
                            color:#5e7da3;
                            font-size:9px;
                        ">
                            Latest Predicted
                        </div>

                        <div style="
                            color:#ffffff;
                            font-size:18px;
                            font-weight:800;
                            margin-top:3px;
                        ">
                            {latest_predicted:.0f} W
                        </div>

                    </div>

                </div>

            </div>


            <div style="
                background:#081323;
                border:1px solid #183452;
                border-radius:14px;
                padding:20px;
            ">

                <div style="
                    color:#ffffff;
                    font-size:14px;
                    font-weight:700;
                    margin-bottom:9px;
                ">
                    🚨 Anomaly Analysis
                </div>

                <div style="
                    color:#7890ad;
                    font-size:11px;
                    line-height:1.7;
                ">
                    {anomaly_message}
                </div>

                <div style="
                    margin-top:16px;
                    color:#5e7da3;
                    font-size:9px;
                ">
                    Detection method
                </div>

                <div style="
                    color:#b8c9dd;
                    font-size:11px;
                    font-weight:600;
                    margin-top:4px;
                ">
                    Isolation Forest
                </div>

            </div>

        </div>
        """
    )

    # ------------------------------------------------------------
    # AI EXPLANATION
    # ------------------------------------------------------------

    render_html(
        """
        <div style="
            background:linear-gradient(
                135deg,
                #0b1e38,
                #081323
            );
            border:1px solid #16457d;
            border-radius:14px;
            padding:20px;
            margin-bottom:16px;
        ">

            <div style="
                color:#ffffff;
                font-size:14px;
                font-weight:700;
            ">
                🧠 How AI is analyzing your home
            </div>

            <div style="
                color:#7890ad;
                font-size:11px;
                line-height:1.8;
                margin-top:9px;
            ">
                The energy prediction model estimates expected power
                consumption from the available home sensor data.
                The anomaly detection model identifies readings that
                behave differently from normal energy patterns.
                These results are stored in PostgreSQL and displayed
                here as explainable AI insights.
            </div>

            <div style="
                display:grid;
                grid-template-columns:repeat(3,1fr);
                gap:10px;
                margin-top:16px;
            ">

                <div style="
                    background:#09182b;
                    border:1px solid #17334f;
                    border-radius:10px;
                    padding:13px;
                ">

                    <div style="
                        color:#5f9fff;
                        font-size:10px;
                        font-weight:700;
                    ">
                        01
                    </div>

                    <div style="
                        color:#dbe8f7;
                        font-size:11px;
                        font-weight:700;
                        margin-top:5px;
                    ">
                        Sensor Data
                    </div>

                </div>


                <div style="
                    background:#09182b;
                    border:1px solid #17334f;
                    border-radius:10px;
                    padding:13px;
                ">

                    <div style="
                        color:#5f9fff;
                        font-size:10px;
                        font-weight:700;
                    ">
                        02
                    </div>

                    <div style="
                        color:#dbe8f7;
                        font-size:11px;
                        font-weight:700;
                        margin-top:5px;
                    ">
                        ML Prediction
                    </div>

                </div>


                <div style="
                    background:#09182b;
                    border:1px solid #17334f;
                    border-radius:10px;
                    padding:13px;
                ">

                    <div style="
                        color:#5f9fff;
                        font-size:10px;
                        font-weight:700;
                    ">
                        03
                    </div>

                    <div style="
                        color:#dbe8f7;
                        font-size:11px;
                        font-weight:700;
                        margin-top:5px;
                    ">
                        AI Insight
                    </div>

                </div>

            </div>

        </div>
        """
    )

    # ------------------------------------------------------------
    # RECENT AI EVENTS
    # ------------------------------------------------------------

    recent_ai = insight_df.tail(
        6
    ).iloc[::-1]

    activity_html = ""

    for _, row in recent_ai.iterrows():

        if bool(row["Anomaly"]):

            event_icon = "⚠"
            event_title = "Anomaly detected"

        else:

            event_icon = "✓"
            event_title = "Normal energy pattern"

        timestamp = row["Time"]

        if pd.notna(timestamp):

            try:

                time_text = pd.to_datetime(
                    timestamp
                ).strftime(
                    "%b %d · %H:%M"
                )

            except Exception:

                time_text = "Time unavailable"

        else:

            time_text = "Time unavailable"

        activity_html += f"""
        <div style="
            display:flex;
            align-items:center;
            gap:12px;
            padding:12px 0;
            border-bottom:1px solid #12263d;
        ">

            <div style="
                width:30px;
                height:30px;
                border-radius:8px;
                background:#10233b;
                display:flex;
                align-items:center;
                justify-content:center;
                color:#69a9ff;
                font-size:12px;
            ">
                {event_icon}
            </div>

            <div style="
                flex:1;
            ">

                <div style="
                    color:#dce8f6;
                    font-size:11px;
                    font-weight:700;
                ">
                    {event_title}
                </div>

                <div style="
                    color:#607995;
                    font-size:9px;
                    margin-top:3px;
                ">
                    {time_text}
                    · Actual {row["Actual"]:.0f} W
                    · Predicted {row["Predicted"]:.0f} W
                </div>

            </div>

        </div>
        """

    render_html(
        f"""
        <div style="
            background:#081323;
            border:1px solid #183452;
            border-radius:14px;
            padding:20px;
        ">

            <div style="
                color:#ffffff;
                font-size:14px;
                font-weight:700;
            ">
                Recent AI Events
            </div>

            <div style="
                color:#7890ad;
                font-size:10px;
                margin-top:4px;
                margin-bottom:5px;
            ">
                Latest ML observations from the backend
            </div>

            {activity_html}

        </div>
        """
    )

    st.stop()
    
elif current_page == "Automations":

    # ============================================================
    # AUTOMATIONS PAGE
    # ============================================================

    automations_api = api_get("/automations")
    automations = normalize_records(automations_api)

    active_automations = [
        automation
        for automation in automations
        if bool(automation.get("status", False))
    ]

    inactive_automations = [
        automation
        for automation in automations
        if not bool(automation.get("status", False))
    ]

    render_html(
        """
        <div class="page-header">
            <div class="page-title">
                Automations
            </div>

            <div class="page-subtitle">
                Create and manage smart rules for your home.
            </div>
        </div>
        """
    )

    # ============================================================
    # AUTOMATION SUMMARY
    # ============================================================

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        render_html(
            f"""
            <div class="account-stat">
                <div class="account-stat-label">
                    TOTAL AUTOMATIONS
                </div>
                <div class="account-stat-value">
                    {len(automations)}
                </div>
            </div>
            """
        )

    with metric_col2:
        render_html(
            f"""
            <div class="account-stat">
                <div class="account-stat-label">
                    ACTIVE
                </div>
                <div class="account-stat-value">
                    {len(active_automations)}
                </div>
            </div>
            """
        )

    with metric_col3:
        render_html(
            f"""
            <div class="account-stat">
                <div class="account-stat-label">
                    INACTIVE
                </div>
                <div class="account-stat-value">
                    {len(inactive_automations)}
                </div>
            </div>
            """
        )

    st.markdown("")

    # ============================================================
    # ADD AUTOMATION
    # ============================================================

    with st.expander("➕ Create New Automation", expanded=False):

        automation_name = st.text_input(
            "Automation Name",
            placeholder="Example: Turn AC off when temperature drops",
            key="automation_name",
        )

        device_options = {
            str(device.get("name", "Unknown Device")):
            device.get("id")
            for device in devices
        }

        selected_device_name = st.selectbox(
            "Device",
            list(device_options.keys())
            if device_options
            else ["No devices available"],
            key="automation_device",
        )

        trigger_type = st.selectbox(
            "Trigger",
            [
                "Temperature",
                "High Power",
                "Device Status",
                "Schedule",
            ],
            key="automation_trigger_type",
        )

        trigger_value = st.text_input(
            "Trigger Value",
            placeholder="Example: 30",
            key="automation_trigger_value",
        )

        action = st.selectbox(
            "Action",
            [
                "Turn ON",
                "Turn OFF",
            ],
            key="automation_action",
        )

        schedule_time = st.text_input(
            "Schedule Time",
            placeholder="HH:MM",
            key="automation_schedule_time",
        )

        automation_status = st.checkbox(
            "Active",
            value=True,
            key="automation_status",
        )

        if st.button(
            "Create Automation",
            type="primary",
            use_container_width=True,
            key="create_automation",
        ):

            if not automation_name.strip():
                st.warning(
                    "Please enter an automation name."
                )

            else:

                selected_device_id = (
                    device_options.get(
                        selected_device_name
                    )
                )

                try:

                    response = requests.post(
                        f"{API_URL}/automations",
                        params={
                            "name": automation_name.strip(),
                            "device_id": selected_device_id,
                            "trigger_type": trigger_type,
                            "trigger_value": trigger_value,
                            "action": action,
                            "schedule_time": schedule_time,
                            "status": automation_status,
                        },
                        timeout=5,
                    )

                    if response.status_code == 200:

                        st.success(
                            "Automation created successfully."
                        )

                        st.rerun()

                    else:

                        st.error(
                            f"Could not create automation. "
                            f"HTTP {response.status_code}"
                        )

                except requests.RequestException as exc:

                    st.error(
                        f"Backend connection failed: {exc}"
                    )

    # ============================================================
    # AUTOMATION LIST
    # ============================================================

    st.markdown("### Your Automations")

    if not automations:

        st.info(
            "No automations created yet."
        )

    for automation in automations:

        automation_id = automation.get("id")

        automation_name = str(
            automation.get(
                "name",
                "Unnamed Automation"
            )
        )

        device_name = str(
            automation.get(
                "device_name",
                "Unknown Device"
            )
        )

        trigger = str(
            automation.get(
                "trigger_type",
                "Unknown Trigger"
            )
        )

        trigger_value = str(
            automation.get(
                "trigger_value",
                ""
            )
        )

        automation_action = str(
            automation.get(
                "action",
                "Unknown Action"
            )
        )

        is_active = bool(
            automation.get(
                "status",
                False
            )
        )

        status_text = (
            "ACTIVE"
            if is_active
            else "INACTIVE"
        )

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [5, 2, 3],
                gap="small",
            )

            with col1:

                render_html(
                    f"""
                    <div>
                        <div style="
                            color:#ffffff;
                            font-size:14px;
                            font-weight:800;
                        ">
                            ⚙️ {escape(automation_name)}
                        </div>

                        <div style="
                            color:#6688b2;
                            font-size:11px;
                            margin-top:5px;
                        ">
                            {escape(device_name)}
                        </div>

                        <div style="
                            color:#8faacc;
                            font-size:10px;
                            margin-top:4px;
                        ">
                            {escape(trigger)}
                            {escape(trigger_value)}
                            →
                            {escape(automation_action)}
                        </div>
                    </div>
                    """
                )

            with col2:

                render_html(
                    f"""
                    <div style="
                        color:#39e6aa;
                        font-size:10px;
                        font-weight:800;
                        padding-top:8px;
                    ">
                        ● {status_text}
                    </div>
                    """
                )

            with col3:

                toggle_label = (
                    "⏻ Turn OFF"
                    if is_active
                    else "⏻ Turn ON"
                )

                if st.button(
                    toggle_label,
                    key=f"automation_toggle_{automation_id}",
                    use_container_width=True,
                ):

                    try:

                        response = requests.patch(
                            f"{API_URL}/automations/"
                            f"{automation_id}/status",
                            params={
                                "status": not is_active
                            },
                            timeout=5,
                        )

                        if response.status_code == 200:
                            st.rerun()

                        else:
                            st.error(
                                "Could not change automation status."
                            )

                    except requests.RequestException as exc:

                        st.error(
                            f"Backend connection failed: {exc}"
                        )

                if st.button(
                    "🗑️ Delete",
                    key=f"automation_delete_{automation_id}",
                    use_container_width=True,
                ):

                    try:

                        response = requests.delete(
                            f"{API_URL}/automations/"
                            f"{automation_id}",
                            timeout=5,
                        )

                        if response.status_code == 200:

                            st.success(
                                "Automation deleted successfully."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Could not delete automation."
                            )

                    except requests.RequestException as exc:

                        st.error(
                            f"Backend connection failed: {exc}"
                        )

    st.stop()
    
elif current_page == "Alerts":

    # ============================================================
    # ALERTS PAGE
    # ============================================================

    sensor_api = api_get("/sensor-readings")
    sensor_readings = normalize_records(sensor_api)

    alert_rows = []

    # ------------------------------------------------------------
    # AI ANOMALY ALERTS
    # ------------------------------------------------------------

    for row in ml_results:

        anomaly_raw = row.get(
            "is_anomaly",
            row.get(
                "anomaly",
                row.get("anomaly_detected", False),
            ),
        )

        anomaly_status = str(
            row.get("anomaly_status", "")
        ).lower()

        is_anomaly = (
            bool(anomaly_raw)
            or "anomaly" in anomaly_status
            or "abnormal" in anomaly_status
            or anomaly_status in {"true", "1"}
        )

        if not is_anomaly:
            continue

        actual = number_value(
            row.get(
                "actual_power_watts",
                row.get(
                    "actual_power",
                    row.get("power_watts", 0),
                ),
            )
        )

        predicted = number_value(
            row.get(
                "predicted_power_watts",
                row.get(
                    "predicted_power",
                    row.get("prediction", actual),
                ),
            )
        )

        gap = abs(actual - predicted)

        severity = "High" if gap >= 250 else "Medium"

        timestamp = row.get(
            "recorded_at",
            row.get("timestamp", ""),
        )

        alert_rows.append(
            {
                "time": timestamp,
                "type": "AI Anomaly",
                "severity": severity,
                "device": "Home Energy Model",
                "title": "Unusual energy pattern detected",
                "detail": (
                    f"Actual {actual:.0f} W vs predicted {predicted:.0f} W"
                ),
                "source": "Isolation Forest",
            }
        )

    # ------------------------------------------------------------
    # SENSOR ALERTS
    # ------------------------------------------------------------

    device_lookup = {
        str(device.get("id")): device
        for device in devices
    }

    for reading in sensor_readings:

        temperature = number_value(
            reading.get("temperature", 0)
        )

        humidity = number_value(
            reading.get("humidity", 0)
        )

        power = number_value(
            reading.get("power_watts", 0)
        )

        device = device_lookup.get(
            str(reading.get("device_id")),
            {},
        )

        device_name = str(
            device.get(
                "name",
                f"Device {reading.get('device_id', '')}",
            )
        )

        timestamp = reading.get(
            "recorded_at",
            reading.get("timestamp", ""),
        )

        if temperature >= 32:

            alert_rows.append(
                {
                    "time": timestamp,
                    "type": "Temperature",
                    "severity": "High",
                    "device": device_name,
                    "title": "High temperature detected",
                    "detail": (
                        f"Temperature reached "
                        f"{temperature:.1f} °C"
                    ),
                    "source": "Sensor Reading",
                }
            )

        elif temperature >= 30:

            alert_rows.append(
                {
                    "time": timestamp,
                    "type": "Temperature",
                    "severity": "Medium",
                    "device": device_name,
                    "title": "Temperature is elevated",
                    "detail": (
                        f"Temperature reached "
                        f"{temperature:.1f} °C"
                    ),
                    "source": "Sensor Reading",
                }
            )

        if power >= 1000:

            alert_rows.append(
                {
                    "time": timestamp,
                    "type": "High Power",
                    "severity": "High",
                    "device": device_name,
                    "title": "High power usage detected",
                    "detail": (
                        f"Power consumption reached "
                        f"{power:.0f} W"
                    ),
                    "source": "Sensor Reading",
                }
            )

        if humidity >= 80:

            alert_rows.append(
                {
                    "time": timestamp,
                    "type": "Humidity",
                    "severity": "Medium",
                    "device": device_name,
                    "title": "High humidity detected",
                    "detail": (
                        f"Humidity reached "
                        f"{humidity:.0f}%"
                    ),
                    "source": "Sensor Reading",
                }
            )

    # ------------------------------------------------------------
    # SORT ALERTS
    # ------------------------------------------------------------

    def alert_sort_key(item):

        try:
            return pd.to_datetime(
                item.get("time"),
                errors="coerce",
            )

        except Exception:

            return pd.Timestamp.min


    alert_rows.sort(
        key=alert_sort_key,
        reverse=True,
    )

    # Keep dashboard responsive.
    alert_rows = alert_rows[:250]

    high_count = sum(
        item["severity"] == "High"
        for item in alert_rows
    )

    medium_count = sum(
        item["severity"] == "Medium"
        for item in alert_rows
    )

    anomaly_count = sum(
        item["type"] == "AI Anomaly"
        for item in alert_rows
    )

    # ============================================================
    # HEADER
    # ============================================================

    render_html(
        """
        <div class="page-header">

            <div class="page-title">
                Alerts
            </div>

            <div class="page-subtitle">
                AI and sensor-based events detected across your smart home.
            </div>

        </div>
        """
    )

    # ============================================================
    # SUMMARY CARDS
    # ============================================================

    summary1, summary2, summary3, summary4 = st.columns(4)

    summary_items = [
        (
            summary1,
            "TOTAL ALERTS",
            len(alert_rows),
            "All detected events",
        ),
        (
            summary2,
            "HIGH PRIORITY",
            high_count,
            "Needs attention",
        ),
        (
            summary3,
            "MEDIUM",
            medium_count,
            "Monitor these events",
        ),
        (
            summary4,
            "AI ANOMALIES",
            anomaly_count,
            "ML-detected patterns",
        ),
    ]

    for column, label, value, subtitle in summary_items:

        with column:

            render_html(
                f"""
                <div style="
                    background:#081323;
                    border:1px solid #183452;
                    border-radius:14px;
                    padding:15px;
                    min-height:92px;
                ">

                    <div style="
                        color:#6f8fb7;
                        font-size:9px;
                        font-weight:800;
                        letter-spacing:.6px;
                    ">
                        {escape(label)}
                    </div>

                    <div style="
                        color:#ffffff;
                        font-size:24px;
                        font-weight:800;
                        margin-top:7px;
                    ">
                        {value}
                    </div>

                    <div style="
                        color:#607995;
                        font-size:9px;
                        margin-top:3px;
                    ">
                        {escape(subtitle)}
                    </div>

                </div>
                """
            )

    st.markdown("")

    # ============================================================
    # FILTERS
    # ============================================================

    filter_col1, filter_col2, filter_col3 = st.columns(
        [1.2, 1.2, 2.2]
    )

    with filter_col1:

        severity_filter = st.selectbox(
            "Severity",
            [
                "All",
                "High",
                "Medium",
            ],
            key="alerts_severity_filter",
        )

    with filter_col2:

        type_filter = st.selectbox(
            "Type",
            [
                "All",
                "AI Anomaly",
                "High Power",
                "Temperature",
                "Humidity",
            ],
            key="alerts_type_filter",
        )

    with filter_col3:

        alert_search = st.text_input(
            "Search alerts",
            placeholder="Search device, alert or source...",
            key="alerts_search",
        )

    filtered_alerts = []

    search_term = alert_search.strip().lower()

    for alert in alert_rows:

        matches_severity = (
            severity_filter == "All"
            or alert["severity"] == severity_filter
        )

        matches_type = (
            type_filter == "All"
            or alert["type"] == type_filter
        )

        searchable = " ".join(
            [
                str(alert.get("device", "")),
                str(alert.get("title", "")),
                str(alert.get("detail", "")),
                str(alert.get("source", "")),
            ]
        ).lower()

        matches_search = (
            not search_term
            or search_term in searchable
        )

        if (
            matches_severity
            and matches_type
            and matches_search
        ):
            filtered_alerts.append(alert)

    # ============================================================
    # RECENT ALERTS
    # ============================================================

    render_html(
        """
        <div style="
            color:#ffffff;
            font-size:15px;
            font-weight:800;
            margin-top:20px;
            margin-bottom:10px;
        ">
            Recent Alerts
        </div>
        """
    )

    if not filtered_alerts:

        render_html(
            """
            <div style="
                background:#081323;
                border:1px solid #183452;
                border-radius:14px;
                padding:25px;
                color:#7890ad;
                font-size:12px;
                text-align:center;
            ">
                No alerts match the current filters.
            </div>
            """
        )

    severity_colors = {
        "High": "#ff6678",
        "Medium": "#ffb638",
    }

    for alert in filtered_alerts[:50]:

        severity = alert["severity"]

        severity_color = severity_colors.get(
            severity,
            "#7f9fc8",
        )

        time_value = alert.get(
            "time",
            "",
        )

        try:

            parsed_time = pd.to_datetime(
                time_value,
                errors="coerce",
            )

            if pd.notna(parsed_time):

                time_text = parsed_time.strftime(
                    "%d %b %Y · %H:%M"
                )

            else:

                time_text = str(time_value)

        except Exception:

            time_text = str(time_value)

        render_html(
            f"""
            <div style="
                background:#081323;
                border:1px solid #183452;
                border-radius:14px;
                padding:15px 17px;
                margin-bottom:9px;
            ">

                <div style="
                    display:flex;
                    align-items:flex-start;
                    justify-content:space-between;
                    gap:15px;
                ">

                    <div style="flex:1;">

                        <div style="
                            color:#ffffff;
                            font-size:13px;
                            font-weight:800;
                        ">
                            {"🚨" if severity == "High" else "⚠️"}
                            &nbsp;
                            {escape(alert["title"])}
                        </div>

                        <div style="
                            color:#7695b9;
                            font-size:10px;
                            margin-top:5px;
                        ">
                            {escape(alert["device"])}
                            &nbsp; · &nbsp;
                            {escape(alert["type"])}
                        </div>

                        <div style="
                            color:#a5bad4;
                            font-size:10px;
                            margin-top:7px;
                        ">
                            {escape(alert["detail"])}
                        </div>

                        <div style="
                            color:#607995;
                            font-size:9px;
                            margin-top:6px;
                        ">
                            {escape(time_text)}
                            &nbsp; · &nbsp;
                            Source:
                            {escape(alert["source"])}
                        </div>

                    </div>

                    <div style="
                        color:{severity_color};
                        border:1px solid {severity_color};
                        border-radius:999px;
                        padding:5px 9px;
                        font-size:9px;
                        font-weight:800;
                        white-space:nowrap;
                    ">
                        {escape(severity.upper())}
                    </div>

                </div>

            </div>
            """
        )

    # ============================================================
    # DATABASE STATUS
    # ============================================================

    render_html(
        f"""
        <div style="
            color:#607995;
            font-size:9px;
            margin-top:14px;
            padding-bottom:5px;
        ">
            Live data sources:
            ML Results ({len(ml_results):,})
            · Sensor Readings ({len(sensor_readings):,})
            · Devices ({len(devices):,})
        </div>
        """
    )

    # ============================================================
    # OPEN AI INSIGHTS
    # ============================================================

    if st.button(
        "↗",
        key="alerts_open_ai_insights",
        help="Open AI insights",
    ):

        go_to_page(
            "AI Insights"
        )

    st.stop()    
    
elif current_page == "Devices":

    # ============================================================
    # DEVICES PAGE
    # ============================================================

    sensor_api = api_get("/sensor-readings")
    sensor_readings = normalize_records(
        sensor_api
    )

    # ------------------------------------------------------------
    # DEVICE LOOKUP
    # ------------------------------------------------------------

    device_lookup = {
        str(device.get("id")): device
        for device in devices
    }

    # ------------------------------------------------------------
    # LATEST SENSOR READING PER DEVICE
    # ------------------------------------------------------------

    latest_readings = {}

    for reading in sensor_readings:

        device_id = str(
            reading.get(
                "device_id",
                ""
            )
        )

        recorded_at = reading.get(
            "recorded_at",
            ""
        )

        try:
            recorded_time = pd.to_datetime(
                recorded_at,
                errors="coerce"
            )
        except Exception:
            recorded_time = pd.NaT

        if device_id not in latest_readings:

            latest_readings[device_id] = (
                reading,
                recorded_time
            )

        else:

            previous_time = (
                latest_readings[device_id][1]
            )

            if (
                pd.notna(recorded_time)
                and (
                    pd.isna(previous_time)
                    or recorded_time > previous_time
                )
            ):

                latest_readings[device_id] = (
                    reading,
                    recorded_time
                )

    # ============================================================
    # DEVICE METRICS
    # ============================================================

    total_devices = len(devices)

    active_devices_count = sum(
        bool(
            device.get(
                "status",
                False
            )
        )
        for device in devices
    )

    inactive_devices_count = (
        total_devices
        - active_devices_count
    )

    total_power = sum(
        number_value(
            device.get(
                "power_watts",
                0
            )
        )
        for device in devices
        if bool(
            device.get(
                "status",
                False
            )
        )
    )

    # ============================================================
    # HEADER
    # ============================================================

    render_html(
        """
        <div class="page-header">

            <div class="page-title">
                Devices
            </div>

            <div class="page-subtitle">
                Manage connected devices, monitor live activity
                and maintain your smart-home device network.
            </div>

        </div>
        """
    )

    # ============================================================
    # SUMMARY
    # ============================================================

    metric1, metric2, metric3, metric4 = st.columns(4)

    device_metrics = [
        (
            metric1,
            "TOTAL DEVICES",
            total_devices,
            "Connected devices"
        ),
        (
            metric2,
            "ACTIVE",
            active_devices_count,
            "Currently enabled"
        ),
        (
            metric3,
            "INACTIVE",
            inactive_devices_count,
            "Currently disabled"
        ),
        (
            metric4,
            "CURRENT POWER",
            f"{total_power:.0f} W",
            "Active device load"
        ),
    ]

    for column, label, value, subtitle in device_metrics:

        with column:

            render_html(
                f"""
                <div style="
                    background:#081323;
                    border:1px solid #183452;
                    border-radius:14px;
                    padding:15px;
                    min-height:92px;
                ">

                    <div style="
                        color:#6f8fb7;
                        font-size:9px;
                        font-weight:800;
                        letter-spacing:.6px;
                    ">
                        {escape(label)}
                    </div>

                    <div style="
                        color:#ffffff;
                        font-size:23px;
                        font-weight:800;
                        margin-top:7px;
                    ">
                        {escape(value)}
                    </div>

                    <div style="
                        color:#607995;
                        font-size:9px;
                        margin-top:3px;
                    ">
                        {escape(subtitle)}
                    </div>

                </div>
                """
            )

    st.markdown("")

    # ============================================================
    # ADD DEVICE
    # ============================================================

    with st.expander(
        "➕ Add New Device",
        expanded=False
    ):

        add_col1, add_col2 = st.columns(2)

        with add_col1:

            new_device_name = st.text_input(
                "Device Name",
                placeholder="Example: Bedroom Fan",
                key="new_device_name"
            )

            new_device_type = st.selectbox(
                "Device Type",
                [
                    "AC",
                    "Light",
                    "Fan",
                    "TV",
                    "Speaker",
                    "Camera",
                    "Appliance",
                    "Other",
                ],
                key="new_device_type"
            )

        with add_col2:

            new_device_room = st.text_input(
                "Room",
                placeholder="Example: Bedroom",
                key="new_device_room"
            )

            new_device_power = st.number_input(
                "Power Consumption (W)",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key="new_device_power"
            )

            new_device_status = st.checkbox(
                "Active",
                value=True,
                key="new_device_status"
            )

        if st.button(
            "Add Device",
            key="add_device_button",
            type="primary",
            use_container_width=True
        ):

            if not new_device_name.strip():

                st.warning(
                    "Please enter a device name."
                )

            elif not new_device_room.strip():

                st.warning(
                    "Please enter a room."
                )

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/devices",
                        params={
                            "name": new_device_name.strip(),
                            "device_type": new_device_type,
                            "room": new_device_room.strip(),
                            "status": new_device_status,
                            "power_watts": new_device_power,
                        },
                        timeout=5
                    )

                    if response.status_code == 200:

                        st.success(
                            "Device added successfully."
                        )

                        st.rerun()

                    else:

                        st.error(
                            f"Could not add device. "
                            f"HTTP {response.status_code}"
                        )

                except requests.RequestException as exc:

                    st.error(
                        f"Backend connection failed: {exc}"
                    )

    # ============================================================
    # FILTERS
    # ============================================================

    filter1, filter2, filter3 = st.columns(
        [1.2, 1.2, 2.2]
    )

    with filter1:

        device_status_filter = st.selectbox(
            "Status",
            [
                "All",
                "Active",
                "Inactive",
            ],
            key="device_status_filter"
        )

    with filter2:

        device_types = sorted(
            {
                str(
                    device.get(
                        "device_type",
                        "Unknown"
                    )
                )
                for device in devices
            }
        )

        device_type_filter = st.selectbox(
            "Device Type",
            [
                "All"
            ] + device_types,
            key="device_type_filter"
        )

    with filter3:

        device_search = st.text_input(
            "Search devices",
            placeholder="Search device, room or type...",
            key="device_search"
        )

    # ============================================================
    # FILTER DEVICE LIST
    # ============================================================

    filtered_devices = []

    search_term = (
        device_search
        .strip()
        .lower()
    )

    for device in devices:

        device_name = str(
            device.get(
                "name",
                "Unknown Device"
            )
        )

        device_type = str(
            device.get(
                "device_type",
                "Unknown"
            )
        )

        room_name = str(
            device.get(
                "room",
                "Unknown Room"
            )
        )

        is_active = bool(
            device.get(
                "status",
                False
            )
        )

        status_name = (
            "Active"
            if is_active
            else "Inactive"
        )

        matches_status = (
            device_status_filter == "All"
            or status_name == device_status_filter
        )

        matches_type = (
            device_type_filter == "All"
            or device_type == device_type_filter
        )

        searchable = (
            f"{device_name} "
            f"{device_type} "
            f"{room_name}"
        ).lower()

        matches_search = (
            not search_term
            or search_term in searchable
        )

        if (
            matches_status
            and matches_type
            and matches_search
        ):

            filtered_devices.append(
                device
            )

    # ============================================================
    # DEVICE LIST
    # ============================================================

    render_html(
        """
        <div style="
            color:#ffffff;
            font-size:15px;
            font-weight:800;
            margin-top:20px;
            margin-bottom:10px;
        ">
            Connected Devices
        </div>
        """
    )

    icon_map = {
        "AC": "❄️",
        "Light": "💡",
        "Fan": "🌀",
        "TV": "📺",
        "Speaker": "🔊",
        "Camera": "📹",
        "Appliance": "🧊",
        "Other": "⚡",
    }

    # ------------------------------------------------------------
    # DEVICE CARDS
    # ------------------------------------------------------------

    for device in filtered_devices:

        device_id = device.get(
            "id"
        )

        device_name = str(
            device.get(
                "name",
                "Unknown Device"
            )
        )

        device_type = str(
            device.get(
                "device_type",
                "Other"
            )
        )

        room_name = str(
            device.get(
                "room",
                "Unknown Room"
            )
        )

        is_active = bool(
            device.get(
                "status",
                False
            )
        )

        device_power = number_value(
            device.get(
                "power_watts",
                0
            )
        )

        icon = icon_map.get(
            device_type,
            "⚡"
        )

        latest = latest_readings.get(
            str(device_id)
        )

        temperature_text = "—"
        humidity_text = "—"
        latest_power = device_power
        latest_time = "No recent reading"

        if latest:

            reading = latest[0]

            temperature = number_value(
                reading.get(
                    "temperature",
                    0
                )
            )

            humidity = number_value(
                reading.get(
                    "humidity",
                    0
                )
            )

            latest_power = number_value(
                reading.get(
                    "power_watts",
                    device_power
                )
            )

            temperature_text = (
                f"{temperature:.1f} °C"
            )

            humidity_text = (
                f"{humidity:.0f}%"
            )

            try:

                parsed_time = pd.to_datetime(
                    reading.get(
                        "recorded_at",
                        ""
                    ),
                    errors="coerce"
                )

                if pd.notna(parsed_time):

                    latest_time = (
                        parsed_time.strftime(
                            "%d %b %Y · %H:%M"
                        )
                    )

            except Exception:

                pass

        status_color = (
            "#31d68e"
            if is_active
            else "#77869a"
        )

        status_text = (
            "ACTIVE"
            if is_active
            else "INACTIVE"
        )

        with st.container(
            border=True
        ):

            top_col1, top_col2 = st.columns(
                [5, 1.5]
            )

            with top_col1:

                render_html(
                    f"""
                    <div style="
                        display:flex;
                        align-items:center;
                        gap:12px;
                    ">

                        <div style="
                            width:46px;
                            height:46px;
                            border-radius:13px;
                            background:#102544;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            font-size:21px;
                        ">
                            {icon}
                        </div>

                        <div>

                            <div style="
                                color:#ffffff;
                                font-size:14px;
                                font-weight:800;
                            ">
                                {escape(device_name)}
                            </div>

                            <div style="
                                color:#6688b2;
                                font-size:10px;
                                margin-top:3px;
                            ">
                                {escape(room_name)}
                                &nbsp; · &nbsp;
                                {escape(device_type)}
                            </div>

                        </div>

                    </div>
                    """
                )

            with top_col2:

                render_html(
                    f"""
                    <div style="
                        color:{status_color};
                        font-size:10px;
                        font-weight:800;
                        text-align:right;
                        padding-top:8px;
                    ">
                        ● {status_text}
                    </div>
                    """
                )

            st.markdown("")

            info1, info2, info3, info4 = st.columns(4)

            with info1:

                st.metric(
                    "Power",
                    f"{latest_power:.0f} W"
                )

            with info2:

                st.metric(
                    "Temperature",
                    temperature_text
                )

            with info3:

                st.metric(
                    "Humidity",
                    humidity_text
                )

            with info4:

                st.metric(
                    "Device ID",
                    str(device_id)
                )

            st.caption(
                f"Latest reading: {latest_time}"
            )

            # ----------------------------------------------------
            # DEVICE ACTIONS
            # ----------------------------------------------------

            action1, action2, action3 = st.columns(
                3,
                gap="small"
            )

            with action1:

                if st.button(
                    "✏️ Edit",
                    key=f"edit_device_{device_id}",
                    use_container_width=True
                ):

                    st.session_state[
                        "edit_device_id"
                    ] = device_id

                    st.rerun()

            with action2:

                toggle_text = (
                    "⏻ Turn OFF"
                    if is_active
                    else "⏻ Turn ON"
                )

                if st.button(
                    toggle_text,
                    key=f"toggle_device_{device_id}",
                    use_container_width=True
                ):

                    try:

                        response = requests.put(
                            f"{API_URL}/devices/{device_id}",
                            params={
                                "name": device_name,
                                "device_type": device_type,
                                "room": room_name,
                                "status": not is_active,
                                "power_watts": device_power,
                            },
                            timeout=5
                        )

                        if response.status_code == 200:

                            st.rerun()

                        else:

                            st.error(
                                "Could not change device status."
                            )

                    except requests.RequestException as exc:

                        st.error(
                            f"Backend connection failed: {exc}"
                        )

            with action3:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_device_{device_id}",
                    use_container_width=True
                ):

                    try:

                        response = requests.delete(
                            f"{API_URL}/devices/{device_id}",
                            timeout=5
                        )

                        if response.status_code == 200:

                            st.success(
                                "Device deleted successfully."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Could not delete device."
                            )

                    except requests.RequestException as exc:

                        st.error(
                            f"Backend connection failed: {exc}"
                        )

            # ----------------------------------------------------
            # EDIT / UPDATE DEVICE
            # ----------------------------------------------------

            if st.session_state.get(
                "edit_device_id"
            ) == device_id:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### ✏️ Edit {device_name}"
                    )

                    edit_col1, edit_col2 = st.columns(2)

                    with edit_col1:

                        edit_name = st.text_input(
                            "Device Name",
                            value=device_name,
                            key=f"edit_device_name_{device_id}"
                        )

                        edit_type = st.selectbox(
                            "Device Type",
                            [
                                "AC",
                                "Light",
                                "Fan",
                                "TV",
                                "Speaker",
                                "Camera",
                                "Appliance",
                                "Other",
                            ],
                            index=(
                                [
                                    "AC",
                                    "Light",
                                    "Fan",
                                    "TV",
                                    "Speaker",
                                    "Camera",
                                    "Appliance",
                                    "Other",
                                ].index(device_type)
                                if device_type in [
                                    "AC",
                                    "Light",
                                    "Fan",
                                    "TV",
                                    "Speaker",
                                    "Camera",
                                    "Appliance",
                                    "Other",
                                ]
                                else 7
                            ),
                            key=f"edit_device_type_{device_id}"
                        )

                    with edit_col2:

                        edit_room = st.text_input(
                            "Room",
                            value=room_name,
                            key=f"edit_device_room_{device_id}"
                        )

                        edit_power = st.number_input(
                            "Power Consumption (W)",
                            min_value=0.0,
                            value=device_power,
                            step=1.0,
                            key=f"edit_device_power_{device_id}"
                        )

                        edit_status = st.checkbox(
                            "Active",
                            value=is_active,
                            key=f"edit_device_status_{device_id}"
                        )

                    update_col, cancel_col = st.columns(2)

                    with update_col:

                        if st.button(
                            "💾 Update Device",
                            key=f"update_device_{device_id}",
                            type="primary",
                            use_container_width=True
                        ):

                            if not edit_name.strip():

                                st.warning(
                                    "Please enter a device name."
                                )

                            elif not edit_room.strip():

                                st.warning(
                                    "Please enter a room."
                                )

                            else:

                                try:

                                    response = requests.put(
                                        f"{API_URL}/devices/{device_id}",
                                        params={
                                            "name": edit_name.strip(),
                                            "device_type": edit_type,
                                            "room": edit_room.strip(),
                                            "status": edit_status,
                                            "power_watts": edit_power,
                                        },
                                        timeout=5
                                    )

                                    if response.status_code == 200:

                                        st.session_state[
                                            "edit_device_id"
                                        ] = None

                                        st.success(
                                            "Device updated successfully."
                                        )

                                        st.rerun()

                                    else:

                                        st.error(
                                            f"Could not update device. "
                                            f"HTTP {response.status_code}"
                                        )

                                except requests.RequestException as exc:

                                    st.error(
                                        f"Backend connection failed: {exc}"
                                    )

                    with cancel_col:

                        if st.button(
                            "Cancel",
                            key=f"cancel_device_edit_{device_id}",
                            use_container_width=True
                        ):

                            st.session_state[
                                "edit_device_id"
                            ] = None

                            st.rerun()

    # ============================================================
    # DATABASE INFORMATION
    # ============================================================

    render_html(
        f"""
        <div style="
            color:#607995;
            font-size:9px;
            margin-top:15px;
            padding-bottom:5px;
        ">
            Live PostgreSQL data:
            {total_devices} devices
            · {len(sensor_readings):,} sensor readings
        </div>
        """
    )

    st.stop()
    
elif current_page == "Reports":

    # ============================================================
    # REPORTS & ANALYTICS
    # ============================================================

    # ------------------------------------------------------------
    # LOAD DATABASE DATA
    # ------------------------------------------------------------

    reports_sensor_api = api_get(
        "/sensor-readings"
    )

    reports_ml_api = api_get(
        "/ml-results"
    )

    reports_sensor = normalize_records(
        reports_sensor_api
    )

    reports_ml = normalize_records(
        reports_ml_api
    )

    reports_devices = devices.copy()

    # ------------------------------------------------------------
    # HEADER
    # ------------------------------------------------------------

    render_html(
        """
        <div class="page-header">

            <div class="page-title">
                Reports
            </div>

            <div class="page-subtitle">
                Advanced energy, device and AI performance analytics
                powered by your smart-home database.
            </div>

        </div>
        """
    )

    # ------------------------------------------------------------
    # REPORT CONTROLS
    # ------------------------------------------------------------

    control1, control2, control3 = st.columns(
        [1.2, 1.4, 1]
    )

    with control1:

        report_period = st.selectbox(
            "Report Period",
            [
                "All Available Data",
                "Last 24 Hours",
                "Last 7 Days",
                "Last 30 Days",
            ],
            key="reports_period"
        )

    with control2:

        report_device_options = [
            "All Devices"
        ]

        report_device_options += [
            str(
                device.get(
                    "name",
                    "Unknown Device"
                )
            )
            for device in reports_devices
        ]

        report_device = st.selectbox(
            "Device",
            report_device_options,
            key="reports_device"
        )

    with control3:

        if st.button(
            "↻ Refresh",
            key="reports_refresh",
            use_container_width=True
        ):

            st.rerun()

    # ============================================================
    # BUILD SENSOR DATAFRAME
    # ============================================================

    sensor_rows = []

    device_lookup = {
        str(
            device.get("id")
        ): device
        for device in reports_devices
    }

    for reading in reports_sensor:

        device_id = str(
            reading.get(
                "device_id",
                ""
            )
        )

        device = device_lookup.get(
            device_id,
            {}
        )

        device_name = device.get(
            "name",
            "Unknown Device"
        )

        timestamp = reading.get(
            "recorded_at"
        )

        power = number_value(
            reading.get(
                "power_watts",
                0
            )
        )

        temperature = number_value(
            reading.get(
                "temperature",
                0
            )
        )

        humidity = number_value(
            reading.get(
                "humidity",
                0
            )
        )

        sensor_rows.append(
            {
                "Time": timestamp,
                "Device": str(device_name),
                "Power": power,
                "Temperature": temperature,
                "Humidity": humidity,
            }
        )

    sensor_df = pd.DataFrame(
        sensor_rows
    )

    if not sensor_df.empty:

        sensor_df["Time"] = pd.to_datetime(
            sensor_df["Time"],
            errors="coerce"
        )

        sensor_df["Power"] = pd.to_numeric(
            sensor_df["Power"],
            errors="coerce"
        ).fillna(0)

        sensor_df = sensor_df.dropna(
            subset=["Time"]
        )

        sensor_df = sensor_df.sort_values(
            "Time"
        ).reset_index(
            drop=True
        )

    # ============================================================
    # BUILD ML DATAFRAME
    # ============================================================

    ml_rows = []

    for row in reports_ml:

        timestamp = (
            row.get("recorded_at")
            or row.get("created_at")
            or row.get("timestamp")
        )

        actual = row.get(
            "actual_power_watts"
        )

        if actual is None:

            actual = row.get(
                "power_watts",
                0
            )

        predicted = row.get(
            "predicted_power_watts"
        )

        if predicted is None:

            predicted = row.get(
                "predicted_power",
                actual
            )

        anomaly_value = str(
            row.get(
                "anomaly_status",
                ""
            )
        ).lower()

        is_anomaly = anomaly_value in [
            "anomaly",
            "true",
            "1",
            "yes"
        ]

        ml_rows.append(
            {
                "Time": timestamp,
                "Actual": number_value(
                    actual
                ),
                "Predicted": number_value(
                    predicted
                ),
                "Anomaly": is_anomaly,
            }
        )

    ml_df = pd.DataFrame(
        ml_rows
    )

    if not ml_df.empty:

        ml_df["Time"] = pd.to_datetime(
            ml_df["Time"],
            errors="coerce"
        )

        ml_df["Actual"] = pd.to_numeric(
            ml_df["Actual"],
            errors="coerce"
        ).fillna(0)

        ml_df["Predicted"] = pd.to_numeric(
            ml_df["Predicted"],
            errors="coerce"
        ).fillna(0)

        ml_df = ml_df.dropna(
            subset=["Time"]
        )

        ml_df = ml_df.sort_values(
            "Time"
        ).reset_index(
            drop=True
        )

    # ============================================================
    # APPLY DEVICE FILTER
    # ============================================================

    if (
        not sensor_df.empty
        and report_device != "All Devices"
    ):

        sensor_df = sensor_df[
            sensor_df["Device"]
            == report_device
        ].copy()

    # ============================================================
    # APPLY DATE FILTER
    # ============================================================

    def apply_report_period(
        frame,
        time_column="Time"
    ):

        if frame.empty:

            return frame

        if frame[time_column].isna().all():

            return frame

        latest_time = frame[
            time_column
        ].max()

        if report_period == "Last 24 Hours":

            start_time = (
                latest_time
                - pd.Timedelta(hours=24)
            )

        elif report_period == "Last 7 Days":

            start_time = (
                latest_time
                - pd.Timedelta(days=7)
            )

        elif report_period == "Last 30 Days":

            start_time = (
                latest_time
                - pd.Timedelta(days=30)
            )

        else:

            return frame

        filtered_frame = frame[
            frame[time_column]
            >= start_time
        ].copy()

        if filtered_frame.empty:

            return frame

        return filtered_frame.reset_index(
            drop=True
        )

    sensor_df = apply_report_period(
        sensor_df
    )

    ml_df = apply_report_period(
        ml_df
    )

    # ============================================================
    # ENERGY CALCULATION
    # ============================================================

    def report_energy_kwh(
        frame,
        value_column="Power"
    ):

        if frame.empty:

            return 0.0

        temp = frame[
            ["Time", value_column]
        ].copy()

        temp[value_column] = pd.to_numeric(
            temp[value_column],
            errors="coerce"
        ).fillna(0)

        temp = temp.dropna(
            subset=["Time"]
        ).sort_values(
            "Time"
        )

        if temp.empty:

            return 0.0

        if len(temp) == 1:

            return float(
                temp[value_column].iloc[0]
                / 1000.0
            )

        gaps = (
            temp["Time"]
            .diff()
            .dt.total_seconds()
            .div(3600)
        )

        valid_gaps = gaps[
            (gaps > 0)
            & (gaps <= 6)
        ]

        if not valid_gaps.empty:

            default_hours = float(
                valid_gaps.median()
            )

        else:

            default_hours = 1.0

        gaps = gaps.fillna(
            default_hours
        ).clip(
            lower=0,
            upper=6
        )

        return float(
            (
                temp[value_column]
                * gaps
                / 1000.0
            ).sum()
        )

    # ============================================================
    # REPORT METRICS
    # ============================================================

    total_energy = report_energy_kwh(
        sensor_df,
        "Power"
    )

    average_power = (
        float(
            sensor_df["Power"].mean()
        )
        if not sensor_df.empty
        else 0.0
    )

    peak_power = (
        float(
            sensor_df["Power"].max()
        )
        if not sensor_df.empty
        else 0.0
    )

    estimated_cost = (
        total_energy * 8.0
    )

    carbon_footprint = (
        total_energy * 0.82
    )

    anomaly_count = 0

    if not ml_df.empty:

        anomaly_count = int(
            ml_df["Anomaly"].sum()
        )

    prediction_gap = 0.0

    if not ml_df.empty:

        prediction_gap = float(
            (
                ml_df["Actual"]
                - ml_df["Predicted"]
            )
            .abs()
            .mean()
        )

    # ============================================================
    # KPI CARDS
    # ============================================================

    k1, k2, k3, k4 = st.columns(
        4,
        gap="small"
    )

    report_cards = [
        (
            k1,
            "TOTAL ENERGY",
            f"{total_energy:.2f} kWh",
            "Measured sensor consumption"
        ),
        (
            k2,
            "ESTIMATED COST",
            f"₹{estimated_cost:,.2f}",
            "Using ₹8 / kWh estimate"
        ),
        (
            k3,
            "PEAK POWER",
            f"{peak_power:.0f} W",
            "Highest recorded reading"
        ),
        (
            k4,
            "CARBON FOOTPRINT",
            f"{carbon_footprint:.2f} kg",
            "Using 0.82 kg CO₂ / kWh"
        ),
    ]

    for column, title, value, subtitle in report_cards:

        with column:

            render_html(
                f"""
                <div style="
                    background:#081323;
                    border:1px solid #183452;
                    border-radius:14px;
                    padding:15px;
                    min-height:105px;
                ">

                    <div style="
                        color:#6f8fb7;
                        font-size:9px;
                        font-weight:800;
                        letter-spacing:.6px;
                    ">
                        {escape(title)}
                    </div>

                    <div style="
                        color:#ffffff;
                        font-size:22px;
                        font-weight:800;
                        margin-top:8px;
                    ">
                        {escape(value)}
                    </div>

                    <div style="
                        color:#607995;
                        font-size:9px;
                        margin-top:4px;
                    ">
                        {escape(subtitle)}
                    </div>

                </div>
                """
            )

    # ============================================================
    # DATA STATUS
    # ============================================================

    render_html(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            background:#07111f;
            border:1px solid #183452;
            border-radius:11px;
            padding:10px 13px;
            margin-top:14px;
        ">

            <div style="
                color:#7fa4d2;
                font-size:9px;
            ">
                DATABASE REPORT
            </div>

            <div style="
                color:#31d68e;
                font-size:9px;
                font-weight:800;
            ">
                ● LIVE DATA
            </div>

        </div>
        """
    )

    # ============================================================
    # ENERGY CONSUMPTION TREND
    # ============================================================

    render_html(
        """
        <div style="
            color:#ffffff;
            font-size:15px;
            font-weight:800;
            margin-top:20px;
            margin-bottom:8px;
        ">
            Energy Consumption Trend
        </div>
        """
    )

    if not sensor_df.empty:

        trend_df = sensor_df.copy()

        trend_df["Energy"] = (
            trend_df["Power"]
            / 1000.0
        )

        trend_fig = go.Figure()

        trend_fig.add_trace(
            go.Scatter(
                x=trend_df["Time"],
                y=trend_df["Energy"],
                mode="lines+markers",
                name="Energy",
                line={
                    "width": 1
                },
                marker={
                    "size": 1
                },
                hovertemplate=(
                    "%{x}<br>"
                    "Energy: %{y:.3f} kWh"
                    "<extra></extra>"
                )
            )
        )

        trend_fig.update_layout(
            height=270,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#8ea5c1"
            ),
            xaxis=dict(
                showgrid=False
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#13263d",
                title="kWh"
            ),
            legend=dict(
                orientation="h",
                y=1.08
            )
        )

        st.plotly_chart(
            trend_fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            },
            key="reports_energy_trend"
        )

    else:

        st.info(
            "No sensor data is available for this report."
        )

    # ============================================================
    # DEVICE USAGE + AI SUMMARY
    # ============================================================

    left_col, right_col = st.columns(
        2,
        gap="medium"
    )

    # ------------------------------------------------------------
    # DEVICE USAGE
    # ------------------------------------------------------------

    with left_col:

        render_html(
            """
            <div style="
                color:#ffffff;
                font-size:15px;
                font-weight:800;
                margin-top:12px;
                margin-bottom:8px;
            ">
                Device Usage
            </div>
            """
        )

        if not sensor_df.empty:

            device_usage = (
                sensor_df
                .groupby("Device")["Power"]
                .mean()
                .sort_values(
                    ascending=False
                )
            )

            usage_fig = go.Figure()

            usage_fig.add_trace(
                go.Bar(
                    x=device_usage.index,
                    y=device_usage.values,
                    name="Average Power",
                    hovertemplate=(
                        "%{x}<br>"
                        "Average: %{y:.0f} W"
                        "<extra></extra>"
                    )
                )
            )

            usage_fig.update_layout(
                height=270,
                margin=dict(
                    l=10,
                    r=10,
                    t=15,
                    b=50
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="#8ea5c1"
                ),
                xaxis=dict(
                    showgrid=False
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#13263d",
                    title="Watts"
                ),
                showlegend=False
            )

            st.plotly_chart(
                usage_fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                },
                key="reports_device_usage"
            )

        else:

            st.info(
                "No device usage data available."
            )

    # ------------------------------------------------------------
    # AI SUMMARY
    # ------------------------------------------------------------

    with right_col:

        render_html(
            """
            <div style="
                color:#ffffff;
                font-size:15px;
                font-weight:800;
                margin-top:12px;
                margin-bottom:8px;
            ">
                AI Report Summary
            </div>
            """
        )

        if not ml_df.empty:

            ml_actual = float(
                ml_df["Actual"].mean()
            )

            ml_predicted = float(
                ml_df["Predicted"].mean()
            )

            if prediction_gap <= 100:

                prediction_status = (
                    "Prediction gap is relatively small."
                )

            else:

                prediction_status = (
                    "Prediction gap requires monitoring."
                )

            ai_status = (
                "Attention required"
                if anomaly_count > 0
                else "Normal"
            )

            render_html(
                f"""
                <div style="
                    background:#081323;
                    border:1px solid #183452;
                    border-radius:14px;
                    padding:18px;
                    min-height:225px;
                ">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                    ">

                        <div style="
                            color:#ffffff;
                            font-size:13px;
                            font-weight:800;
                        ">
                            🤖 ML Monitoring
                        </div>

                        <div style="
                            color:#f5b83d;
                            font-size:9px;
                            font-weight:800;
                        ">
                            {escape(ai_status)}
                        </div>

                    </div>

                    <div style="
                        display:grid;
                        grid-template-columns:
                            repeat(2, 1fr);
                        gap:10px;
                        margin-top:18px;
                    ">

                        <div style="
                            background:#0b1a2d;
                            border-radius:10px;
                            padding:11px;
                        ">

                            <div style="
                                color:#607995;
                                font-size:8px;
                            ">
                                AVG ACTUAL
                            </div>

                            <div style="
                                color:#ffffff;
                                font-size:17px;
                                font-weight:800;
                                margin-top:4px;
                            ">
                                {ml_actual:.0f} W
                            </div>

                        </div>

                        <div style="
                            background:#0b1a2d;
                            border-radius:10px;
                            padding:11px;
                        ">

                            <div style="
                                color:#607995;
                                font-size:8px;
                            ">
                                AVG PREDICTED
                            </div>

                            <div style="
                                color:#ffffff;
                                font-size:17px;
                                font-weight:800;
                                margin-top:4px;
                            ">
                                {ml_predicted:.0f} W
                            </div>

                        </div>

                        <div style="
                            background:#0b1a2d;
                            border-radius:10px;
                            padding:11px;
                        ">

                            <div style="
                                color:#607995;
                                font-size:8px;
                            ">
                                PREDICTION GAP
                            </div>

                            <div style="
                                color:#ffffff;
                                font-size:17px;
                                font-weight:800;
                                margin-top:4px;
                            ">
                                {prediction_gap:.0f} W
                            </div>

                        </div>

                        <div style="
                            background:#0b1a2d;
                            border-radius:10px;
                            padding:11px;
                        ">

                            <div style="
                                color:#607995;
                                font-size:8px;
                            ">
                                ANOMALIES
                            </div>

                            <div style="
                                color:#ffffff;
                                font-size:17px;
                                font-weight:800;
                                margin-top:4px;
                            ">
                                {anomaly_count}
                            </div>

                        </div>

                    </div>

                    <div style="
                        color:#6f8fb7;
                        font-size:9px;
                        margin-top:14px;
                    ">
                        {escape(prediction_status)}
                    </div>

                </div>
                """
            )

        else:

            st.info(
                "No ML results are available."
            )

    # ============================================================
    # ACTUAL VS PREDICTED
    # ============================================================

    render_html(
        """
        <div style="
            color:#ffffff;
            font-size:15px;
            font-weight:800;
            margin-top:20px;
            margin-bottom:8px;
        ">
            AI Prediction Analysis
        </div>
        """
    )

    if not ml_df.empty:

        prediction_fig = go.Figure()

        prediction_fig.add_trace(
            go.Scatter(
                x=ml_df["Time"],
                y=ml_df["Actual"],
                mode="lines",
                name="Actual",
                line={
                    "width": 2
                }
            )
        )

        prediction_fig.add_trace(
            go.Scatter(
                x=ml_df["Time"],
                y=ml_df["Predicted"],
                mode="lines",
                name="Predicted",
                line={
                    "width": 1.5,
                    "dash": "dash"
                }
            )
        )

        prediction_fig.update_layout(
            height=280,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#8ea5c1"
            ),
            xaxis=dict(
                showgrid=False
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#13263d",
                title="Power (W)"
            ),
            legend=dict(
                orientation="h",
                y=1.08
            )
        )

        st.plotly_chart(
            prediction_fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            },
            key="reports_prediction_chart"
        )

    else:

        st.info(
            "No ML prediction data is available."
        )

    # ============================================================
    # ANOMALY ANALYSIS
    # ============================================================

    anomaly_col1, anomaly_col2 = st.columns(
        2,
        gap="medium"
    )

    with anomaly_col1:

        render_html(
            f"""
            <div style="
                background:#081323;
                border:1px solid #183452;
                border-radius:14px;
                padding:18px;
                margin-top:12px;
            ">

                <div style="
                    color:#ffffff;
                    font-size:14px;
                    font-weight:800;
                ">
                    ⚠️ AI Anomaly Detection
                </div>

                <div style="
                    color:#607995;
                    font-size:9px;
                    margin-top:5px;
                ">
                    Unusual patterns detected by the ML model.
                </div>

                <div style="
                    color:#ffffff;
                    font-size:30px;
                    font-weight:800;
                    margin-top:18px;
                ">
                    {anomaly_count}
                </div>

                <div style="
                    color:#6f8fb7;
                    font-size:9px;
                ">
                    detected anomaly records
                </div>

            </div>
            """
        )

    with anomaly_col2:

        normal_count = max(
            0,
            len(ml_df) - anomaly_count
        )

        anomaly_rate = (
            (
                anomaly_count
                / len(ml_df)
            )
            * 100
            if len(ml_df) > 0
            else 0
        )

        render_html(
            f"""
            <div style="
                background:#081323;
                border:1px solid #183452;
                border-radius:14px;
                padding:18px;
                margin-top:12px;
            ">

                <div style="
                    color:#ffffff;
                    font-size:14px;
                    font-weight:800;
                ">
                    AI Health Overview
                </div>

                <div style="
                    display:grid;
                    grid-template-columns:
                        repeat(2, 1fr);
                    gap:10px;
                    margin-top:15px;
                ">

                    <div style="
                        background:#0b1a2d;
                        border-radius:10px;
                        padding:11px;
                    ">

                        <div style="
                            color:#607995;
                            font-size:8px;
                        ">
                            NORMAL
                        </div>

                        <div style="
                            color:#ffffff;
                            font-size:18px;
                            font-weight:800;
                            margin-top:4px;
                        ">
                            {normal_count}
                        </div>

                    </div>

                    <div style="
                        background:#0b1a2d;
                        border-radius:10px;
                        padding:11px;
                    ">

                        <div style="
                            color:#607995;
                            font-size:8px;
                        ">
                            ANOMALY RATE
                        </div>

                        <div style="
                            color:#ffffff;
                            font-size:18px;
                            font-weight:800;
                            margin-top:4px;
                        ">
                            {anomaly_rate:.1f}%
                        </div>

                    </div>

                </div>

            </div>
            """
        )

    # ============================================================
    # DAILY USAGE
    # ============================================================

    render_html(
        """
        <div style="
            color:#ffffff;
            font-size:15px;
            font-weight:800;
            margin-top:20px;
            margin-bottom:8px;
        ">
            Daily Power Pattern
        </div>
        """
    )

    if not sensor_df.empty:

        daily_df = (
            sensor_df
            .set_index("Time")
            .resample("D")["Power"]
            .mean()
            .reset_index()
        )

        daily_fig = go.Figure()

        daily_fig.add_trace(
            go.Bar(
                x=daily_df["Time"],
                y=daily_df["Power"],
                name="Average Power",
                hovertemplate=(
                    "%{x}<br>"
                    "Average: %{y:.0f} W"
                    "<extra></extra>"
                )
            )
        )

        daily_fig.update_layout(
            height=250,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#8ea5c1"
            ),
            xaxis=dict(
                showgrid=False
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#13263d",
                title="Watts"
            ),
            showlegend=False
        )

        st.plotly_chart(
            daily_fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            },
            key="reports_daily_usage"
        )

    else:

        st.info(
            "No daily usage data available."
        )

    # ============================================================
    # REPORT DETAILS
    # ============================================================

    render_html(
        """
        <div style="
            color:#ffffff;
            font-size:15px;
            font-weight:800;
            margin-top:20px;
            margin-bottom:8px;
        ">
            Report Details
        </div>
        """
    )

    detail1, detail2, detail3, detail4 = st.columns(
        4
    )

    with detail1:

        st.metric(
            "Sensor Records",
            f"{len(sensor_df):,}"
        )

    with detail2:

        st.metric(
            "ML Records",
            f"{len(ml_df):,}"
        )

    with detail3:

        st.metric(
            "Average Power",
            f"{average_power:.0f} W"
        )

    with detail4:

        st.metric(
            "Devices",
            f"{len(reports_devices):,}"
        )

    # ============================================================
    # CSV EXPORT
    # ============================================================

    export_df = sensor_df.copy()

    if not export_df.empty:

        export_df["Time"] = (
            export_df["Time"]
            .dt.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

    if not export_df.empty:

        csv_data = export_df.to_csv(
            index=False
        )

        st.download_button(
            "📥 Download Device Report CSV",
            data=csv_data,
            file_name="ai_home_device_report.csv",
            mime="text/csv",
            key="reports_download_csv"
        )

    # ============================================================
    # REPORT FOOTER
    # ============================================================

    render_html(
        f"""
        <div style="
            color:#607995;
            font-size:9px;
            margin-top:14px;
            padding-bottom:10px;
        ">
            Report generated from PostgreSQL-backed sensor data,
            device records and saved ML prediction results.
            · {len(sensor_df):,} sensor records
            · {len(ml_df):,} ML records
        </div>
        """
    )

    st.stop()    
    

elif current_page == "Account":

    # ============================================================
    # ACCOUNT PAGE
    # ============================================================

    if "edit_user_id" not in st.session_state:
        st.session_state.edit_user_id = None

    users = normalize_records(users_api)

    # ============================================================
    # ACCOUNT UI STYLES
    # ============================================================

    render_html(
        """
        <style>

        .account-page {
            width: 100%;
        }

        .account-hero {
            background:
                radial-gradient(circle at 85% 20%, rgba(30,120,255,.18), transparent 35%),
                linear-gradient(135deg, #0d2342 0%, #081526 55%, #07101d 100%);
            border: 1px solid #174c87;
            border-radius: 20px;
            padding: 26px;
            margin-top: 26px;
            margin-bottom: 22px;
            box-shadow: 0 18px 45px rgba(0,0,0,.20);
        }

        .account-hero-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }

        .account-profile-left {
            display: flex;
            align-items: center;
            gap: 18px;
        }

        .account-avatar-large {
            width: 68px;
            height: 68px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            background: linear-gradient(135deg, #1677ff, #4f46e5);
            border: 1px solid #4b9cff;
            box-shadow: 0 0 28px rgba(30,120,255,.22);
        }

        .account-name-large {
            color: #ffffff;
            font-size: 22px;
            font-weight: 800;
            margin-bottom: 5px;
        }

        .account-email-small {
            color: #7f9fc8;
            font-size: 12px;
        }

        .account-status-pill {
            color: #55e0aa;
            background: rgba(40,210,150,.08);
            border: 1px solid rgba(70,220,170,.25);
            border-radius: 999px;
            padding: 7px 12px;
            font-size: 11px;
            font-weight: 800;
        }

        .account-stat-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-top: 20px;
        }

        .account-stat {
            background: rgba(5,15,28,.55);
            border: 1px solid #173a61;
            border-radius: 13px;
            padding: 14px;
        }

        .account-stat-label {
            color: #6688b2;
            font-size: 10px;
            margin-bottom: 5px;
        }

        .account-stat-value {
            color: #ffffff;
            font-size: 18px;
            font-weight: 800;
        }

        .account-card {
            background: #081323;
            border: 1px solid #183452;
            border-radius: 16px;
            padding: 20px;
            min-height: 190px;
            box-sizing: border-box;
            box-shadow: 0 10px 28px rgba(0,0,0,.10);
        }

        .account-card-wide {
            background: #081323;
            border: 1px solid #183452;
            border-radius: 16px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 10px 28px rgba(0,0,0,.10);
        }

        .account-card-title {
            color: #ffffff;
            font-size: 15px;
            font-weight: 800;
            margin-bottom: 5px;
        }

        .account-card-subtitle {
            color: #6688b2;
            font-size: 11px;
            margin-bottom: 16px;
        }

        .account-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #12273f;
        }

        .account-row:last-child {
            border-bottom: none;
        }

        .account-label {
            color: #7695b9;
            font-size: 12px;
        }

        .account-value {
            color: #e8f2ff;
            font-size: 12px;
            font-weight: 700;
            text-align: right;
        }

        .account-active {
            color: #45dfaa;
            font-size: 11px;
            font-weight: 800;
        }

        .account-users-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 15px;
        }

        .account-user-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .account-user-avatar {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            background: #10284a;
            border: 1px solid #1c4775;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 21px;
        }

        .account-user-name {
            color: #ffffff;
            font-size: 13px;
            font-weight: 800;
        }

        .account-user-role {
            color: #6688b2;
            font-size: 10px;
            margin-top: 3px;
        }

        .account-user-active {
            color: #39e6aa;
            font-size: 10px;
            font-weight: 800;
        }

        .account-user-inactive {
            color: #ffb638;
            font-size: 10px;
            font-weight: 800;
        }

        .account-security-item {
            background: #0a192d;
            border: 1px solid #173756;
            border-radius: 12px;
            padding: 13px;
            margin-bottom: 10px;
        }

        .account-security-title {
            color: #dcecff;
            font-size: 12px;
            font-weight: 700;
        }

        .account-security-text {
            color: #6787ad;
            font-size: 10px;
            margin-top: 4px;
        }

        </style>

        <div class="account-page">

            <div class="page-header">
                <div class="page-title">Account</div>
                <div class="page-subtitle">
                    Manage your profile, home users, preferences and security.
                </div>
            </div>

        </div>
        """
    )

    # ============================================================
    # ACCOUNT PROFILE
    # ============================================================

    active_users = [
        user for user in users
        if bool(user.get("status", False))
    ]

    admin_users = [
        user for user in users
        if str(user.get("role", "")).lower() == "admin"
    ]

    profile_user = admin_users[0] if admin_users else (
        users[0] if users else {}
    )

    profile_name = str(
        profile_user.get("name", "AI Home User")
    )

    profile_avatar = str(
        profile_user.get("avatar", "👤")
    )

    connected_device_count = len(devices)

    render_html(
        f"""
        <div class="account-hero">

            <div class="account-hero-top">

                <div class="account-profile-left">

                    <div class="account-avatar-large">
                        {escape(profile_avatar)}
                    </div>

                    <div>
                        <div class="account-name-large">
                            {escape(profile_name)}
                        </div>

                        <div class="account-email-small">
                            AI Home Intelligence account
                        </div>
                    </div>

                </div>

                <div class="account-status-pill">
                    ● ACTIVE ACCOUNT
                </div>

            </div>

            <div class="account-stat-grid">

                <div class="account-stat">
                    <div class="account-stat-label">
                        HOME USERS
                    </div>
                    <div class="account-stat-value">
                        {len(users)}
                    </div>
                </div>

                <div class="account-stat">
                    <div class="account-stat-label">
                        ACTIVE USERS
                    </div>
                    <div class="account-stat-value">
                        {len(active_users)}
                    </div>
                </div>

                <div class="account-stat">
                    <div class="account-stat-label">
                        CONNECTED DEVICES
                    </div>
                    <div class="account-stat-value">
                        {connected_device_count}
                    </div>
                </div>

            </div>

        </div>
        """
    )

    # ============================================================
    # HOME INFORMATION + PREFERENCES
    # ============================================================

    account_col1, account_col2 = st.columns(2, gap="large")

    with account_col1:

        render_html(
            f"""
            <div class="account-card">

                <div class="account-card-title">
                    🏠 Home Information
                </div>

                <div class="account-card-subtitle">
                    Connected smart home overview
                </div>

                <div class="account-row">
                    <div class="account-label">Home Name</div>
                    <div class="account-value">My Smart Home</div>
                </div>

                <div class="account-row">
                    <div class="account-label">Connected Devices</div>
                    <div class="account-value">
                        {connected_device_count}
                    </div>
                </div>

                <div class="account-row">
                    <div class="account-label">AI Monitoring</div>
                    <div class="account-active">ACTIVE</div>
                </div>

            </div>
            """
        )

    with account_col2:

        render_html(
            """
            <div class="account-card">

                <div class="account-card-title">
                    ⚙️ Preferences
                </div>

                <div class="account-card-subtitle">
                    Dashboard display preferences
                </div>

                <div class="account-row">
                    <div class="account-label">Temperature Unit</div>
                    <div class="account-value">°C</div>
                </div>

                <div class="account-row">
                    <div class="account-label">Energy Unit</div>
                    <div class="account-value">kWh</div>
                </div>

                <div class="account-row">
                    <div class="account-label">Notifications</div>
                    <div class="account-active">ON</div>
                </div>

            </div>
            """
        )

    # ============================================================
    # HOME USERS
    # ============================================================

    render_html(
        """
        <div class="account-card-wide">

            <div class="account-users-header">

                <div>
                    <div class="account-card-title">
                        👥 Home Users
                    </div>

                    <div class="account-card-subtitle">
                        Manage people who have access to your smart home.
                    </div>
                </div>

            </div>

        </div>
        """
    )

    # ============================================================
    # USER SEARCH + FILTER
    # ============================================================

    user_filter_col1, user_filter_col2 = st.columns([2.5, 1])

    with user_filter_col1:

        user_search = st.text_input(
            "Search users",
            placeholder="Search by name or role...",
            key="account_user_search",
        )

    with user_filter_col2:

        user_status_filter = st.selectbox(
            "Status",
            ["All", "Active", "Inactive"],
            key="account_user_status_filter",
        )

    filtered_users = []

    for user in users:

        name = str(
            user.get("name", "")
        )

        role = str(
            user.get("role", "")
        )

        is_active = bool(
            user.get("status", False)
        )

        matches_search = (
            not user_search.strip()
            or user_search.lower().strip() in name.lower()
            or user_search.lower().strip() in role.lower()
        )

        matches_status = (
            user_status_filter == "All"
            or (
                user_status_filter == "Active"
                and is_active
            )
            or (
                user_status_filter == "Inactive"
                and not is_active
            )
        )

        if matches_search and matches_status:
            filtered_users.append(user)

    # ============================================================
    # ADD USER
    # ============================================================

    with st.expander("➕ Add New Home User", expanded=False):

        add_col1, add_col2 = st.columns(2)

        with add_col1:

            new_user_name = st.text_input(
                "Name",
                key="new_user_name",
            )

            new_user_role = st.selectbox(
                "Role",
                ["Admin", "Member", "Guest"],
                key="new_user_role",
            )

        with add_col2:

            new_user_avatar = st.text_input(
                "Avatar",
                value="👤",
                key="new_user_avatar",
            )

            new_user_status = st.checkbox(
                "Active",
                value=True,
                key="new_user_status",
            )

        if st.button(
            "Add User",
            key="add_user_button",
            type="primary",
            use_container_width=True,
        ):

            if not new_user_name.strip():

                st.warning(
                    "Please enter a user name."
                )

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/users",
                        params={
                            "name": new_user_name.strip(),
                            "role": new_user_role,
                            "avatar": new_user_avatar or "👤",
                            "status": new_user_status,
                        },
                        timeout=5,
                    )

                    if response.status_code == 200:

                        st.success(
                            "User added successfully."
                        )

                        st.rerun()

                    else:

                        st.error(
                            f"Could not add user. HTTP {response.status_code}"
                        )

                except requests.RequestException as exc:

                    st.error(
                        f"Backend connection failed: {exc}"
                    )

    # ============================================================
    # USER LIST
    # ============================================================

    if not filtered_users:

        st.info(
            "No users match the current search or filter."
        )

    for user in filtered_users:

        user_id = user.get("id")

        user_name = str(
            user.get("name", "Unknown User")
        )

        user_role = str(
            user.get("role", "Member")
        )

        user_avatar = str(
            user.get("avatar", "👤")
        )

        user_is_active = bool(
            user.get("status", False)
        )

        status_label = (
            "ACTIVE"
            if user_is_active
            else "INACTIVE"
        )

        status_class = (
            "account-user-active"
            if user_is_active
            else "account-user-inactive"
        )

        with st.container(border=True):

            row_col1, row_col2, row_col3 = st.columns(
                [5, 1.2, 3.3],
                gap="small",
            )

            with row_col1:

                render_html(
                    f"""
                    <div class="account-user-left">

                        <div class="account-user-avatar">
                            {escape(user_avatar)}
                        </div>

                        <div>
                            <div class="account-user-name">
                                {escape(user_name)}
                            </div>

                            <div class="account-user-role">
                                {escape(user_role)}
                            </div>
                        </div>

                    </div>
                    """
                )

            with row_col2:

                render_html(
                    f'<div class="{status_class}">{status_label}</div>'
                )

            with row_col3:

                action1, action2, action3 = st.columns(
                    3,
                    gap="small",
                )

                with action1:

                    if st.button(
                        "✏️ Edit",
                        key=f"edit_user_{user_id}",
                        use_container_width=True,
                    ):

                        st.session_state.edit_user_id = user_id

                        st.rerun()

                with action2:

                    if st.button(
                        "⏻ On" if not user_is_active else "⏻ Off",
                        key=f"toggle_user_{user_id}",
                        use_container_width=True,
                    ):

                        try:

                            response = requests.put(
                                f"{API_URL}/users/{user_id}",
                                params={
                                    "name": user_name,
                                    "role": user_role,
                                    "avatar": user_avatar,
                                    "status": not user_is_active,
                                },
                                timeout=5,
                            )

                            if response.status_code == 200:

                                st.rerun()

                            else:

                                st.error(
                                    "Could not change user status."
                                )

                        except requests.RequestException as exc:

                            st.error(
                                f"Backend connection failed: {exc}"
                            )

                with action3:

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_user_{user_id}",
                        use_container_width=True,
                    ):

                        try:

                            response = requests.delete(
                                f"{API_URL}/users/{user_id}",
                                timeout=5,
                            )

                            if response.status_code == 200:

                                st.session_state.edit_user_id = None

                                st.success(
                                    "User deleted successfully."
                                )

                                st.rerun()

                            else:

                                st.error(
                                    "Could not delete user."
                                )

                        except requests.RequestException as exc:

                            st.error(
                                f"Backend connection failed: {exc}"
                            )

            # ====================================================
            # EDIT USER
            # ====================================================

            if st.session_state.edit_user_id == user_id:

                with st.container(border=True):

                    st.markdown(
                        f"### ✏️ Edit {user_name}"
                    )

                    edit_col1, edit_col2 = st.columns(2)

                    with edit_col1:

                        edit_name = st.text_input(
                            "Name",
                            value=user_name,
                            key=f"edit_name_{user_id}",
                        )

                        roles = [
                            "Admin",
                            "Member",
                            "Guest",
                        ]

                        edit_role = st.selectbox(
                            "Role",
                            roles,
                            index=(
                                roles.index(user_role)
                                if user_role in roles
                                else 1
                            ),
                            key=f"edit_role_{user_id}",
                        )

                    with edit_col2:

                        edit_avatar = st.text_input(
                            "Avatar",
                            value=user_avatar,
                            key=f"edit_avatar_{user_id}",
                        )

                        edit_status = st.checkbox(
                            "Active",
                            value=user_is_active,
                            key=f"edit_status_{user_id}",
                        )

                    update_col, cancel_col = st.columns(2)

                    with update_col:

                        if st.button(
                            "Update User",
                            key=f"update_user_{user_id}",
                            type="primary",
                            use_container_width=True,
                        ):

                            if not edit_name.strip():

                                st.warning(
                                    "Please enter a user name."
                                )

                            else:

                                try:

                                    response = requests.put(
                                        f"{API_URL}/users/{user_id}",
                                        params={
                                            "name": edit_name.strip(),
                                            "role": edit_role,
                                            "avatar": edit_avatar or "👤",
                                            "status": edit_status,
                                        },
                                        timeout=5,
                                    )

                                    if response.status_code == 200:

                                        st.session_state.edit_user_id = None

                                        st.success(
                                            "User updated successfully."
                                        )

                                        st.rerun()

                                    else:

                                        st.error(
                                            f"Could not update user. HTTP {response.status_code}"
                                        )

                                except requests.RequestException as exc:

                                    st.error(
                                        f"Backend connection failed: {exc}"
                                    )

                    with cancel_col:

                        if st.button(
                            "Cancel",
                            key=f"cancel_edit_{user_id}",
                            use_container_width=True,
                        ):

                            st.session_state.edit_user_id = None

                            st.rerun()

    # ============================================================
    # SECURITY
    # ============================================================

    render_html(
        """
        <div class="account-card-wide">

            <div class="account-card-title">
                🔐 Security & Privacy
            </div>

            <div class="account-card-subtitle">
                Account security status and access information.
            </div>

            <div class="account-security-item">

                <div class="account-security-title">
                    🔑 Password Protection
                </div>

                <div class="account-security-text">
                    Your account is protected by password authentication.
                </div>

            </div>

            <div class="account-security-item">

                <div class="account-security-title">
                    🔔 Notifications
                </div>

                <div class="account-security-text">
                    Security and smart-home notifications are enabled.
                </div>

            </div>

            <div class="account-security-item">

                <div class="account-security-title">
                    🛡️ Account Status
                </div>

                <div class="account-security-text">
                    Account is currently active.
                </div>

            </div>

        </div>
        """
    )

    st.stop()

elif current_page == "AI Model Center":

    # ============================================================
    # AI MODEL CENTER
    # ============================================================

    # ------------------------------------------------------------
    # LOAD ML STATUS
    # ------------------------------------------------------------

    model_status_api = api_get(
        "/ml-status"
    )

    if not isinstance(
        model_status_api,
        dict
    ):
        model_status_api = {}

    energy_status = model_status_api.get(
        "energy_prediction",
        {}
    )

    anomaly_status = model_status_api.get(
        "anomaly_detection",
        {}
    )

    energy_loaded = bool(
        energy_status.get(
            "model_loaded",
            False
        )
    )

    anomaly_loaded = bool(
        anomaly_status.get(
            "model_loaded",
            False
        )
    )

    energy_algorithm = energy_status.get(
        "algorithm",
        "Linear Regression"
    )

    anomaly_algorithm = anomaly_status.get(
        "algorithm",
        "Isolation Forest"
    )

    # ------------------------------------------------------------
    # LOAD ML RESULTS
    # ------------------------------------------------------------

    model_results_api = api_get(
        "/ml-results"
    )

    model_results = normalize_records(
        model_results_api
    )

    model_df = pd.DataFrame(
        model_results
    )

    # ------------------------------------------------------------
    # PREPARE MODEL METRICS
    # ------------------------------------------------------------

    model_records = len(
        model_df
    )

    mae_value = 0.0
    rmse_value = 0.0
    r2_value = 0.0
    anomaly_count = 0

    if not model_df.empty:

        if (
            "actual_power_watts"
            in model_df.columns
            and
            "predicted_power_watts"
            in model_df.columns
        ):

            actual_values = pd.to_numeric(
                model_df[
                    "actual_power_watts"
                ],
                errors="coerce"
            )

            predicted_values = pd.to_numeric(
                model_df[
                    "predicted_power_watts"
                ],
                errors="coerce"
            )

            valid_mask = (
                actual_values.notna()
                &
                predicted_values.notna()
            )

            actual_values = (
                actual_values[
                    valid_mask
                ]
            )

            predicted_values = (
                predicted_values[
                    valid_mask
                ]
            )

            if len(
                actual_values
            ) > 0:

                differences = (
                    actual_values
                    - predicted_values
                )

                mae_value = float(
                    differences.abs().mean()
                )

                rmse_value = float(
                    (
                        differences
                        ** 2
                    ).mean()
                    ** 0.5
                )

                actual_mean = float(
                    actual_values.mean()
                )

                denominator = float(
                    (
                        (
                            actual_values
                            - actual_mean
                        )
                        ** 2
                    ).sum()
                )

                if denominator > 0:

                    r2_value = float(
                        1
                        -
                        (
                            (
                                differences
                                ** 2
                            ).sum()
                            / denominator
                        )
                    )

        if (
            "anomaly_status"
            in model_df.columns
        ):

            anomaly_values = (
                model_df[
                    "anomaly_status"
                ]
                .astype(str)
                .str.lower()
            )

            anomaly_count = int(
                anomaly_values.isin(
                    [
                        "anomaly",
                        "true",
                        "1",
                        "yes",
                    ]
                ).sum()
            )

    # ------------------------------------------------------------
    # MODEL STATUS
    # ------------------------------------------------------------

    loaded_models = sum(
        [
            energy_loaded,
            anomaly_loaded,
        ]
    )

    total_models = 2

    if loaded_models == total_models:

        overall_status = "ALL SYSTEMS ONLINE"

        overall_status_color = "#31d68e"

    elif loaded_models > 0:

        overall_status = "PARTIALLY ONLINE"

        overall_status_color = "#f5b83d"

    else:

        overall_status = "MODELS OFFLINE"

        overall_status_color = "#ff5c73"

    # ============================================================
    # PAGE HEADER
    # ============================================================

    render_html(
        f"""
        <div style="
            background:
                radial-gradient(
                    circle at 90% 10%,
                    rgba(45,120,255,.20),
                    transparent 35%
                ),
                linear-gradient(
                    135deg,
                    #0b1c34 0%,
                    #071221 55%,
                    #050c17 100%
                );
            border:1px solid #174879;
            border-radius:20px;
            padding:25px 26px;
            margin-top:20px;
            margin-bottom:20px;
        ">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:20px;
            ">

                <div>

                    <div style="
                        color:#ffffff;
                        font-size:27px;
                        font-weight:800;
                    ">
                        AI Model Center
                    </div>

                    <div style="
                        color:#7898bf;
                        font-size:11px;
                        margin-top:5px;
                    ">
                        Monitor trained models, prediction
                        performance and AI system health.
                    </div>

                </div>

                <div style="
                    background:#071a17;
                    border:1px solid
                        rgba(49,214,142,.35);
                    border-radius:30px;
                    padding:9px 15px;
                    color:{overall_status_color};
                    font-size:9px;
                    font-weight:800;
                    white-space:nowrap;
                ">
                    ● {escape(overall_status)}
                </div>

            </div>

        </div>
        """
    )

    # ============================================================
    # MODEL KPI CARDS
    # ============================================================

    m1, m2, m3, m4 = st.columns(
        4,
        gap="small"
    )

    model_kpis = [
        (
            m1,
            "MODELS LOADED",
            f"{loaded_models}/{total_models}",
            "AI models available"
        ),
        (
            m2,
            "ML RECORDS",
            f"{model_records:,}",
            "Backend prediction records"
        ),
        (
            m3,
            "MAE",
            f"{mae_value:.1f} W",
            "Mean absolute error"
        ),
        (
            m4,
            "ANOMALIES",
            f"{anomaly_count:,}",
            "Detected unusual patterns"
        ),
    ]

    for column, title, value, subtitle in model_kpis:

        with column:

            render_html(
                f"""
                <div style="
                    background:#081323;
                    border:1px solid #183452;
                    border-radius:14px;
                    padding:16px;
                    min-height:110px;
                ">

                    <div style="
                        color:#6f91ba;
                        font-size:9px;
                        font-weight:800;
                        letter-spacing:.7px;
                    ">
                        {escape(title)}
                    </div>

                    <div style="
                        color:#ffffff;
                        font-size:23px;
                        font-weight:800;
                        margin-top:9px;
                    ">
                        {escape(value)}
                    </div>

                    <div style="
                        color:#607995;
                        font-size:9px;
                        margin-top:4px;
                    ">
                        {escape(subtitle)}
                    </div>

                </div>
                """
            )

    # ============================================================
    # MODEL CARDS
    # ============================================================

    render_html(
        """
        <div style="
            color:#ffffff;
            font-size:16px;
            font-weight:800;
            margin-top:24px;
            margin-bottom:10px;
        ">
            Deployed AI Models
        </div>
        """
    )

    model_col1, model_col2 = st.columns(
        2,
        gap="medium"
    )

    # ------------------------------------------------------------
    # ENERGY MODEL
    # ------------------------------------------------------------

    with model_col1:

        energy_state = (
            "READY"
            if energy_loaded
            else "OFFLINE"
        )

        energy_color = (
            "#31d68e"
            if energy_loaded
            else "#ff5c73"
        )

        render_html(
            f"""
            <div style="
                background:#081323;
                border:1px solid #183452;
                border-radius:16px;
                padding:20px;
                min-height:225px;
            ">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                ">

                    <div style="
                        display:flex;
                        align-items:center;
                        gap:10px;
                    ">

                        <div style="
                            width:40px;
                            height:40px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            background:#0b2441;
                            border-radius:11px;
                            font-size:20px;
                        ">
                            ⚡
                        </div>

                        <div>

                            <div style="
                                color:#ffffff;
                                font-size:14px;
                                font-weight:800;
                            ">
                                Energy Prediction
                            </div>

                            <div style="
                                color:#607995;
                                font-size:9px;
                                margin-top:3px;
                            ">
                                Power consumption forecasting
                            </div>

                        </div>

                    </div>

                    <div style="
                        color:{energy_color};
                        font-size:9px;
                        font-weight:800;
                    ">
                        ● {energy_state}
                    </div>

                </div>

                <div style="
                    display:grid;
                    grid-template-columns:
                        repeat(2, 1fr);
                    gap:10px;
                    margin-top:20px;
                ">

                    <div style="
                        background:#0b1a2d;
                        border-radius:10px;
                        padding:12px;
                    ">

                        <div style="
                            color:#607995;
                            font-size:8px;
                        ">
                            ALGORITHM
                        </div>

                        <div style="
                            color:#ffffff;
                            font-size:12px;
                            font-weight:700;
                            margin-top:5px;
                        ">
                            {escape(
                                energy_algorithm
                            )}
                        </div>

                    </div>

                    <div style="
                        background:#0b1a2d;
                        border-radius:10px;
                        padding:12px;
                    ">

                        <div style="
                            color:#607995;
                            font-size:8px;
                        ">
                            RMSE
                        </div>

                        <div style="
                            color:#ffffff;
                            font-size:16px;
                            font-weight:800;
                            margin-top:5px;
                        ">
                            {rmse_value:.1f} W
                        </div>

                    </div>

                </div>

                <div style="
                    color:#6f8fb7;
                    font-size:9px;
                    line-height:1.6;
                    margin-top:15px;
                ">
                    Predicts home power consumption using
                    environmental and appliance-related
                    features.
                </div>

            </div>
            """
        )

    # ------------------------------------------------------------
    # ANOMALY MODEL
    # ------------------------------------------------------------

    with model_col2:

        anomaly_state = (
            "READY"
            if anomaly_loaded
            else "OFFLINE"
        )

        anomaly_color = (
            "#31d68e"
            if anomaly_loaded
            else "#ff5c73"
        )

        render_html(
            f"""
            <div style="
                background:#081323;
                border:1px solid #183452;
                border-radius:16px;
                padding:20px;
                min-height:225px;
            ">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                ">

                    <div style="
                        display:flex;
                        align-items:center;
                        gap:10px;
                    ">

                        <div style="
                            width:40px;
                            height:40px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            background:#0b2441;
                            border-radius:11px;
                            font-size:20px;
                        ">
                            🛡️
                        </div>

                        <div>

                            <div style="
                                color:#ffffff;
                                font-size:14px;
                                font-weight:800;
                            ">
                                Anomaly Detection
                            </div>

                            <div style="
                                color:#607995;
                                font-size:9px;
                                margin-top:3px;
                            ">
                                Unusual energy pattern detection
                            </div>

                        </div>

                    </div>

                    <div style="
                        color:{anomaly_color};
                        font-size:9px;
                        font-weight:800;
                    ">
                        ● {anomaly_state}
                    </div>

                </div>

                <div style="
                    display:grid;
                    grid-template-columns:
                        repeat(2, 1fr);
                    gap:10px;
                    margin-top:20px;
                ">

                    <div style="
                        background:#0b1a2d;
                        border-radius:10px;
                        padding:12px;
                    ">

                        <div style="
                            color:#607995;
                            font-size:8px;
                        ">
                            ALGORITHM
                        </div>

                        <div style="
                            color:#ffffff;
                            font-size:12px;
                            font-weight:700;
                            margin-top:5px;
                        ">
                            {escape(
                                anomaly_algorithm
                            )}
                        </div>

                    </div>

                    <div style="
                        background:#0b1a2d;
                        border-radius:10px;
                        padding:12px;
                    ">

                        <div style="
                            color:#607995;
                            font-size:8px;
                        ">
                            DETECTIONS
                        </div>

                        <div style="
                            color:#ffffff;
                            font-size:16px;
                            font-weight:800;
                            margin-top:5px;
                        ">
                            {anomaly_count}
                        </div>

                    </div>

                </div>

                <div style="
                    color:#6f8fb7;
                    font-size:9px;
                    line-height:1.6;
                    margin-top:15px;
                ">
                    Identifies unusual power behavior that
                    may require attention or investigation.
                </div>

            </div>
            """
        )

    # ============================================================
    # MODEL PERFORMANCE
    # ============================================================

    render_html(
        """
        <div style="
            color:#ffffff;
            font-size:16px;
            font-weight:800;
            margin-top:24px;
            margin-bottom:10px;
        ">
            Model Performance
        </div>
        """
    )

    performance_col1, performance_col2 = st.columns(
        2,
        gap="medium"
    )

    with performance_col1:

        render_html(
            f"""
            <div style="
                background:#081323;
                border:1px solid #183452;
                border-radius:16px;
                padding:19px;
            ">

                <div style="
                    color:#ffffff;
                    font-size:13px;
                    font-weight:800;
                ">
                    Energy Prediction Metrics
                </div>

                <div style="
                    display:grid;
                    grid-template-columns:
                        repeat(3, 1fr);
                    gap:10px;
                    margin-top:15px;
                ">

                    <div style="
                        background:#0b1a2d;
                        border-radius:10px;
                        padding:12px;
                    ">
                        <div style="
                            color:#607995;
                            font-size:8px;
                        ">
                            MAE
                        </div>
                        <div style="
                            color:#ffffff;
                            font-size:17px;
                            font-weight:800;
                            margin-top:4px;
                        ">
                            {mae_value:.1f}
                        </div>
                    </div>

                    <div style="
                        background:#0b1a2d;
                        border-radius:10px;
                        padding:12px;
                    ">
                        <div style="
                            color:#607995;
                            font-size:8px;
                        ">
                            RMSE
                        </div>
                        <div style="
                            color:#ffffff;
                            font-size:17px;
                            font-weight:800;
                            margin-top:4px;
                        ">
                            {rmse_value:.1f}
                        </div>
                    </div>

                    <div style="
                        background:#0b1a2d;
                        border-radius:10px;
                        padding:12px;
                    ">
                        <div style="
                            color:#607995;
                            font-size:8px;
                        ">
                            R²
                        </div>
                        <div style="
                            color:#ffffff;
                            font-size:17px;
                            font-weight:800;
                            margin-top:4px;
                        ">
                            {r2_value:.3f}
                        </div>
                    </div>

                </div>

                <div style="
                    color:#607995;
                    font-size:9px;
                    margin-top:12px;
                ">
                    Metrics calculated from saved ML prediction
                    records returned by the backend.
                </div>

            </div>
            """
        )

    with performance_col2:

        render_html(
            f"""
            <div style="
                background:#081323;
                border:1px solid #183452;
                border-radius:16px;
                padding:19px;
            ">

                <div style="
                    color:#ffffff;
                    font-size:13px;
                    font-weight:800;
                ">
                    AI System Health
                </div>

                <div style="
                    margin-top:15px;
                ">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        padding:10px 0;
                        border-bottom:
                            1px solid #11263d;
                    ">

                        <span style="
                            color:#7890ad;
                            font-size:9px;
                        ">
                            Energy model
                        </span>

                        <span style="
                            color:#31d68e;
                            font-size:9px;
                            font-weight:800;
                        ">
                            {"ONLINE" if energy_loaded else "OFFLINE"}
                        </span>

                    </div>

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        padding:10px 0;
                        border-bottom:
                            1px solid #11263d;
                    ">

                        <span style="
                            color:#7890ad;
                            font-size:9px;
                        ">
                            Anomaly model
                        </span>

                        <span style="
                            color:#31d68e;
                            font-size:9px;
                            font-weight:800;
                        ">
                            {"ONLINE" if anomaly_loaded else "OFFLINE"}
                        </span>

                    </div>

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        padding:10px 0;
                    ">

                        <span style="
                            color:#7890ad;
                            font-size:9px;
                        ">
                            Backend ML records
                        </span>

                        <span style="
                            color:#ffffff;
                            font-size:9px;
                            font-weight:800;
                        ">
                            {model_records:,}
                        </span>

                    </div>

                </div>

            </div>
            """
        )

    # ============================================================
    # ACTUAL VS PREDICTED MINI CHART
    # ============================================================

    if (
        not model_df.empty
        and
        "actual_power_watts"
        in model_df.columns
        and
        "predicted_power_watts"
        in model_df.columns
    ):

        render_html(
            """
            <div style="
                color:#ffffff;
                font-size:16px;
                font-weight:800;
                margin-top:24px;
                margin-bottom:8px;
            ">
                Prediction Monitoring
            </div>
            """
        )

        chart_model_df = model_df.copy()

        chart_model_df["Actual"] = pd.to_numeric(
            chart_model_df[
                "actual_power_watts"
            ],
            errors="coerce"
        )

        chart_model_df["Predicted"] = pd.to_numeric(
            chart_model_df[
                "predicted_power_watts"
            ],
            errors="coerce"
        )

        chart_model_df = (
            chart_model_df
            .dropna(
                subset=[
                    "Actual",
                    "Predicted"
                ]
            )
            .tail(40)
        )

        if not chart_model_df.empty:

            prediction_chart = go.Figure()

            prediction_chart.add_trace(
                go.Scatter(
                    x=list(
                        range(
                            len(
                                chart_model_df
                            )
                        )
                    ),
                    y=chart_model_df[
                        "Actual"
                    ],
                    mode="lines",
                    name="Actual",
                    line={
                        "width": 2
                    },
                )
            )

            prediction_chart.add_trace(
                go.Scatter(
                    x=list(
                        range(
                            len(
                                chart_model_df
                            )
                        )
                    ),
                    y=chart_model_df[
                        "Predicted"
                    ],
                    mode="lines",
                    name="Predicted",
                    line={
                        "width": 1.5,
                        "dash": "dash"
                    },
                )
            )

            prediction_chart.update_layout(
                height=260,
                margin=dict(
                    l=10,
                    r=10,
                    t=10,
                    b=10
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="#8ea5c1"
                ),
                xaxis=dict(
                    showgrid=False,
                    title="Recent ML Records"
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#13263d",
                    title="Power (W)"
                ),
                legend=dict(
                    orientation="h",
                    y=1.08
                )
            )

            st.plotly_chart(
                prediction_chart,
                use_container_width=True,
                config={
                    "displayModeBar": False
                },
                key="model_center_prediction_chart"
            )

    # ============================================================
    # MODEL INFORMATION
    # ============================================================

    render_html(
        """
        <div style="
            background:#07111f;
            border:1px solid #183452;
            border-radius:14px;
            padding:15px 17px;
            margin-top:20px;
        ">

            <div style="
                color:#ffffff;
                font-size:12px;
                font-weight:800;
            ">
                🧠 AI Pipeline
            </div>

            <div style="
                color:#6f8fb7;
                font-size:9px;
                line-height:1.7;
                margin-top:6px;
            ">
                Sensor data → trained ML models →
                energy prediction + anomaly detection →
                PostgreSQL ML results →
                dashboard analytics.
            </div>

        </div>
        """
    )

    # ============================================================
    # REFRESH
    # ============================================================

    if st.button(
        "↻ Refresh Model Status",
        key="model_center_refresh"
    ):

        st.rerun()

    st.stop()


elif current_page == "Support":

    # ============================================================
    # SUPPORT PAGE
    # ============================================================

    render_html(
        """
        <style>
        .support-header {
            margin-bottom: 28px;
        }

        .support-title {
            font-size: 30px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 6px;
        }

        .support-subtitle {
            color: #6fa9e8;
            font-size: 14px;
        }

        .support-hero {
            background:
                linear-gradient(135deg, #0b1d38 0%, #081426 55%, #07101f 100%);
            border: 1px solid #164b85;
            border-radius: 18px;
            padding: 28px;
            margin-bottom: 22px;
            box-shadow: 0 0 30px rgba(0, 102, 255, 0.08);
        }

        .support-hero-title {
            color: #ffffff;
            font-size: 22px;
            font-weight: 750;
            margin-bottom: 8px;
        }

        .support-hero-text {
            color: #82a9d2;
            font-size: 13px;
            line-height: 1.6;
            max-width: 760px;
        }

        .support-card {
            background: #071323;
            border: 1px solid #12304f;
            border-radius: 16px;
            padding: 22px;
            min-height: 150px;
        }

        .support-card-icon {
            font-size: 25px;
            margin-bottom: 12px;
        }

        .support-card-title {
            color: #ffffff;
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 7px;
        }

        .support-card-text {
            color: #7096bd;
            font-size: 12px;
            line-height: 1.55;
        }

        .support-section-title {
            color: #ffffff;
            font-size: 19px;
            font-weight: 750;
            margin-top: 28px;
            margin-bottom: 14px;
        }

        .support-faq {
            background: #071323;
            border: 1px solid #12304f;
            border-radius: 14px;
            padding: 17px 20px;
            margin-bottom: 10px;
        }

        .support-faq-question {
            color: #ffffff;
            font-size: 14px;
            font-weight: 650;
            margin-bottom: 6px;
        }

        .support-faq-answer {
            color: #7096bd;
            font-size: 12px;
            line-height: 1.55;
        }

        .support-status {
            background: #071323;
            border: 1px solid #12304f;
            border-radius: 16px;
            padding: 20px;
        }

        .support-status-title {
            color: #ffffff;
            font-size: 15px;
            font-weight: 700;
            margin-bottom: 15px;
        }

        .support-status-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 11px 0;
            border-bottom: 1px solid #10263e;
        }

        .support-status-row:last-child {
            border-bottom: none;
        }

        .support-status-name {
            color: #8ab2dc;
            font-size: 12px;
        }

        .support-online {
            color: #39e6aa;
            font-size: 12px;
            font-weight: 700;
        }

        .support-active {
            color: #4ea1ff;
            font-size: 12px;
            font-weight: 700;
        }
        </style>

        <div class="support-header">
            <div class="support-title">Support</div>
            <div class="support-subtitle">
                Get help with your AI Home Intelligence system.
            </div>
        </div>

        <div class="support-hero">
            <div class="support-hero-title">
                👋 How can we help?
            </div>
            <div class="support-hero-text">
                Find answers, troubleshoot your smart-home devices,
                or contact support if you need assistance.
            </div>
        </div>
        """
    )

    # ============================================================
    # SUPPORT OPTIONS
    # ============================================================

    support_col1, support_col2, support_col3 = st.columns(3)

    with support_col1:
        render_html(
            """
            <div class="support-card">
                <div class="support-card-icon">📖</div>
                <div class="support-card-title">Help Center</div>
                <div class="support-card-text">
                    Learn how to use your dashboard, devices,
                    AI monitoring and energy tracking.
                </div>
            </div>
            """
        )

    with support_col2:
        render_html(
            """
            <div class="support-card">
                <div class="support-card-icon">⚡</div>
                <div class="support-card-title">Device Issues</div>
                <div class="support-card-text">
                    Check device status, power readings and
                    common smart-device problems.
                </div>
            </div>
            """
        )

    with support_col3:
        render_html(
            """
            <div class="support-card">
                <div class="support-card-icon">🤖</div>
                <div class="support-card-title">AI Monitoring</div>
                <div class="support-card-text">
                    Understand AI predictions, anomaly detection
                    and smart energy analysis.
                </div>
            </div>
            """
        )

    # ============================================================
    # SYSTEM STATUS
    # ============================================================

    render_html(
        """
        <div class="support-section-title">
            System Status
        </div>
        """
    )

    status_col1, status_col2 = st.columns(2)

    with status_col1:
        render_html(
            """
            <div class="support-status">
                <div class="support-status-title">
                    🟢 System Health
                </div>

                <div class="support-status-row">
                    <span class="support-status-name">Dashboard</span>
                    <span class="support-online">ONLINE</span>
                </div>

                <div class="support-status-row">
                    <span class="support-status-name">AI Monitoring</span>
                    <span class="support-active">ACTIVE</span>
                </div>

                <div class="support-status-row">
                    <span class="support-status-name">Device Monitoring</span>
                    <span class="support-online">RUNNING</span>
                </div>
            </div>
            """
        )

    with status_col2:
        render_html(
            """
            <div class="support-status">
                <div class="support-status-title">
                    🔧 Services
                </div>

                <div class="support-status-row">
                    <span class="support-status-name">Backend API</span>
                    <span class="support-online">ONLINE</span>
                </div>

                <div class="support-status-row">
                    <span class="support-status-name">Database</span>
                    <span class="support-online">CONNECTED</span>
                </div>

                <div class="support-status-row">
                    <span class="support-status-name">ML Models</span>
                    <span class="support-active">READY</span>
                </div>
            </div>
            """
        )

    # ============================================================
    # COMMON QUESTIONS
    # ============================================================

    render_html(
        """
        <div class="support-section-title">
            Common Questions
        </div>

        <div class="support-faq">
            <div class="support-faq-question">
                Why is my device showing OFFLINE?
            </div>
            <div class="support-faq-answer">
                Check whether the device is connected and available
                to the smart-home system. Refresh the Tracking page
                to retrieve the latest status.
            </div>
        </div>

        <div class="support-faq">
            <div class="support-faq-question">
                What does AI Prediction mean?
            </div>
            <div class="support-faq-answer">
                AI Prediction is the power consumption estimated by
                the trained machine-learning model.
            </div>
        </div>

        <div class="support-faq">
            <div class="support-faq-question">
                What does AI Status mean?
            </div>
            <div class="support-faq-answer">
                AI Status indicates whether the monitored device is
                operating normally or showing unusual activity.
            </div>
        </div>

        <div class="support-faq">
            <div class="support-faq-question">
                How can I see detailed device usage?
            </div>
            <div class="support-faq-answer">
                Open the Tracking page and select the device you want
                to monitor. You can view power readings and AI predictions.
            </div>
        </div>
        """
    )

    # ============================================================
    # CONTACT SUPPORT
    # ============================================================

    render_html(
        """
        <div class="support-section-title">
            Contact Support
        </div>
        """
    )

    with st.container(border=True):

        support_name = st.text_input(
            "Name",
            placeholder="Enter your name",
            key="support_name"
        )

        support_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="support_email"
        )

        support_issue = st.selectbox(
            "Issue Type",
            [
                "Device problem",
                "AI prediction issue",
                "Dashboard problem",
                "Account issue",
                "Other"
            ],
            key="support_issue"
        )

        support_message = st.text_area(
            "Message",
            placeholder="Describe your problem...",
            height=120,
            key="support_message"
        )

        if st.button(
            "Send Support Request",
            key="send_support_request",
            use_container_width=True
        ):

            if not support_name.strip():
                st.warning("Please enter your name.")

            elif not support_email.strip():
                st.warning("Please enter your email.")

            elif not support_message.strip():
                st.warning("Please describe your problem.")

            else:
                st.success(
                    "Support request submitted successfully."
                )            
    st.stop()
                
elif current_page == "How it works":

    # ---------------------------------------------------------
    # HOW IT WORKS - HEADER
    # ---------------------------------------------------------
    render_html(
        """
        <div class="page-header">
            <div class="page-title">How AI Home Intelligence Works</div>
            <div class="page-subtitle">
                Understand how smart-home data moves from devices
                through the backend and machine-learning models
                into useful AI insights.
            </div>
        </div>
        """
    )

    # ---------------------------------------------------------
    # SYSTEM FLOW
    # ---------------------------------------------------------
    render_html(
        """
        <div class="how-flow">

            <div class="how-flow-step">
                <div class="flow-number">01</div>
                <div class="flow-icon">📡</div>
                <div class="flow-title">Collect Data</div>
                <div class="flow-text">
                    Smart-home devices provide temperature, humidity,
                    device state and power-consumption readings.
                </div>
            </div>

            <div class="flow-arrow">→</div>

            <div class="how-flow-step">
                <div class="flow-number">02</div>
                <div class="flow-icon">🗄️</div>
                <div class="flow-title">Store Data</div>
                <div class="flow-text">
                    Sensor readings and device information are stored
                    in the PostgreSQL database for analysis.
                </div>
            </div>

            <div class="flow-arrow">→</div>

            <div class="how-flow-step">
                <div class="flow-number">03</div>
                <div class="flow-icon">🤖</div>
                <div class="flow-title">Run ML Models</div>
                <div class="flow-text">
                    Trained machine-learning models analyze home
                    conditions and generate predictions and anomalies.
                </div>
            </div>

            <div class="flow-arrow">→</div>

            <div class="how-flow-step">
                <div class="flow-number">04</div>
                <div class="flow-icon">💡</div>
                <div class="flow-title">Generate Insights</div>
                <div class="flow-text">
                    ML results are converted into understandable
                    insights, monitoring information and alerts.
                </div>
            </div>

        </div>
        """
    )

    # ---------------------------------------------------------
    # ARCHITECTURE
    # ---------------------------------------------------------
    render_html(
        """
        <div class="how-section-title">
            <div>System architecture</div>
            <span>How the main components work together</span>
        </div>

        <div class="how-grid">

            <div class="how-card">
                <div class="how-card-icon">📡</div>
                <div class="how-card-title">1. Smart Devices</div>
                <div class="how-card-text">
                    Connected home devices provide information such as
                    device state, temperature, humidity and power usage.
                </div>

                <div class="how-card-tags">
                    <span>Devices</span>
                    <span>Sensors</span>
                    <span>Power</span>
                </div>
            </div>

            <div class="how-card">
                <div class="how-card-icon">🗄️</div>
                <div class="how-card-title">2. PostgreSQL Database</div>
                <div class="how-card-text">
                    Device information, sensor readings, users,
                    automations and machine-learning results are stored
                    in the PostgreSQL database.
                </div>

                <div class="how-card-tags">
                    <span>PostgreSQL</span>
                    <span>Storage</span>
                    <span>Records</span>
                </div>
            </div>

            <div class="how-card">
                <div class="how-card-icon">⚙️</div>
                <div class="how-card-title">3. FastAPI Backend</div>
                <div class="how-card-text">
                    The FastAPI backend connects the dashboard with the
                    database and exposes APIs for devices, readings,
                    users, automations and ML results.
                </div>

                <div class="how-card-tags">
                    <span>FastAPI</span>
                    <span>REST API</span>
                    <span>Backend</span>
                </div>
            </div>

            <div class="how-card">
                <div class="how-card-icon">🧠</div>
                <div class="how-card-title">4. Energy Prediction</div>
                <div class="how-card-text">
                    A trained Linear Regression model predicts expected
                    power consumption from the available home conditions.
                </div>

                <div class="how-card-tags">
                    <span>Linear Regression</span>
                    <span>Prediction</span>
                    <span>Energy</span>
                </div>
            </div>

            <div class="how-card">
                <div class="how-card-icon">🔍</div>
                <div class="how-card-title">5. Anomaly Detection</div>
                <div class="how-card-text">
                    An Isolation Forest model identifies readings that
                    differ from normal energy-consumption patterns.
                </div>

                <div class="how-card-tags">
                    <span>Isolation Forest</span>
                    <span>Anomaly</span>
                    <span>Monitoring</span>
                </div>
            </div>

            <div class="how-card">
                <div class="how-card-icon">📊</div>
                <div class="how-card-title">6. Streamlit Dashboard</div>
                <div class="how-card-text">
                    The dashboard presents device activity, energy
                    analysis, AI predictions, anomalies and reports
                    in an interactive interface.
                </div>

                <div class="how-card-tags">
                    <span>Streamlit</span>
                    <span>Charts</span>
                    <span>Insights</span>
                </div>
            </div>

        </div>
        """
    )

    # ---------------------------------------------------------
    # DATA → AI → DECISION PIPELINE
    # ---------------------------------------------------------
    render_html(
        """
        <div class="how-section-title">
            <div>Data → AI → Decision</div>
            <span>The complete intelligence pipeline</span>
        </div>

        <div class="how-detail-card">

            <div class="how-detail-header">
                <div>
                    <div class="how-detail-title">
                        🧠 From raw readings to intelligent insights
                    </div>

                    <div class="how-detail-subtitle">
                        Each stage transforms the data into information
                        that can be used by the dashboard.
                    </div>
                </div>

                <div class="how-status">
                    ● AI PIPELINE ACTIVE
                </div>
            </div>

            <div class="how-detail-content">

                <div class="detail-item">
                    <div class="detail-icon">1</div>
                    <div>
                        <strong>Input data</strong>
                        <p>
                            Temperature, humidity, device state and
                            power-consumption values enter the system.
                        </p>
                    </div>
                </div>

                <div class="detail-item">
                    <div class="detail-icon">2</div>
                    <div>
                        <strong>Data storage</strong>
                        <p>
                            The backend stores and retrieves readings
                            from PostgreSQL through API endpoints.
                        </p>
                    </div>
                </div>

                <div class="detail-item">
                    <div class="detail-icon">3</div>
                    <div>
                        <strong>Feature processing</strong>
                        <p>
                            Relevant home conditions are prepared in the
                            format required by the trained ML models.
                        </p>
                    </div>
                </div>

                <div class="detail-item">
                    <div class="detail-icon">4</div>
                    <div>
                        <strong>Energy prediction</strong>
                        <p>
                            The Linear Regression model estimates expected
                            power consumption for the given conditions.
                        </p>
                    </div>
                </div>

                <div class="detail-item">
                    <div class="detail-icon">5</div>
                    <div>
                        <strong>Anomaly detection</strong>
                        <p>
                            Isolation Forest evaluates the readings and
                            identifies unusual energy-consumption behavior.
                        </p>
                    </div>
                </div>

                <div class="detail-item">
                    <div class="detail-icon">6</div>
                    <div>
                        <strong>Dashboard insight</strong>
                        <p>
                            Predictions and anomaly results are displayed
                            as charts, KPIs, alerts and AI insights.
                        </p>
                    </div>
                </div>

            </div>

        </div>
        """
    )

    # ---------------------------------------------------------
    # ML MODEL EXPLANATION
    # ---------------------------------------------------------
    render_html(
        """
        <div class="how-section-title">
            <div>Machine-learning models</div>
            <span>What each model does inside the system</span>
        </div>

        <div class="how-grid">

            <div class="how-card">
                <div class="how-card-icon">📈</div>

                <div class="how-card-title">
                    Linear Regression
                </div>

                <div class="how-card-text">
                    Used for energy prediction. The model learns the
                    relationship between home conditions and historical
                    power consumption to estimate expected power usage.
                </div>

                <div class="how-card-tags">
                    <span>Supervised</span>
                    <span>Regression</span>
                    <span>Energy Prediction</span>
                </div>
            </div>

            <div class="how-card">
                <div class="how-card-icon">🛡️</div>

                <div class="how-card-title">
                    Isolation Forest
                </div>

                <div class="how-card-text">
                    Used for anomaly detection. The model identifies
                    observations that appear different from normal
                    energy-consumption behavior.
                </div>

                <div class="how-card-tags">
                    <span>Unsupervised</span>
                    <span>Anomaly Detection</span>
                    <span>Monitoring</span>
                </div>
            </div>

        </div>
        """
    )

    # ---------------------------------------------------------
    # TRACKING EXPLANATION
    # ---------------------------------------------------------
    render_html(
        """
        <div class="how-section-title">
            <div>How energy tracking works</div>
            <span>Understand actual usage and AI predictions</span>
        </div>

        <div class="how-detail-card">

            <div class="how-detail-header">
                <div>
                    <div class="how-detail-title">
                        📈 Energy monitoring workflow
                    </div>

                    <div class="how-detail-subtitle">
                        The Tracking dashboard combines real readings
                        with machine-learning results.
                    </div>
                </div>

                <div class="how-status">
                    ● MONITORING
                </div>
            </div>

            <div class="how-detail-content">

                <div class="detail-item">
                    <div class="detail-icon">1</div>
                    <div>
                        <strong>Read sensor data</strong>
                        <p>
                            The system retrieves recorded power readings
                            and device information from the backend.
                        </p>
                    </div>
                </div>

                <div class="detail-item">
                    <div class="detail-icon">2</div>
                    <div>
                        <strong>Calculate energy usage</strong>
                        <p>
                            Power readings are analyzed to understand
                            consumption over time.
                        </p>
                    </div>
                </div>

                <div class="detail-item">
                    <div class="detail-icon">3</div>
                    <div>
                        <strong>Compare actual and predicted values</strong>
                        <p>
                            The dashboard compares measured power with
                            the AI model's predicted power values.
                        </p>
                    </div>
                </div>

                <div class="detail-item">
                    <div class="detail-icon">4</div>
                    <div>
                        <strong>Identify unusual behavior</strong>
                        <p>
                            Anomaly results help highlight readings that
                            require additional attention.
                        </p>
                    </div>
                </div>

            </div>

        </div>
        """
    )

    # ---------------------------------------------------------
    # WHAT THE USER CAN DO
    # ---------------------------------------------------------
    render_html(
        """
        <div class="how-section-title">
            <div>What you can do with the system</div>
            <span>Key capabilities available in the dashboard</span>
        </div>

        <div class="how-grid">

            <div class="how-card">
                <div class="how-card-icon">💡</div>
                <div class="how-card-title">Monitor Devices</div>
                <div class="how-card-text">
                    View connected devices, their status and available
                    device information from the dashboard.
                </div>
            </div>

            <div class="how-card">
                <div class="how-card-icon">📊</div>
                <div class="how-card-title">Track Energy</div>
                <div class="how-card-text">
                    Analyze energy consumption patterns and compare
                    actual readings with AI predictions.
                </div>
            </div>

            <div class="how-card">
                <div class="how-card-icon">🤖</div>
                <div class="how-card-title">Understand AI Results</div>
                <div class="how-card-text">
                    Review prediction performance, anomaly results and
                    model information through the AI sections.
                </div>
            </div>

            <div class="how-card">
                <div class="how-card-icon">🔔</div>
                <div class="how-card-title">Review Alerts</div>
                <div class="how-card-text">
                    Check unusual device activity and system alerts
                    generated from monitoring information.
                </div>
            </div>

            <div class="how-card">
                <div class="how-card-icon">⚙️</div>
                <div class="how-card-title">Automate Devices</div>
                <div class="how-card-text">
                    Create automation rules that connect triggers,
                    schedules and device actions.
                </div>
            </div>

            <div class="how-card">
                <div class="how-card-icon">📄</div>
                <div class="how-card-title">Generate Reports</div>
                <div class="how-card-text">
                    Review energy statistics, device usage, AI analysis
                    and downloadable report information.
                </div>
            </div>

        </div>
        """
    )

    # ---------------------------------------------------------
    # SIMPLE SUMMARY
    # ---------------------------------------------------------
    render_html(
        """
        <div class="how-summary">

            <div class="summary-icon">🏠</div>

            <div>
                <div class="summary-title">
                    Smart home intelligence in one place
                </div>

                <div class="summary-text">
                    AI Home Intelligence combines smart-device data,
                    PostgreSQL storage, FastAPI services, machine-learning
                    models and an interactive Streamlit dashboard to turn
                    raw home readings into understandable energy insights.
                </div>
            </div>

        </div>
        """
    )

    st.stop()                


# ============================================================
# PAGE HEADER
# ============================================================

render_html(
    """
    <div class="page-header">

        <div class="page-title">
            AI Home Intelligence
        </div>

        <div class="page-subtitle">
            Smart Home Monitoring & Machine Learning Dashboard
        </div>

    </div>
    """
)


# ============================================================
# HERO SUMMARY
# ============================================================

# Show active users from the PostgreSQL users table.
active_users = [
    user
    for user in (users_api or [])
    if bool(user.get("status", False))
]

user_avatars_html = "".join(
    f"<span class=\"user-avatar\">{escape(user.get('avatar', '👤'))}</span>"
    for user in active_users[:4]
)

if not user_avatars_html:
    user_avatars_html = '<span class="hero-small">No active users</span>'


render_html(
    f"""
    <div class="hero">

        <div class="hero-grid">

            <div class="hero-energy">

                <div class="saving-ring">
                    {energy_saved}%
                </div>

                <div>

                    <div class="hero-label">
                        Energy saved
                    </div>

                    <div class="hero-number">
                        {energy_saved}%
                    </div>

                    <div class="hero-small">
                        Equivalent to
                        <span class="money">
                            ${equivalent_savings}
                        </span>
                    </div>

                </div>

            </div>


            <div class="hero-divider">
            </div>


            <div>

                <div class="hero-label">
                    Current users
                </div>

                <div class="avatar-row">
                    {user_avatars_html}
                </div>

            </div>

        </div>

    </div>
    """
)


# ============================================================
# DEVICE / SETTINGS TABS
# ============================================================

render_html(
    """
    <div class="tabs">

        <div class="tab-active">
            ▣ &nbsp; Devices
        </div>

        <div class="tab">
            ⚙ &nbsp; Settings
        </div>

    </div>
    """
)

# ============================================================
# DEVICE CARDS
# ============================================================

reference_devices = [
    {
        "name": "Smart Webcam",
        "type": "Camera",
        "icon": "📹",
        "status": True,
        "room": "Wi-Fi",
        "id": 7,
    },
    {
        "name": "Stereo Speaker",
        "type": "Speaker",
        "icon": "🔊",
        "status": True,
        "room": "Wi-Fi",
        "id": 8,
    },
    {
        "name": "Room Light",
        "type": "Light",
        "icon": "💡",
        "status": False,
        "room": "Wi-Fi",
        "id": 9,
    },
]

device_columns = st.columns(3)


for column, device in zip(
    device_columns,
    reference_devices,
):

    with column:

        # Find matching device from PostgreSQL
        backend_device = next(
            (
                item
                for item in devices
                if str(
                    item.get("name", "")
                ).lower()
                == device["name"].lower()
            ),
            None,
        )

        if backend_device:

            device["id"] = backend_device.get("id")

            device["status"] = bool(
                backend_device.get(
                    "status",
                    device["status"]
                )
            )

        device_id = device.get("id")

        # ----------------------------------------------------
        # DEVICE CARD
        # ----------------------------------------------------

        with st.container(
            key=f"home_device_card_{device_id}"
        ):

            top_left, top_right = st.columns(
                [4, 1]
            )

            with top_left:

                render_html(
                    f"""
                    <div class="home-device-icon">
                        {device["icon"]}
                    </div>

                    <div class="home-device-name">
                        {escape(device["name"])}
                    </div>

                    <div class="home-device-meta">
                        ◔ &nbsp; Wi-Fi
                    </div>
                    """
                )

            with top_right:

                new_status = st.toggle(
                    "",
                    value=device["status"],
                    key=f"home_device_toggle_{device_id}",
                    label_visibility="collapsed",
                )

            # ------------------------------------------------
            # UPDATE POSTGRESQL
            # ------------------------------------------------

            if new_status != device["status"]:

                try:

                    response = requests.put(
                        f"{API_URL}/devices/{device_id}/status",
                        params={
                            "status": new_status
                        },
                        timeout=3,
                    )

                    if response.status_code == 200:

                        st.rerun()

                    else:

                        st.error(
                            "Unable to update device status."
                        )

                except requests.RequestException:

                    st.error(
                        "Backend is not available."
                    )


# ============================================================
# HOME DEVICE CARD STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* Device card */
    div[class*="st-key-home_device_card_"] {
        background: #081321;
        border: 1px solid #19304a;
        border-radius: 14px;
        padding: 18px;
        min-height: 94px;
        margin-bottom: 8px;
        transition: all 0.2s ease;
    }

    div[class*="st-key-home_device_card_"]:hover {
        border-color: #24527d;
        transform: translateY(-1px);
    }

    /* Device icon */
    .home-device-icon {
        font-size: 28px;
        margin-bottom: 6px;
    }

    /* Device name */
    .home-device-name {
        color: #f5f7fb;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    /* Wi-Fi */
    .home-device-meta {
        color: #7d91a8;
        font-size: 10px;
    }

    /* Toggle position */
    div[class*="st-key-home_device_card_"]
    [data-testid="stToggle"] {
        margin-top: 3px;
        display: flex;
        justify-content: flex-end;
    }

    /* Hide toggle text */
    div[class*="st-key-home_device_card_"]
    [data-testid="stToggle"] label {
        display: none !important;
    }

    /* Toggle */
    div[class*="st-key-home_device_card_"]
    [role="switch"] {
        width: 42px !important;
        height: 23px !important;
        border-radius: 20px !important;
    }

    /* ON = green */
    div[class*="st-key-home_device_card_"]
    [role="switch"][aria-checked="true"] {
        background-color: #10b981 !important;
        border-color: #10b981 !important;
    }

    /* OFF = dark */
    div[class*="st-key-home_device_card_"]
    [role="switch"][aria-checked="false"] {
        background-color: #334155 !important;
        border-color: #334155 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SUGGESTED CATEGORIES
# ============================================================

# ------------------------------------------------------------
# CATEGORY MANAGEMENT VIEW
# ------------------------------------------------------------

if st.session_state.get(
    "category_management",
    False
):

    render_html(
        """
        <div class="section-title">
            <span>
                Category Management
            </span>
        </div>
        """
    )

    back_col, add_col = st.columns(
        [6, 1]
    )

    with back_col:

        if st.button(
            "← Back",
            key="category_back"
        ):

            st.session_state[
                "category_management"
            ] = False

            st.rerun()

    with add_col:

        add_category_clicked = st.button(
            "＋ Add",
            key="add_category_button"
        )


    # --------------------------------------------------------
    # ADD CATEGORY
    # --------------------------------------------------------

    if add_category_clicked:

        st.session_state[
            "show_add_category"
        ] = True

        st.session_state[
            "edit_category_id"
        ] = None


    if st.session_state.get(
        "show_add_category",
        False
    ):

        st.markdown(
            "### Add Category"
        )

        with st.form(
            "add_category_form"
        ):

            new_name = st.text_input(
                "Category Name"
            )

            new_icon = st.text_input(
                "Icon",
                value="🏠"
            )

            new_description = st.text_input(
                "Description"
            )

            new_status = st.checkbox(
                "Active",
                value=True
            )

            save_category = st.form_submit_button(
                "Add Category"
            )

            cancel_category = st.form_submit_button(
                "Cancel"
            )


        if save_category:

            if not new_name.strip():

                st.error(
                    "Category name is required."
                )

            else:

                response = requests.post(
                    f"{API_URL}/categories",
                    params={
                        "name": new_name,
                        "icon": new_icon,
                        "description": new_description,
                        "status": new_status,
                    },
                    timeout=10,
                )

                if response.ok:

                    st.success(
                        "Category added successfully."
                    )

                    st.session_state[
                        "show_add_category"
                    ] = False

                    st.rerun()

                else:

                    st.error(
                        "Unable to add category."
                    )


        if cancel_category:

            st.session_state[
                "show_add_category"
            ] = False

            st.rerun()


    # --------------------------------------------------------
    # GET CATEGORIES
    # --------------------------------------------------------

    categories_api = api_get(
        "/categories"
    )

    categories_data = (
        categories_api.get(
            "categories",
            []
        )
        if isinstance(
            categories_api,
            dict
        )
        else []
    )


    # --------------------------------------------------------
    # CATEGORY MANAGEMENT LIST
    # --------------------------------------------------------

    render_html(
        """
        <div style="
            margin-top: 20px;
            margin-bottom: 12px;
            font-size: 15px;
            font-weight: 700;
        ">
            All Categories
        </div>
        """
    )


    for category in categories_data:

        category_id = category.get(
            "id"
        )

        category_name = category.get(
            "name",
            "Category"
        )

        category_icon = category.get(
            "icon",
            "🏠"
        )

        category_description = category.get(
            "description",
            ""
        )

        category_status = bool(
            category.get(
                "status",
                True
            )
        )


        # ----------------------------------------------------
        # EDIT MODE
        # ----------------------------------------------------

        if st.session_state.get(
            "edit_category_id"
        ) == category_id:

            st.markdown(
                f"### Edit {category_name}"
            )

            with st.form(
                f"edit_category_form_{category_id}"
            ):

                edit_name = st.text_input(
                    "Category Name",
                    value=category_name
                )

                edit_icon = st.text_input(
                    "Icon",
                    value=category_icon
                )

                edit_description = st.text_input(
                    "Description",
                    value=category_description
                )

                edit_status = st.checkbox(
                    "Active",
                    value=category_status
                )

                update_category = st.form_submit_button(
                    "Update"
                )

                cancel_edit = st.form_submit_button(
                    "Cancel"
                )


            if update_category:

                if not edit_name.strip():

                    st.error(
                        "Category name is required."
                    )

                else:

                    response = requests.put(
                        f"{API_URL}/categories/{category_id}",
                        params={
                            "name": edit_name,
                            "icon": edit_icon,
                            "description": edit_description,
                            "status": edit_status,
                        },
                        timeout=10,
                    )

                    if response.ok:

                        st.success(
                            "Category updated successfully."
                        )

                        st.session_state[
                            "edit_category_id"
                        ] = None

                        st.rerun()

                    else:

                        st.error(
                            "Unable to update category."
                        )


            if cancel_edit:

                st.session_state[
                    "edit_category_id"
                ] = None

                st.rerun()

            continue


        # ----------------------------------------------------
        # NORMAL CATEGORY ROW
        # ----------------------------------------------------

        row_col_1, row_col_2, row_col_3, row_col_4 = st.columns(
            [1, 4, 1, 1]
        )


        with row_col_1:

            st.markdown(
                f"### {escape(str(category_icon))}"
            )


        with row_col_2:

            st.markdown(
                f"**{escape(str(category_name))}**"
            )

            st.caption(
                str(category_description)
            )


        with row_col_3:

            status_changed = st.checkbox(
                "Active",
                value=category_status,
                key=f"category_status_{category_id}"
            )


        with row_col_4:

            edit_clicked = st.button(
                "✏️ Edit",
                key=f"edit_category_{category_id}"
            )


            delete_clicked = st.button(
                "🗑️ Delete",
                key=f"delete_category_{category_id}"
            )


        # ----------------------------------------------------
        # STATUS UPDATE
        # ----------------------------------------------------

        if status_changed != category_status:

            response = requests.put(
                f"{API_URL}/categories/{category_id}",
                params={
                    "name": category_name,
                    "icon": category_icon,
                    "description": category_description,
                    "status": status_changed,
                },
                timeout=10,
            )

            if response.ok:

                st.rerun()

            else:

                st.error(
                    "Unable to update category status."
                )


        # ----------------------------------------------------
        # EDIT
        # ----------------------------------------------------

        if edit_clicked:

            st.session_state[
                "edit_category_id"
            ] = category_id

            st.rerun()


        # ----------------------------------------------------
        # DELETE
        # ----------------------------------------------------

        if delete_clicked:

            response = requests.delete(
                f"{API_URL}/categories/{category_id}",
                timeout=10,
            )

            if response.ok:

                st.success(
                    "Category deleted successfully."
                )

                st.rerun()

            else:

                st.error(
                    "Unable to delete category."
                )


        st.divider()


    st.stop()

# ============================================================
# SUGGESTED CATEGORIES
# ============================================================


# ============================================================
# CATEGORY MANAGEMENT PAGE
# ============================================================

if st.session_state.get(
    "category_management",
    False
):

    render_html(
        """
        <div style="
            margin-bottom: 25px;
        ">

            <div style="
                font-size: 26px;
                font-weight: 800;
                margin-bottom: 6px;
            ">
                Category Management
            </div>

            <div style="
                font-size: 13px;
                opacity: 0.65;
            ">
                Manage your smart home categories
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # TOP ACTIONS
    # --------------------------------------------------------

    back_col, spacer_col, add_col = st.columns(
        [1.5, 4.5, 1.5]
    )


    with back_col:

        if st.button(
            "← Back",
            key="category_management_back"
        ):

            st.session_state[
                "category_management"
            ] = False

            st.session_state[
                "show_add_category"
            ] = False

            st.session_state[
                "edit_category_id"
            ] = None

            st.rerun()


    with add_col:

        if st.button(
            "＋ Add Category",
            key="category_add_button"
        ):

            st.session_state[
                "show_add_category"
            ] = True

            st.session_state[
                "edit_category_id"
            ] = None

            st.rerun()


    # --------------------------------------------------------
    # LOAD CATEGORIES
    # --------------------------------------------------------

    categories_api = api_get(
        "/categories"
    )


    categories_from_database = (
        categories_api.get(
            "categories",
            []
        )
        if isinstance(
            categories_api,
            dict
        )
        else []
    )


    # --------------------------------------------------------
    # CATEGORY SUMMARY
    # --------------------------------------------------------

    total_categories = len(
        categories_from_database
    )

    active_categories = sum(
        1
        for category in categories_from_database
        if bool(
            category.get(
                "status",
                True
            )
        )
    )

    inactive_categories = (
        total_categories
        - active_categories
    )


    summary_col_1, summary_col_2, summary_col_3 = st.columns(
        3
    )


    with summary_col_1:

        st.metric(
            "Total Categories",
            total_categories
        )


    with summary_col_2:

        st.metric(
            "Active",
            active_categories
        )


    with summary_col_3:

        st.metric(
            "Inactive",
            inactive_categories
        )


    # --------------------------------------------------------
    # ADD CATEGORY FORM
    # --------------------------------------------------------

    if st.session_state.get(
        "show_add_category",
        False
    ):

        st.markdown(
            "### Add New Category"
        )


        with st.form(
            "add_category_form"
        ):

            add_col_1, add_col_2 = st.columns(
                2
            )


            with add_col_1:

                new_name = st.text_input(
                    "Category Name",
                    placeholder="Example: Security"
                )


                new_icon = st.text_input(
                    "Icon",
                    value="🏠",
                    max_chars=10
                )


            with add_col_2:

                new_description = st.text_input(
                    "Description",
                    placeholder="Example: Monitor home security"
                )


                new_status = st.checkbox(
                    "Active",
                    value=True
                )


            save_category = st.form_submit_button(
                "＋ Add Category"
            )


            cancel_category = st.form_submit_button(
                "Cancel"
            )


        if save_category:

            if not new_name.strip():

                st.error(
                    "Category name is required."
                )

            else:

                response = requests.post(
                    f"{API_URL}/categories",
                    params={
                        "name": new_name.strip(),
                        "icon": new_icon,
                        "description": new_description.strip(),
                        "status": new_status,
                    },
                    timeout=10,
                )


                if response.ok:

                    st.success(
                        "Category added successfully."
                    )

                    st.session_state[
                        "show_add_category"
                    ] = False

                    st.rerun()

                else:

                    st.error(
                        "Unable to add category."
                    )


        if cancel_category:

            st.session_state[
                "show_add_category"
            ] = False

            st.rerun()


    # --------------------------------------------------------
    # MANAGEMENT CATEGORY COLORS
    # --------------------------------------------------------

    category_color_classes = [

        "security",
        "climate",
        "sensors",
        "appliances",
        "lighting",
        "locks",
        "entertainment",
        "energy",

    ]


    # --------------------------------------------------------
    # CATEGORY MANAGEMENT LIST
    # --------------------------------------------------------

    st.markdown(
        "### All Categories"
    )


    for index, category in enumerate(
        categories_from_database
    ):

        category_id = category.get(
            "id"
        )

        category_name = str(
            category.get(
                "name",
                "Category"
            )
        )

        category_icon = str(
            category.get(
                "icon",
                "🏠"
            )
        )

        category_description = str(
            category.get(
                "description",
                ""
            )
        )

        category_status = bool(
            category.get(
                "status",
                True
            )
        )


        category_name_class = (
            category_name
            .lower()
            .replace(
                " ",
                "-"
            )
        )


        known_classes = {

            "security",
            "climate",
            "sensors",
            "appliances",
            "lighting",
            "remote-lock",
            "locks",
            "entertainment",
            "energy",

        }


        if category_name_class in known_classes:

            css_class = category_name_class

        else:

            css_class = category_color_classes[
                index
                % len(category_color_classes)
            ]


        # ====================================================
        # EDIT MODE
        # ====================================================

        if st.session_state.get(
            "edit_category_id"
        ) == category_id:

            st.markdown(
                f"### ✏️ Edit {category_name}"
            )


            with st.form(
                f"edit_category_form_{category_id}"
            ):

                edit_col_1, edit_col_2 = st.columns(
                    2
                )


                with edit_col_1:

                    edit_name = st.text_input(
                        "Category Name",
                        value=category_name
                    )


                    edit_icon = st.text_input(
                        "Icon",
                        value=category_icon,
                        max_chars=10
                    )


                with edit_col_2:

                    edit_description = st.text_input(
                        "Description",
                        value=category_description
                    )


                    edit_status = st.checkbox(
                        "Active",
                        value=category_status
                    )


                update_category = st.form_submit_button(
                    "✓ Update Category"
                )


                cancel_edit = st.form_submit_button(
                    "Cancel"
                )


            if update_category:

                if not edit_name.strip():

                    st.error(
                        "Category name is required."
                    )

                else:

                    response = requests.put(
                        f"{API_URL}/categories/{category_id}",
                        params={
                            "name": edit_name.strip(),
                            "icon": edit_icon,
                            "description": edit_description.strip(),
                            "status": edit_status,
                        },
                        timeout=10,
                    )


                    if response.ok:

                        st.success(
                            "Category updated successfully."
                        )

                        st.session_state[
                            "edit_category_id"
                        ] = None

                        st.rerun()

                    else:

                        st.error(
                            "Unable to update category."
                        )


            if cancel_edit:

                st.session_state[
                    "edit_category_id"
                ] = None

                st.rerun()


            st.divider()

            continue


        # ====================================================
        # CATEGORY MANAGEMENT CARD
        # ====================================================

        render_html(
            f"""
            <div class="
                category-card
                {css_class}
            "
            style="
                margin-bottom: 8px;
            ">

                <div class="category-row">

                    <div class="category-icon">
                        {escape(category_icon)}
                    </div>

                    <div>

                        <div class="category-title">
                            {escape(category_name)}
                        </div>

                        <div class="category-count">
                            ● &nbsp;
                            {
                                "Active"
                                if category_status
                                else "Inactive"
                            }
                        </div>

                    </div>

                </div>

                <div style="
                    margin-top: 10px;
                    font-size: 12px;
                    opacity: 0.65;
                ">
                    {escape(category_description)}
                </div>

            </div>
            """
        )


        # ----------------------------------------------------
        # ACTION BUTTONS
        # ----------------------------------------------------

        action_col_1, action_col_2, action_col_3 = st.columns(
            [1, 1, 4]
        )


        with action_col_1:

            edit_clicked = st.button(
                "✏️ Edit",
                key=f"edit_category_{category_id}"
            )


        with action_col_2:

            delete_clicked = st.button(
                "🗑️ Delete",
                key=f"delete_category_{category_id}"
            )


        # ----------------------------------------------------
        # EDIT
        # ----------------------------------------------------

        if edit_clicked:

            st.session_state[
                "edit_category_id"
            ] = category_id

            st.session_state[
                "show_add_category"
            ] = False

            st.rerun()


        # ----------------------------------------------------
        # DELETE
        # ----------------------------------------------------

        if delete_clicked:

            response = requests.delete(
                f"{API_URL}/categories/{category_id}",
                timeout=10,
            )


            if response.ok:

                st.success(
                    "Category deleted successfully."
                )

                st.rerun()

            else:

                st.error(
                    "Unable to delete category."
                )


        st.divider()


    # IMPORTANT:
    # Stop only the management page here.
    # Never put st.stop() inside the category card loop.

    st.stop()


# ============================================================
# SUGGESTED CATEGORIES HEADER
# ============================================================

category_title_col, category_view_col = st.columns(
    [6, 1]
)


with category_title_col:

    render_html(
        """
        <div class="section-title">

            <span>
                Suggested Categories
            </span>

        </div>
        """
    )


with category_view_col:

    view_all_clicked = st.button(
        "View all →",
        key="view_all_categories"
    )


if view_all_clicked:

    st.session_state[
        "category_management"
    ] = True

    st.session_state[
        "show_add_category"
    ] = False

    st.session_state[
        "edit_category_id"
    ] = None

    st.rerun()


# ============================================================
# CATEGORY DATA
# ============================================================

categories = [

    (
        "security",
        "🛡️",
        "Security",
        "2 Cameras",
    ),

    (
        "climate",
        "▤",
        "Climate-Con",
        "2 AC",
    ),

    (
        "sensors",
        "◉",
        "Sensors",
        "Humidity & Air",
    ),

    (
        "appliances",
        "▣",
        "Appliances",
        "1 Fridge",
    ),

    (
        "lighting",
        "💡",
        "Lighting",
        "5 Devices",
    ),

    (
        "locks",
        "🔒",
        "Remote Lock",
        "6 Doors",
    ),

    (
        "entertainment",
        "▣",
        "Entertainment",
        "2 TV",
    ),

    (
        "energy",
        "ϟ",
        "Energy",
        "Usage Insights",
    ),

]


# ============================================================
# CATEGORY CARDS
# ============================================================

category_columns = st.columns(4)


for index, category in enumerate(
    categories
):

    css_class, icon, title, count = category

    with category_columns[
        index % 4
    ]:

        render_html(
            f"""
            <div class="
                category-card
                {css_class}
            ">

                <div class="category-row">

                    <div class="category-icon">
                        {icon}
                    </div>

                    <div>

                        <div class="category-title">
                            {escape(title)}
                        </div>

                        <div class="category-count">
                            ● &nbsp;{escape(count)}
                        </div>

                    </div>

                </div>

            </div>
            """
        )

# ============================================================
# PREPARE ENERGY CHART DATA
# ============================================================

chart_rows = []


for row in ml_results:

    recorded_at = (
        row.get("recorded_at")
        or row.get("created_at")
        or row.get("timestamp")
    )

    actual = row.get(
        "actual_power_watts"
    )

    if actual is None:

        actual = row.get(
            "power_watts",
            0
        )


    predicted = row.get(
        "predicted_power_watts"
    )

    if predicted is None:

        predicted = row.get(
            "predicted_power",
            actual
        )


    chart_rows.append(
        {
            "Time": recorded_at,
            "Actual": number_value(
                actual
            ),
            "Predicted": number_value(
                predicted
            ),
        }
    )


if chart_rows:

    chart_df = pd.DataFrame(
        chart_rows
    )

else:

    # This is only a visual fallback when
    # the backend has no ML result records.

    dates = pd.date_range(
        end=datetime.now(),
        periods=7,
        freq="D",
    )

    chart_df = pd.DataFrame(
        {
            "Time": dates,
            "Actual": [
                17,
                22,
                20,
                29,
                34,
                23,
                18,
            ],
            "Predicted": [
                16,
                20,
                22,
                24,
                27,
                25,
                29,
            ],
        }
    )


# Keep only useful values.

chart_df = chart_df[
    [
        "Time",
        "Actual",
        "Predicted",
    ]
]


# Limit the chart to the most recent
# 30 records so the dashboard stays compact.

if len(chart_df) > 30:

    chart_df = chart_df.tail(30)


# ============================================================
# CALCULATE ANOMALIES
# ============================================================

anomaly_count = 0


for row in ml_results:

    status = str(
        row.get(
            "anomaly_status",
            ""
        )
    ).lower()


    if (
        "anomaly" in status
        or "abnormal" in status
        or status == "true"
        or status == "1"
    ):

        anomaly_count += 1


# ============================================================
# BOTTOM ANALYTICS
# ============================================================

chart_col, insight_col, alert_col = st.columns(
    [1.65, 0.85, 0.85]
)

# ============================================================
# ENERGY CONSUMPTION
# ============================================================

with chart_col:

    # --------------------------------------------------------
    # Prepare chart data from ML results
    # --------------------------------------------------------

    energy_chart_df = chart_df.copy()

    if not energy_chart_df.empty:

        energy_chart_df["Actual"] = pd.to_numeric(
            energy_chart_df["Actual"],
            errors="coerce"
        )

        energy_chart_df["Predicted"] = pd.to_numeric(
            energy_chart_df["Predicted"],
            errors="coerce"
        )

        energy_chart_df = energy_chart_df.dropna(
            subset=[
                "Actual",
                "Predicted"
            ]
        )

        energy_chart_df = energy_chart_df.tail(
            30
        ).reset_index(
            drop=True
        )


    # --------------------------------------------------------
    # Interactive chart
    # --------------------------------------------------------

    if not energy_chart_df.empty:

        # ----------------------------------------------------
        # Create readable time labels
        # ----------------------------------------------------

        if "Time" in energy_chart_df.columns:

            try:

                energy_chart_df["Chart Time"] = (
                    pd.to_datetime(
                        energy_chart_df["Time"],
                        errors="coerce"
                    )
                )

            except Exception:

                energy_chart_df["Chart Time"] = (
                    energy_chart_df.index
                )

        else:

            energy_chart_df["Chart Time"] = (
                energy_chart_df.index
            )


        # ----------------------------------------------------
        # Display latest 30 readings
        # ----------------------------------------------------

        display_df = energy_chart_df.tail(
            30
        ).copy()


        # ----------------------------------------------------
        # Build Plotly figure
        # ----------------------------------------------------

        figure = go.Figure()


        figure.add_trace(
            go.Scatter(
                x=display_df["Chart Time"],
                y=display_df["Actual"],
                mode="lines+markers",
                name="Actual",
                line=dict(
                    width=2
                ),
                marker=dict(
                    size=4
                ),
                hovertemplate=(
                    "<b>Actual Energy</b><br>"
                    "%{y:.0f} W"
                    "<br>%{x}"
                    "<extra></extra>"
                )
            )
        )


        figure.add_trace(
            go.Scatter(
                x=display_df["Chart Time"],
                y=display_df["Predicted"],
                mode="lines+markers",
                name="Predicted",
                line=dict(
                    width=1.5,
                    dash="dash"
                ),
                marker=dict(
                    size=3
                ),
                hovertemplate=(
                    "<b>AI Predicted</b><br>"
                    "%{y:.0f} W"
                    "<br>%{x}"
                    "<extra></extra>"
                )
            )
        )


        # ----------------------------------------------------
        # Chart styling
        # ----------------------------------------------------

        figure.update_layout(

            height=250,

            margin=dict(
                l=45,
                r=20,
                t=20,
                b=45
            ),

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                family="Arial",
                size=10
            ),

            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),

            hovermode="x unified",

            xaxis=dict(
                title="Time",
                showgrid=False,
                zeroline=False
            ),

            yaxis=dict(
                title="Power (W)",
                showgrid=True,
                gridcolor="#14263b",
                zeroline=False
            ),

            hoverlabel=dict(
                bgcolor="#081323",
                bordercolor="#21466d",
                font=dict(
                    size=11
                )
            )
        )


        # ----------------------------------------------------
        # Display interactive chart
        # ----------------------------------------------------

        st.plotly_chart(
            figure,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "displaylogo": False,
                "scrollZoom": False,
                "responsive": True
            },
            key="home_energy_interactive_chart"
        )


        # ----------------------------------------------------
        # Small View icon
        # ----------------------------------------------------

        if st.button(
            "↗",
            key="home_energy_view_tracking",
            help="View detailed energy analysis"
        ):
            go_to_page(
                "Tracking"
            )

    else:

        render_html(
            """
            <div style="
                height:250px;
                display:flex;
                align-items:center;
                justify-content:center;
                background:#081323;
                border:1px solid #142d49;
                border-radius:12px;
                margin-top:4px;
            ">

                <div style="
                    text-align:center;
                ">

                    <div style="
                        font-size:25px;
                    ">
                        📊
                    </div>

                    <div style="
                        color:#ffffff;
                        font-size:13px;
                        font-weight:700;
                        margin-top:8px;
                    ">
                        No energy data available
                    </div>

                    <div style="
                        color:#607995;
                        font-size:9px;
                        margin-top:5px;
                    ">
                        ML prediction data will appear here
                        when the backend is connected.
                    </div>

                </div>

            </div>
            """
        )


# ============================================================
# AI INSIGHT
# ============================================================

with insight_col:

    if anomaly_count > 0:

        insight_state = "Alert"

        insight_title = (
            "Anomaly detected"
        )

        insight_text = (
            f"{anomaly_count} unusual "
            "reading(s) found."
        )

        ring_class = "alert"

    else:

        insight_state = "Normal"

        insight_title = (
            "No anomalies detected"
        )

        insight_text = (
            "AI system is monitoring "
            "your home and everything "
            "looks good."
        )

        ring_class = ""


    render_html(
        f"""
        <div class="panel">

            <div class="panel-header">

                <div class="panel-title">
                    AI Insight
                </div>

            </div>


            <div class="
                insight-ring
                {ring_class}
            ">

                {escape(insight_state)}

            </div>


            <div class="insight-text">
                {escape(insight_title)}
            </div>


            <div class="insight-subtext">
                {escape(insight_text)}
            </div>

        </div>
        """
    )


    # Small View icon

    if st.button(
        "↗",
        key="home_ai_insight_view",
        help="View AI insights"
    ):
        go_to_page("AI Insights")

# ============================================================
# RECENT ALERTS
# ============================================================

with alert_col:

    alert_message = (
        "All devices are operating normally."
    )

    alert_icon = "●"

    alert_class = "success"


    # Find a high-power device for a
    # useful real-data alert.

    high_power_device = None

    for device in devices:

        power = number_value(
            device.get(
                "power_watts",
                0
            )
        )

        if power >= 1000:

            high_power_device = device

            break


    if high_power_device:

        high_power_name = escape(
            high_power_device.get(
                "name",
                "Device"
            )
        )

        high_power_alert = (
            f"High energy usage detected "
            f"in {high_power_name}."
        )

    else:

        high_power_alert = (
            "Energy usage is within "
            "the monitored range."
        )


    room_light_alert = (
        "Room Light turned OFF automatically."
    )


    render_html(
        f"""
        <div class="panel">

            <div class="panel-header">

                <div class="panel-title">
                    Recent Alerts
                </div>

            </div>


            <div class="alert-row">

                <span class="success">
                    {escape(alert_icon)}
                </span>

                &nbsp;

                {escape(alert_message)}

                <span class="alert-time">
                    2 min ago
                </span>

            </div>


            <div class="alert-row">

                <span class="warning">
                    ▲
                </span>

                &nbsp;

                {escape(high_power_alert)}

                <span class="alert-time">
                    15 min ago
                </span>

            </div>


            <div class="alert-row">

                <span class="success">
                    ●
                </span>

                &nbsp;

                {escape(room_light_alert)}

                <span class="alert-time">
                    1 hour ago
                </span>

            </div>

        </div>
        """
    )


    # Small View All icon

    if st.button(
        "↗",
        key="home_recent_alerts_view_all",
        help="View all alerts"
    ):
        go_to_page("Alerts")

# ============================================================
# BACKEND STATUS
# ============================================================

if api_online:

    backend_status = (
        '<span class="status-online">'
        '● Backend connected'
        '</span>'
    )

else:

    backend_status = (
        '<span class="status-offline">'
        '● Backend unavailable — using dashboard fallback data'
        '</span>'
    )


render_html(
    f"""
    <div class="status-line">
        {backend_status}
    </div>
    """
)