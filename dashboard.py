import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 1. ตั้งค่าหน้าจอ (Wide Mode)
st.set_page_config(
    page_title="CHELA Blockchain Explorer",
    page_icon="🟡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ระบบ Auto-refresh (รีเฟรชหน้าเว็บทุกๆ 10 วินาที เพื่อดึงข้อมูลใหม่จาก SSD)
st_autorefresh(interval=10000, key="datarefresh")

# 3. กำหนดที่อยู่ไฟล์ข้อมูลใน SSD
# หมายเหตุ: ท่านประธานต้องมั่นใจว่า Mount SSD ไว้ที่ Path นี้แล้ว
DATA_PATH = "/media/mrnong/28e53eb6-2e49-4ad2-b2e1-f1c490db73b1/transactions.csv"

# 4. ฟังก์ชันสำหรับโหลดข้อมูลจาก SSD
def load_blockchain_data():
    if os.path.exists(DATA_PATH):
        try:
            df = pd.read_csv(DATA_PATH)
            return df
        except Exception as e:
            return pd.DataFrame({"Error": [f"อ่านไฟล์ไม่ได้: {e}"]})
    else:
        # ถ้ายังไม่มีไฟล์ ให้สร้างข้อมูลจำลองไว้ดูแก้ขัดก่อน
        dummy_data = {
            "Txn Hash": ["0x7a1b...3e4f", "0x9c2d...1a2b", "0x3e4f...9c2d"],
            "Method": ["Transfer", "Mint", "Stake"],
            "Block": [4829102, 4829101, 4829100],
            "From": ["0x2eeb...087c", "0x0000...0000", "0x5a1b...2c3d"],
            "Amount": ["50,000 CHLA", "1,000,000 CHLA", "25,000 CHLA"]
        }
        return pd.DataFrame(dummy_data)

# 5. ใส่ CSS ตกแต่ง (Binance Dark & Gold Theme)
st.markdown("""
    <style>
    /* พื้นหลังหลัก */
    .main { background-color: #0b0e11; color: #eaecef; }
    
    /* การตกแต่งการ์ด Metric */
    div[data-testid="stMetric"] {
        background-color: #1e2329;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #f3ba2f;
    }
    
    /* สีของตัวเลข Metric */
    div[data-testid="stMetricValue"] { color: #f3ba2f !important; font-family: 'Monaco', monospace; }
    
    /* ปรับแต่งตาราง */
    .stTable { background-color: #1e2329; border-radius: 10px; }
    
    /* หัวข้อ */
    h1, h2, h3 { color: #f3ba2f !important; font-weight: 700; }
    
    /* ปุ่มต่างๆ */
    .stButton>button {
        background-color: #f3ba2f;
        color: black;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ส่วนหัว (Header) ---
st.title("🟡 CHELA MAINNET EXPLORER")
st.caption(f"Network Status: Online | Local Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- แถบตัวเลข (Top Metrics) ---
# ในอนาคตสามารถเขียนโค้ดให้คำนวณจากไฟล์ CSV ได้เลย
tx_df = load_blockchain_data()
total_tx = len(tx_df) if 'Txn Hash' in tx_df.columns else 0
latest_block = tx_df['Block'].max() if 'Block' in tx_df.columns else "N/A"

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="Latest Block", value=f"{latest_block:,}" if isinstance(latest_block, int) else latest_block, delta="Live")
with m2:
    st.metric(label="Total Transactions", value=f"{total_tx:,}", delta="+New")
with m3:
    st.metric(label="Active Nodes", value="128", delta="Stable")
with m4:
    st.metric(label="CHELA Price", value="$0.00045", delta="+5.2%")

st.markdown("---")

# --- ส่วนเนื้อหาหลัก (Main Content) ---
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("⛓️ Recent Transactions (Live from SSD)")
    # แสดงตารางข้อมูลที่โหลดมาจาก CSV
    st.dataframe(tx_df, use_container_width=True, hide_index=True)
    
    if st.button("Manual Refresh Data"):
        st.rerun()

with right_col:
    st.subheader("📊 Tokenomics & Status")
    
    # กราฟแสดงสัดส่วนการใช้เหรียญ
    token_stats = pd.DataFrame({
        "Type": ["Circulating", "Staked", "Burned"],
        "Percent": [70, 20, 10]
    })
    st.bar_chart(token_stats.set_index("Type"))
    
    st.success(f"**Contract Address:**\n0x527FC4D50AC7bF9Cd1B608EDEeB09D53A15Cc64")
    
    with st.expander("Storage Info"):
        st.write(f"Reading from: `{DATA_PATH}`")
        st.write(f"File Status: {'✅ Found' if os.path.exists(DATA_PATH) else '❌ Not Found'}")

# --- ส่วนท้าย (Footer) ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #848e9c;'>© 2026 CHELA Blockchain Network | Layer-2 Solutions</p>", unsafe_allow_html=True)
