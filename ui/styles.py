"""
ui/styles.py
============
CSS kustom untuk tampilan premium aplikasi.
"""

import streamlit as st


def apply_custom_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

        /* Material Icons Class */
        .material-symbols-rounded {
          font-family: 'Material Symbols Rounded', sans-serif !important;
          font-variation-settings:
          'FILL' 1,
          'wght' 400,
          'GRAD' 0,
          'opsz' 24;
          vertical-align: middle;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: linear-gradient(135deg, #f0f4ff 0%, #f8faff 100%);
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f4c81 0%, #1a6bb5 100%);
            border-right: none;
        }
        [data-testid="stSidebar"] * {
            color: #e2e8f0 !important;
        }
        [data-testid="stSidebar"] .stRadio label {
            font-size: 1rem !important;
            font-weight: 600 !important;
            padding: 0.4rem 0 !important;
        }
        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.15) !important;
        }

        /* Section card */
        .section-card {
            background: white;
            border-radius: 16px;
            padding: 2rem 2.5rem;
            box-shadow: 0 4px 24px rgba(15,76,129,0.08);
            margin-bottom: 1.5rem;
            border: 1px solid rgba(15,76,129,0.08);
        }

        /* Metric cards */
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 1.2rem 1.5rem;
            box-shadow: 0 2px 12px rgba(15,76,129,0.1);
            border-left: 4px solid #3b82f6;
            margin-bottom: 1rem;
        }
        .metric-card h4 {
            margin: 0 0 0.3rem 0;
            color: #64748b;
            font-size: 0.85rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .metric-card p {
            margin: 0;
            color: #0f172a;
            font-size: 1.6rem;
            font-weight: 700;
        }

        /* Formula box */
        .formula-box {
            background: #f0f9ff;
            border: 1px solid #bae6fd;
            border-radius: 10px;
            padding: 1rem 1.5rem;
            font-family: 'Courier New', monospace;
            font-size: 0.92rem;
            color: #0369a1;
            margin: 0.8rem 0;
        }

        /* Step header */
        .step-header {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin-bottom: 1rem;
        }
        .step-badge {
            background: linear-gradient(135deg, #3b82f6, #0f4c81);
            color: white;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.9rem;
            flex-shrink: 0;
        }

        /* Upload area */
        [data-testid="stFileUploader"] {
            border: 2px dashed #93c5fd !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            background: #eff6ff !important;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #0f4c81);
            color: white !important;
            border-radius: 10px;
            border: none;
            padding: 0.6rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(59,130,246,0.3);
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(59,130,246,0.4);
        }

        /* Output result cards */
        .result-ringan {
            background: linear-gradient(135deg, #d1fae5, #ecfdf5);
            border: 2px solid #10b981;
            border-radius: 16px;
            padding: 2rem;
        }
        .result-sedang {
            background: linear-gradient(135deg, #fef3c7, #fffbeb);
            border: 2px solid #f59e0b;
            border-radius: 16px;
            padding: 2rem;
        }
        .result-intensif {
            background: linear-gradient(135deg, #fee2e2, #fff1f2);
            border: 2px solid #ef4444;
            border-radius: 16px;
            padding: 2rem;
        }
        .result-title {
            font-size: 1.8rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }

        /* MF table */
        .mf-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }
        .mf-table th {
            background: #1e40af;
            color: white;
            padding: 0.6rem 0.8rem;
            text-align: left;
        }
        .mf-table td {
            padding: 0.5rem 0.8rem;
            border-bottom: 1px solid #e2e8f0;
        }
        .mf-table tr:nth-child(even) td {
            background: #f8faff;
        }
        .mu-value {
            font-weight: 700;
            color: #1e40af;
        }
        .mu-zero {
            font-weight: 400;
            color: #94a3b8;
        }

        /* Expander */
        .streamlit-expanderHeader {
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            background: #f8faff !important;
            border-radius: 8px !important;
        }

        /* Divider */
        hr { border-color: #e2e8f0 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
