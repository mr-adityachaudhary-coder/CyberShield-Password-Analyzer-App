# 🛡️ CyberShield – Cybersecurity Monitoring Dashboard

**CyberShield** is a modern, professional, beginner-friendly cybersecurity monitoring dashboard built with **Python**, **Streamlit**, and **Pandas**. It is inspired by Security Operations Center (SOC) interfaces, designed to help students, developers, and junior security analysts monitor login events, evaluate authentication health, and identify potential security threats.

---

## 🌟 Key Features

1. **Executive SOC Overview (Dashboard)**
   - 4 Dynamic Statistics Cards: **Total Logins**, **Successful Logins**, **Failed Logins**, and **Suspicious Activities** (calculated in real time, never hardcoded).
   - Live Threat Alert Banner: Dynamic warning/success indicators based on threat detection rules.
   - Interactive Visualizations: Authentication Outcomes (Success vs. Failed) bar chart and Activity Classification donut chart.
   - Live Stream: Quick view of recent authentication events.

2. **Authentication Log Explorer (Login Activity)**
   - 20 realistic fictional login records with timestamps, usernames, documentation IPs (RFC 5737 / RFC 1918), login status, and classification.
   - Search bar: Real-time search across usernames and IP addresses.
   - Multi-parameter filtering: Dropdown filters for **Login Status** (`All`, `Success`, `Failed`) and **Activity Classification** (`All`, `Normal`, `Suspicious`).
   - One-click CSV Export: Download filtered records for security auditing.
   - Deep Event Inspector: Detailed audit metadata for any selected record.

3. **Visual Security Analytics**
   - Authentication attempts per user (stacked success/failure breakdown).
   - Top source IP addresses and threat volume.
   - Hourly login activity timeline tracking authentication spikes.

4. **Security Operations Alert Center**
   - Active Incident Queue displaying severity levels (**HIGH**, **MEDIUM**), target usernames, source IPs, triggered heuristic rules, and plain-English threat explanations.
   - Actionable SOC mitigation recommendations (account lockout, MFA enforcement, firewall IP blocking).
   - SOC Incident Response Playbook (Standard Operating Procedure).

5. **Demo Event Simulator & Testing**
   - Interactive sidebar tool to simulate new login attempts (test brute-force or normal logins on the fly).
   - Reset button to instantly return to baseline 20 sample records.
   - Built-in automated unit test suite (`test_logic.py`).

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Install Required Packages
Open PowerShell or Command Prompt and run:
```bash
pip install -r requirements.txt