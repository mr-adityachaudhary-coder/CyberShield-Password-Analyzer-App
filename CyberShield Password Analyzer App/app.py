"""
=============================================================================
Project Name : CyberShield – Cybersecurity Monitoring Dashboard
Technology   : Python, Streamlit, Pandas, Plotly
Description  : A modern, professional cybersecurity SOC monitoring dashboard
               that displays authentication statistics, tracks login activity,
               and detects suspicious behavior using beginner-friendly rules.
=============================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & METADATA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CyberShield – Cybersecurity Monitoring Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS STYLING (Modern Dark SOC Aesthetic)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Application Styles */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Top CyberShield Header Banner */
    .cyber-header-container {
        background: linear-gradient(135deg, #0e1726 0%, #111e38 50%, #0d1527 100%);
        border: 1px solid #1E293B;
        border-top: 3px solid #00D2FF;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }
    .cyber-header-left {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .cyber-logo-icon {
        font-size: 2.8rem;
        background: rgba(0, 210, 255, 0.12);
        padding: 12px;
        border-radius: 12px;
        border: 1px solid rgba(0, 210, 255, 0.35);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .cyber-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.02em;
        margin: 0;
        line-height: 1.1;
    }
    .cyber-title span {
        color: #00D2FF;
        text-shadow: 0 0 15px rgba(0, 210, 255, 0.5);
    }
    .cyber-subtitle {
        color: #38BDF8;
        font-size: 1.0rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-top: 4px;
        margin-bottom: 4px;
    }
    .cyber-desc {
        color: #94A3B8;
        font-size: 0.92rem;
        margin: 0;
        max-width: 650px;
    }

    /* Live SOC Status Badge */
    .soc-status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: rgba(16, 185, 129, 0.12);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10B981;
    }

    /* Statistics Metric Cards */
    .metric-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    .metric-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
    }
    .card-blue::before { background: #38BDF8; }
    .card-green::before { background: #10B981; }
    .card-red::before { background: #EF4444; }
    .card-amber::before { background: #F59E0B; }

    .metric-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-icon {
        font-size: 1.4rem;
        opacity: 0.9;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1;
        margin-bottom: 6px;
    }
    .val-blue { color: #38BDF8; }
    .val-green { color: #10B981; }
    .val-red { color: #EF4444; }
    .val-amber { color: #F59E0B; }
    .metric-subtext {
        font-size: 0.78rem;
        color: #64748B;
        font-weight: 500;
    }

    /* Content Cards */
    .content-card {
        background-color: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }
    .content-card-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 1px solid #1F2937;
        padding-bottom: 10px;
    }

    /* Alert Banner Custom Styles */
    .alert-banner-warning {
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.15) 0%, rgba(245, 158, 11, 0.1) 100%);
        border: 1px solid rgba(239, 68, 68, 0.45);
        border-left: 5px solid #EF4444;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .alert-banner-success {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%);
        border: 1px solid rgba(16, 185, 129, 0.45);
        border-left: 5px solid #10B981;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .alert-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 2px;
    }
    .alert-desc {
        font-size: 0.88rem;
        color: #CBD5E1;
        margin: 0;
    }

    /* Threat Item Card */
    .threat-card {
        background: #151E32;
        border: 1px solid #233352;
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 12px;
        border-left: 4px solid #EF4444;
    }
    .threat-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .threat-badge-high {
        background: rgba(239, 68, 68, 0.2);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 2px 10px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .threat-badge-medium {
        background: rgba(245, 158, 11, 0.2);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 2px 10px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .threat-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #F1F5F9;
    }
    .threat-meta {
        font-size: 0.82rem;
        color: #94A3B8;
        margin-bottom: 6px;
    }
    .threat-action {
        font-size: 0.82rem;
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.08);
        padding: 6px 10px;
        border-radius: 6px;
        border-left: 3px solid #38BDF8;
    }

    /* Disclaimer box */
    .demo-disclaimer {
        background: rgba(30, 41, 59, 0.5);
        border: 1px dashed #334155;
        border-radius: 8px;
        padding: 12px 16px;
        color: #94A3B8;
        font-size: 0.82rem;
        line-height: 1.5;
        margin-top: 20px;
    }

    /* Streamlit DataFrame & Input dark styling enhancements */
    div[data-testid="stDataFrame"] {
        border-radius: 8px;
        border: 1px solid #1F2937;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 3. SAMPLE DATA GENERATION (20 Fictional Records)
# -----------------------------------------------------------------------------
def get_initial_sample_records() -> pd.DataFrame:
    """
    Generates 20 fictional login records for demonstration purposes.
    Uses RFC 5737 (198.51.100.x, 203.0.113.x, 192.0.2.x) documentation IP ranges
    and RFC 1918 private IP ranges to ensure safe, ethical simulation.
    """
    records = [
        {"Timestamp": "2026-10-19 08:14:22", "Username": "admin", "IP Address": "198.51.100.89", "Login Status": "Failed", "Activity Classification": "Suspicious"},
        {"Timestamp": "2026-10-19 08:14:48", "Username": "admin", "IP Address": "198.51.100.89", "Login Status": "Failed", "Activity Classification": "Suspicious"},
        {"Timestamp": "2026-10-19 08:15:15", "Username": "admin", "IP Address": "198.51.100.89", "Login Status": "Failed", "Activity Classification": "Suspicious"},
        {"Timestamp": "2026-10-19 08:30:10", "Username": "sarah.dev", "IP Address": "192.168.1.45", "Login Status": "Success", "Activity Classification": "Normal"},
        {"Timestamp": "2026-10-19 08:45:00", "Username": "alex.ops", "IP Address": "10.0.4.12", "Login Status": "Success", "Activity Classification": "Normal"},
        {"Timestamp": "2026-10-19 09:02:18", "Username": "john.sales", "IP Address": "192.168.1.105", "Login Status": "Success", "Activity Classification": "Normal"},
        {"Timestamp": "2026-10-19 09:15:33", "Username": "finance_mgr", "IP Address": "203.0.113.99", "Login Status": "Failed", "Activity Classification": "Suspicious"},
        {"Timestamp": "2026-10-19 09:20:05", "Username": "chen.qa", "IP Address": "192.168.1.88", "Login Status": "Success", "Activity Classification": "Normal"},
        {"Timestamp": "2026-10-19 09:45:50", "Username": "maria.hr", "IP Address": "192.168.1.112", "Login Status": "Failed", "Activity Classification": "Normal"},
        {"Timestamp": "2026-10-19 09:46:35", "Username": "maria.hr", "IP Address": "192.168.1.112", "Login Status": "Success", "Activity Classification": "Normal"},
        {"Timestamp": "2026-10-19 10:10:14", "Username": "guest_user", "IP Address": "198.51.100.110", "Login Status": "Failed", "Activity Classification": "Suspicious"},
        {"Timestamp": "2026-10-19 10:30:22", "Username": "sec_audit", "IP Address": "10.0.1.5", "Login Status": "Success", "Activity Classification": "Normal"},
        {"Timestamp": "2026-10-19 11:05:40", "Username": "backup_svc", "IP Address": "10.0.2.20", "Login Status": "Success", "Activity Classification": "Normal"},
        {"Timestamp": "2026-10-19 11:42:19", "Username": "david.marketing", "IP Address": "192.168.1.140", "Login Status": "Success", "Activity Classification": "Normal"},
        {"Timestamp": "2026-10-19 12:15:02", "Username": "sarah.dev", "IP Address": "192.168.1.45", "Login Status": "Success", "Activity Classification": "Normal"},
        {"Timestamp": "2026-10-19 12:50:44", "Username": "alex.ops", "IP Address": "10.0.4.12", "Login Status": "Success", "Activity Classification": "Normal"},
        {"Timestamp": "2026-10-19 13:18:29", "Username": "root_service", "IP Address": "203.0.113.220", "Login Status": "Failed", "Activity Classification": "Suspicious"},
        {"Timestamp": "2026-10-19 13:45:10", "Username": "emily.design", "IP Address": "192.168.1.162", "Login Status": "Success", "Activity Classification": "Normal"},
        {"Timestamp": "2026-10-19 14:10:55", "Username": "john.sales", "IP Address": "192.168.1.105", "Login Status": "Success", "Activity Classification": "Normal"},
        {"Timestamp": "2026-10-19 14:35:12", "Username": "alex.ops", "IP Address": "10.0.4.12", "Login Status": "Success", "Activity Classification": "Normal"}
    ]
    return pd.DataFrame(records)

# Initialize Session State so user modifications or simulations persist
if "login_data" not in st.session_state:
    st.session_state.login_data = get_initial_sample_records()


# -----------------------------------------------------------------------------
# 4. SUSPICIOUS ACTIVITY DETECTION ENGINE & METRICS
# -----------------------------------------------------------------------------
def calculate_metrics(df: pd.DataFrame) -> dict:
    """
    Calculates summary login statistics dynamically from the dataframe.
    Never hardcoded to guarantee responsive updates.
    """
    total_logins = len(df)
    successful_logins = int((df["Login Status"] == "Success").sum()) if total_logins > 0 else 0
    failed_logins = int((df["Login Status"] == "Failed").sum()) if total_logins > 0 else 0
    suspicious_activities = int((df["Activity Classification"] == "Suspicious").sum()) if total_logins > 0 else 0
    success_rate = round((successful_logins / total_logins * 100), 1) if total_logins > 0 else 0.0

    return {
        "total_logins": total_logins,
        "successful_logins": successful_logins,
        "failed_logins": failed_logins,
        "suspicious_activities": suspicious_activities,
        "success_rate": success_rate
    }

def analyze_security_threats(df: pd.DataFrame) -> list:
    """
    Simple, beginner-friendly detection rules:
    Rule 1: Flag repeated failed logins by the same user (potential brute force).
    Rule 2: Flag records explicitly marked as suspicious (e.g. untrusted IP / unauthorized target).
    Rule 3: Flag high failure rate from identical IP address.
    """
    threats = []

    if df.empty:
        return threats

    # Rule 1: Repeated failed logins by username
    failed_df = df[df["Login Status"] == "Failed"]
    fail_counts = failed_df["Username"].value_counts()
    for user, count in fail_counts.items():
        if count >= 2:
            user_records = failed_df[failed_df["Username"] == user]
            ips = ", ".join(user_records["IP Address"].unique())
            threats.append({
                "severity": "High" if count >= 3 else "Medium",
                "title": f"Repeated Failed Logins ({count} attempts)",
                "user": user,
                "ip": ips,
                "rule": "Rule 1: Potential Brute-Force / Password Spraying",
                "description": f"User '{user}' incurred {count} failed authentication events from IP(s) {ips}.",
                "recommendation": "Initiate temporary account lockout, enforce Multi-Factor Authentication (MFA), and verify source IP."
            })

    # Rule 2: Explicitly marked suspicious records
    suspicious_df = df[df["Activity Classification"] == "Suspicious"]
    for _, row in suspicious_df.iterrows():
        # Avoid duplicate warning if already covered under repeated failed logins for the exact same user
        if row["Username"] in fail_counts and fail_counts[row["Username"]] >= 2:
            continue
        threats.append({
            "severity": "Medium",
            "title": f"Flagged Suspicious Event ({row['Username']})",
            "user": row["Username"],
            "ip": row["IP Address"],
            "rule": "Rule 2: Anomalous Authentication / Untrusted Source",
            "description": f"Login event for '{row['Username']}' at {row['Timestamp']} flagged as suspicious from IP {row['IP Address']}.",
            "recommendation": "Review IP reputation, check VPN/proxy exit status, and confirm user's physical location."
        })

    return threats


# -----------------------------------------------------------------------------
# 5. HEADER COMPONENT
# -----------------------------------------------------------------------------
def render_header():
    """Renders the top SOC dashboard header with title, subtitle, and live badge."""
    st.markdown("""
    <div class="cyber-header-container">
        <div class="cyber-header-left">
            <div class="cyber-logo-icon">🛡️</div>
            <div>
                <h1 class="cyber-title">Cyber<span>Shield</span></h1>
                <div class="cyber-subtitle">Cybersecurity Monitoring Dashboard</div>
                <p class="cyber-desc">
                    Monitor login activity, analyze authentication events, and identify potential security threats.
                </p>
            </div>
        </div>
        <div>
            <div class="soc-status-badge">
                <div class="pulse-dot"></div>
                SOC ENGINE ACTIVE • SIMULATION MODE
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. SIDEBAR NAVIGATION & CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 16px 0;">
        <span style="font-size: 2.5rem;">🛡️</span>
        <h2 style="color: #00D2FF; margin: 4px 0 0 0; font-size: 1.4rem; font-weight: 800;">CyberShield</h2>
        <p style="color: #64748B; font-size: 0.8rem; margin: 0;">SOC Monitoring v1.0</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧭 Navigation")
    nav_selection = st.radio(
        label="Select Dashboard View",
        options=[
            "📊 Dashboard",
            "📋 Login Activity",
            "📈 Security Analytics",
            "🚨 Security Alerts",
            "ℹ️ About CyberShield"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 🧪 Demo Event Simulator")
    st.caption("Inject a simulated login attempt to test detection rules in real time:")

    with st.expander("➕ Add Simulated Login"):
        new_user = st.text_input("Username", value="temp.contractor", max_chars=25)
        new_ip = st.text_input("Source IP", value="198.51.100.250", max_chars=20)
        new_status = st.selectbox("Login Status", ["Success", "Failed"], index=1)
        new_class = st.selectbox("Activity Type", ["Normal", "Suspicious"], index=1)

        if st.button("🚀 Log Event to Dashboard", use_container_width=True):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame([{
                "Timestamp": current_time,
                "Username": new_user.strip() or "anonymous",
                "IP Address": new_ip.strip() or "192.0.2.1",
                "Login Status": new_status,
                "Activity Classification": new_class
            }])
            st.session_state.login_data = pd.concat([new_row, st.session_state.login_data], ignore_index=True)
            st.success(f"Event recorded for {new_user}!")
            st.rerun()

    if st.button("🔄 Reset to Default 20 Records", use_container_width=True):
        st.session_state.login_data = get_initial_sample_records()
        st.info("Sample dataset reset to default 20 records.")
        st.rerun()

    st.markdown("""
    <div class="demo-disclaimer">
        🔒 <strong>Fictional Demo Environment</strong><br>
        All records and IP addresses utilize documentation ranges (RFC 5737 / RFC 1918) for academic demonstration.
    </div>
    """, unsafe_allow_html=True)


# Always render the shared header
render_header()

# Access current data and compute live metrics
current_df = st.session_state.login_data
metrics = calculate_metrics(current_df)
detected_threats = analyze_security_threats(current_df)


# -----------------------------------------------------------------------------
# 7. VIEW 1: DASHBOARD (Overview)
# -----------------------------------------------------------------------------
if nav_selection == "📊 Dashboard":
    st.markdown("### 📌 Executive Security Overview")

    # Four Dynamic Statistics Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card card-blue">
            <div class="metric-header">
                <span class="metric-label">Total Logins</span>
                <span class="metric-icon">📋</span>
            </div>
            <div class="metric-value val-blue">{metrics['total_logins']}</div>
            <div class="metric-subtext">Total authenticated attempts</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card card-green">
            <div class="metric-header">
                <span class="metric-label">Successful Logins</span>
                <span class="metric-icon">✅</span>
            </div>
            <div class="metric-value val-green">{metrics['successful_logins']}</div>
            <div class="metric-subtext">{metrics['success_rate']}% authentication rate</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card card-red">
            <div class="metric-header">
                <span class="metric-label">Failed Logins</span>
                <span class="metric-icon">❌</span>
            </div>
            <div class="metric-value val-red">{metrics['failed_logins']}</div>
            <div class="metric-subtext">Rejected credentials</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card card-amber">
            <div class="metric-header">
                <span class="metric-label">Suspicious Activities</span>
                <span class="metric-icon">⚠️</span>
            </div>
            <div class="metric-value val-amber">{metrics['suspicious_activities']}</div>
            <div class="metric-subtext">Flagged for SOC review</div>
        </div>
        """, unsafe_allow_html=True)

    # Security Alert Status Banner
    if metrics["suspicious_activities"] > 0:
        st.markdown(f"""
        <div class="alert-banner-warning">
            <div style="font-size: 2rem;">🚨</div>
            <div>
                <div class="alert-title" style="color: #F87171;">SECURITY ALERT: {metrics['suspicious_activities']} Suspicious Activities Detected!</div>
                <p class="alert-desc">
                    {metrics['failed_logins']} failed login events recorded. One or more detection rules triggered. Please inspect the <strong>Security Alerts</strong> tab immediately.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-banner-success">
            <div style="font-size: 2rem;">🛡️</div>
            <div>
                <div class="alert-title" style="color: #34D399;">ALL SYSTEMS NORMAL: No Suspicious Activities Detected</div>
                <p class="alert-desc">
                    All processed login attempts adhere to baseline security policies. Zero anomalies found in current monitoring window.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Visual Analytics Row
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="content-card-header">📊 Authentication Outcomes</div>', unsafe_allow_html=True)

        outcome_df = pd.DataFrame({
            "Outcome": ["Successful", "Failed"],
            "Count": [metrics["successful_logins"], metrics["failed_logins"]],
            "Color": ["#10B981", "#EF4444"]
        })

        fig_bar = px.bar(
            outcome_df,
            x="Outcome",
            y="Count",
            color="Outcome",
            color_discrete_map={"Successful": "#10B981", "Failed": "#EF4444"},
            text="Count"
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0"),
            showlegend=False,
            height=280,
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(gridcolor="#1F2937", zeroline=False),
            xaxis=dict(gridcolor="#1F2937")
        )
        fig_bar.update_traces(textposition='outside', marker=dict(line=dict(width=1, color="#374151")))
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="content-card-header">🛡️ Activity Classification Breakdown</div>', unsafe_allow_html=True)

        class_counts = current_df["Activity Classification"].value_counts().reset_index()
        class_counts.columns = ["Classification", "Count"]

        fig_pie = px.pie(
            class_counts,
            values="Count",
            names="Classification",
            color="Classification",
            color_discrete_map={"Normal": "#38BDF8", "Suspicious": "#EF4444"},
            hole=0.55
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0"),
            height=280,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recent Events Quick Table
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="content-card-header">⚡ Recent Authentication Events (Live Stream)</div>', unsafe_allow_html=True)
    recent_events = current_df.head(6)

    st.dataframe(
        recent_events,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Timestamp": st.column_config.TextColumn("Timestamp 🕒", width="medium"),
            "Username": st.column_config.TextColumn("User Account 👤", width="medium"),
            "IP Address": st.column_config.TextColumn("Source IP 🌐", width="medium"),
            "Login Status": st.column_config.TextColumn("Status 🔑", width="small"),
            "Activity Classification": st.column_config.TextColumn("Classification 🛡️", width="medium"),
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 8. VIEW 2: LOGIN ACTIVITY (Filterable & Searchable Table)
# -----------------------------------------------------------------------------
elif nav_selection == "📋 Login Activity":
    st.markdown("### 📋 Authentication Log Explorer")
    st.caption("Filter, search, inspect, and export all recorded login attempts.")

    # Filter Controls Row
    f_col1, f_col2, f_col3 = st.columns([1.5, 1, 1])

    with f_col1:
        search_query = st.text_input(
            "🔍 Search Records",
            placeholder="Search by username or IP address...",
            help="Filter rows containing this keyword in Username or IP Address"
        )

    with f_col2:
        status_filter = st.selectbox(
            "🔑 Filter by Login Status",
            options=["All", "Success", "Failed"],
            index=0
        )

    with f_col3:
        class_filter = st.selectbox(
            "🛡️ Filter by Classification",
            options=["All", "Normal", "Suspicious"],
            index=0
        )

    # Apply Filters Dynamically
    filtered_df = current_df.copy()

    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Login Status"] == status_filter]

    if class_filter != "All":
        filtered_df = filtered_df[filtered_df["Activity Classification"] == class_filter]

    if search_query:
        query = search_query.lower().strip()
        filtered_df = filtered_df[
            filtered_df["Username"].str.lower().str.contains(query) |
            filtered_df["IP Address"].str.lower().str.contains(query)
        ]

    # Quick Count Display
    st.markdown(f"**Showing {len(filtered_df)} of {len(current_df)} total records**")

    # Table Display Card
    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    if filtered_df.empty:
        st.warning("⚠️ No login records match your active search and filter criteria.")
    else:
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Timestamp": st.column_config.TextColumn("Timestamp 🕒", width="medium"),
                "Username": st.column_config.TextColumn("Username 👤", width="medium"),
                "IP Address": st.column_config.TextColumn("IP Address 🌐", width="medium"),
                "Login Status": st.column_config.TextColumn("Login Status 🔑", width="small"),
                "Activity Classification": st.column_config.TextColumn("Classification 🛡️", width="medium")
            }
        )

    # Download CSV Action
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Log (CSV)",
        data=csv_bytes,
        file_name="cybershield_login_activity.csv",
        mime="text/csv",
        help="Download the currently filtered records as a CSV file for auditing."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Deep Event Inspection Helper
    with st.expander("🔎 Deep Event Inspector"):
        selected_index = st.selectbox(
            "Select Record to Inspect Metadata:",
            options=range(len(filtered_df)) if not filtered_df.empty else [],
            format_func=lambda i: f"#{i+1} | {filtered_df.iloc[i]['Timestamp']} | {filtered_df.iloc[i]['Username']} ({filtered_df.iloc[i]['Login Status']})"
        )
        if not filtered_df.empty:
            sel_row = filtered_df.iloc[selected_index]
            meta_c1, meta_c2, meta_c3 = st.columns(3)
            with meta_c1:
                st.markdown(f"**Target Account:** `{sel_row['Username']}`")
                st.markdown(f"**Authentication Time:** `{sel_row['Timestamp']}`")
            with meta_c2:
                st.markdown(f"**Origin IP Address:** `{sel_row['IP Address']}`")
                st.markdown(f"**Protocol:** `TLS v1.3 / HTTPS (Port 443)`")
            with meta_c3:
                status_color = "green" if sel_row['Login Status'] == "Success" else "red"
                st.markdown(f"**Result:** :{status_color}[{sel_row['Login Status']}]")
                class_color = "red" if sel_row['Activity Classification'] == "Suspicious" else "blue"
                st.markdown(f"**Audit Tag:** :{class_color}[{sel_row['Activity Classification']}]")


# -----------------------------------------------------------------------------
# 9. VIEW 3: SECURITY ANALYTICS (Charts & Trend Analysis)
# -----------------------------------------------------------------------------
elif nav_selection == "📈 Security Analytics":
    st.markdown("### 📈 Visual Security Analytics & Threat Patterns")
    st.caption("Detailed statistical distributions and login activity behavior over time.")

    # Row 1: Logins by User & Activity by Time
    a_col1, a_col2 = st.columns(2)

    with a_col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="content-card-header">👥 Authentication Attempts per User</div>', unsafe_allow_html=True)

        user_summary = current_df.groupby(["Username", "Login Status"]).size().reset_index(name="Attempts")
        fig_user = px.bar(
            user_summary,
            x="Username",
            y="Attempts",
            color="Login Status",
            color_discrete_map={"Success": "#10B981", "Failed": "#EF4444"},
            barmode="stack"
        )
        fig_user.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0"),
            height=320,
            margin=dict(l=20, r=20, t=20, b=30),
            xaxis=dict(gridcolor="#1F2937", tickangle=-30),
            yaxis=dict(gridcolor="#1F2937")
        )
        st.plotly_chart(fig_user, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with a_col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="content-card-header">🌐 Top Source IP Addresses</div>', unsafe_allow_html=True)

        ip_summary = current_df.groupby(["IP Address", "Activity Classification"]).size().reset_index(name="Volume")
        fig_ip = px.bar(
            ip_summary,
            x="Volume",
            y="IP Address",
            orientation="h",
            color="Activity Classification",
            color_discrete_map={"Normal": "#38BDF8", "Suspicious": "#EF4444"}
        )
        fig_ip.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0"),
            height=320,
            margin=dict(l=20, r=20, t=20, b=30),
            xaxis=dict(gridcolor="#1F2937"),
            yaxis=dict(gridcolor="#1F2937")
        )
        st.plotly_chart(fig_ip, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Row 2: Hourly Activity Timeline
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="content-card-header">⏱️ Login Activity Timeline</div>', unsafe_allow_html=True)

    timeline_df = current_df.copy()
    timeline_df["Hour"] = pd.to_datetime(timeline_df["Timestamp"]).dt.strftime("%H:00")
    hourly_counts = timeline_df.groupby(["Hour", "Login Status"]).size().reset_index(name="Count")

    fig_time = px.line(
        hourly_counts,
        x="Hour",
        y="Count",
        color="Login Status",
        markers=True,
        color_discrete_map={"Success": "#10B981", "Failed": "#EF4444"}
    )
    fig_time.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0"),
        height=300,
        margin=dict(l=20, r=20, t=20, b=30),
        xaxis=dict(gridcolor="#1F2937", title="Hour of Day"),
        yaxis=dict(gridcolor="#1F2937", title="Number of Logins")
    )
    st.plotly_chart(fig_time, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 10. VIEW 4: SECURITY ALERTS (Threat Center & Mitigations)
# -----------------------------------------------------------------------------
elif nav_selection == "🚨 Security Alerts":
    st.markdown("### 🚨 Security Operations Alert Center")
    st.caption("Active incident alerts, triggered heuristic rules, and triage response recommendations.")

    # Alert Count Metrics
    m_col1, m_col2, m_col3 = st.columns(3)

    with m_col1:
        st.markdown(f"""
        <div class="metric-card card-amber">
            <div class="metric-header">
                <span class="metric-label">Suspicious Activities</span>
                <span class="metric-icon">⚠️</span>
            </div>
            <div class="metric-value val-amber">{metrics['suspicious_activities']}</div>
            <div class="metric-subtext">Events requiring triage</div>
        </div>
        """, unsafe_allow_html=True)

    with m_col2:
        st.markdown(f"""
        <div class="metric-card card-red">
            <div class="metric-header">
                <span class="metric-label">Failed Logins</span>
                <span class="metric-icon">❌</span>
            </div>
            <div class="metric-value val-red">{metrics['failed_logins']}</div>
            <div class="metric-subtext">Total authentication rejections</div>
        </div>
        """, unsafe_allow_html=True)

    with m_col3:
        status_color = "val-red" if metrics['suspicious_activities'] > 0 else "val-green"
        status_text = "ELEVATED" if metrics['suspicious_activities'] > 0 else "NORMAL"
        card_class = "card-red" if metrics['suspicious_activities'] > 0 else "card-green"
        st.markdown(f"""
        <div class="metric-card {card_class}">
            <div class="metric-header">
                <span class="metric-label">Threat Level</span>
                <span class="metric-icon">📡</span>
            </div>
            <div class="metric-value {status_color}">{status_text}</div>
            <div class="metric-subtext">Heuristic rule evaluation</div>
        </div>
        """, unsafe_allow_html=True)

    # Status Banner: Warning or Success
    if metrics["suspicious_activities"] > 0:
        st.markdown(f"""
        <div class="alert-banner-warning">
            <div style="font-size: 2.2rem;">⚠️</div>
            <div>
                <div class="alert-title" style="color: #F87171;">
                    SECURITY WARNING: {metrics['suspicious_activities']} Suspicious Records Detected!
                </div>
                <p class="alert-desc">
                    Active anomalies detected in authentication traffic. {metrics['failed_logins']} failed login events logged. Review the threat incident queue below.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-banner-success">
            <div style="font-size: 2.2rem;">✅</div>
            <div>
                <div class="alert-title" style="color: #34D399;">
                    ALL CLEAR: Zero Suspicious Records Detected
                </div>
                <p class="alert-desc">
                    No active threat alerts. All login events match standard user profiles and known internal IP ranges.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Detailed Threat Alert Feed
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="content-card-header">⚡ Active Incident Queue</div>', unsafe_allow_html=True)

    if detected_threats:
        for threat in detected_threats:
            badge_class = "threat-badge-high" if threat["severity"] == "High" else "threat-badge-medium"
            st.markdown(f"""
            <div class="threat-card">
                <div class="threat-header">
                    <span class="threat-title">{threat['title']}</span>
                    <span class="{badge_class}">{threat['severity']} SEVERITY</span>
                </div>
                <div class="threat-meta">
                    👤 <strong>Target:</strong> <code>{threat['user']}</code> &nbsp;|&nbsp;
                    🌐 <strong>Origin IP:</strong> <code>{threat['ip']}</code> &nbsp;|&nbsp;
                    🛡️ <strong>Trigger:</strong> {threat['rule']}
                </div>
                <p style="color: #CBD5E1; font-size: 0.86rem; margin: 6px 0 10px 0;">{threat['description']}</p>
                <div class="threat-action">
                    🛠️ <strong>Recommended Action:</strong> {threat['recommendation']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No active incidents found in the queue.")

    st.markdown('</div>', unsafe_allow_html=True)

    # SOC Response Playbook
    with st.expander("🛡️ SOC Incident Response Playbook (Standard Operating Procedure)"):
        st.markdown("""
        1. **Triage & Correlate:** Cross-reference source IP addresses with threat intelligence feeds.
        2. **Account Isolation:** If failed attempts exceed threshold, invoke automated temporary account lockout.
        3. **MFA Re-challenge:** Force password reset and MFA prompt on subsequent authentication.
        4. **Firewall Drop Rule:** Apply edge firewall / WAF ban for persistent aggressive IP blocks.
        5. **Incident Documentation:** Record timestamp, hashes, and indicators of compromise (IOCs) in the SOC ticketing system.
        """)


# -----------------------------------------------------------------------------
# 11. VIEW 5: ABOUT CYBERSHIELD
# -----------------------------------------------------------------------------
elif nav_selection == "ℹ️ About CyberShield":
    st.markdown("### ℹ️ About CyberShield")

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="content-card-header">🛡️ Project Mission & Overview</div>', unsafe_allow_html=True)
    st.markdown("""
    **CyberShield** is a beginner-friendly cybersecurity monitoring dashboard designed to help students, developers,
    and junior security analysts visualize authentication traffic, understand SOC monitoring workflows, and detect suspicious login behaviors.

    ### 🎯 Why Authentication Monitoring Matters
    Authentication logs are the first line of defense in cyber defense operations:
    - **Brute Force Attacks:** Automated scripts repeatedly guessing passwords for administrative accounts.
    - **Credential Stuffing:** Attackers testing stolen lists of usernames and passwords across services.
    - **Anomalous Access:** Legitimate credentials utilized from unusual geographic locations or untrusted subnets.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="content-card-header">⚙️ Suspicious Activity Detection Rules</div>', unsafe_allow_html=True)
    st.markdown("""
    The dashboard implements demonstrative heuristic rules to flag potential security threats:
    - **Rule 1 (Repeated Failed Logins):** Flags any user account with 2 or more failed login attempts in the dataset. Accounts with 3+ attempts are escalated to **High Severity** (Brute-Force pattern).
    - **Rule 2 (Flagged Suspicious Activity):** Flags records explicitly classified as suspicious due to unauthorized IP origin, abnormal access hours, or privileged user probing.
    - **Rule 3 (High Failure Rate Threshold):** Tracks overall failure percentage and alerts SOC operators when failed logins exceed safe operational baselines.

    > **⚠️ Academic Demonstration Disclaimer:** These rules are designed for educational demonstrations and college mini-projects.
    > They illustrate core SIEM/SOC concepts but do not replace production-grade Intrusion Detection Systems (IDS) or Security Information & Event Management (SIEM) platforms.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="content-card-header">💻 Technical Architecture & Stack</div>', unsafe_allow_html=True)
    st.markdown("""
    - **Core Language:** Python 3
    - **Web Framework:** [Streamlit](https://streamlit.io/)
    - **Data Processing:** [Pandas](https://pandas.pydata.org/)
    - **Interactive Visualizations:** [Plotly Express & Graph Objects](https://plotly.com/python/)
    - **Styling:** Custom CSS with SOC dark navy aesthetic and responsive layout
    - **Network Safety:** Strictly utilizes RFC 5737 (`198.51.100.x`, `203.0.113.x`) and RFC 1918 private ranges.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="content-card-header">🎓 College Mini-Project Presentation Guide</div>', unsafe_allow_html=True)
    st.markdown("""
    When presenting CyberShield for your viva or project review, emphasize these key points:
    1. **Real-time Metrics:** Point out how Total Logins, Successes, Failures, and Suspicious events are computed dynamically from data frames.
    2. **Threat Demonstration:** Show the 3 failed attempts on `admin` by `198.51.100.89` and explain how Rule 1 caught the brute-force pattern.
    3. **Interactive Simulation:** Use the sidebar **"Demo Event Simulator"** to inject a live failed event and demonstrate how the dashboard reacts dynamically!
    4. **SOC Analyst Workflow:** Walk through the triage tabs from **Dashboard** -> **Login Activity** -> **Security Alerts**.
    """)
    st.markdown('</div>', unsafe_allow_html=True)