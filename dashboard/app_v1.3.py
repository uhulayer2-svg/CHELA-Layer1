import streamlit as st
from web3 import Web3
import os
import time
from dotenv import load_dotenv

# ====================== CONFIG & INIT ======================
load_dotenv()
st.set_page_config(page_title="CHLA Scan - Ultimate Partner Dashboard", page_icon="🌐", layout="wide")

# เชื่อมต่อเครื่อง X99 (บล็อกเชนความเร็ว 500ms ของท่านประธาน)
RPC_URL = "http://127.0.0.1:9944"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

ALITH_WALLET = "0xf24FF3a9CF04c71Dbc94D0b566f7A27B94566cac"

# ====================== CSS: CLASSIC LIGHT & PARTNER FOCUS ======================
st.markdown("""
<style>
    .stApp {background-color: #f8f9fa; font-family: 'Inter', Helvetica, Arial, sans-serif;}
    #MainMenu {visibility: hidden;} header {visibility: hidden;}
    .block-container {padding-top: 0.5rem; max-width: 1350px;}
    
    /* Partner Bar 2 ชั้น (ไทย/ต่างประเทศ) */
    .partner-section {
        background: white; border-bottom: 1px solid #e7eaf3; padding: 10px 20px; margin-bottom: 20px;
    }
    .partner-row { display: flex; align-items: center; gap: 15px; margin-bottom: 5px; font-size: 12px; }
    .partner-tag { color: #6c757d; font-weight: 700; min-width: 80px; }
    .partner-links a { color: #0784c3; text-decoration: none; margin-right: 15px; font-weight: 500; }
    .partner-links a:hover { text-decoration: underline; color: #111b3d; }

    /* Hero Section */
    .hero-section {
        background-color: #111b3d; background-image: url('https://etherscan.io/images/svg/waves-light.svg');
        border-radius: 8px; padding: 35px 30px; color: white; margin-bottom: 20px;
    }
    .search-bar { width: 100%; padding: 12px; border-radius: 6px; border: none; font-size: 15px; margin-top: 15px; }
    
    /* Stats Card - ตัวเลขสีเข้มชัดเจนตามสั่ง */
    .stats-card {
        background: white; border-radius: 12px; border: 1px solid #e7eaf3;
        padding: 20px; box-shadow: 0 0.5rem 1.2rem rgba(189,197,209,.1);
        margin-top: -45px; display: flex; position: relative; z-index: 10;
    }
    .stat-col {flex: 1; padding: 0 15px; border-right: 1px solid #e7eaf3;}
    .stat-col:last-child {border-right: none;}
    .stat-label { color: #6c757d; font-size: 11px; margin-bottom: 5px; font-weight: 600; text-transform: uppercase; }
    .stat-value { font-size: 20px; font-weight: 800; color: #111b3d !important; } 

    /* List Cards */
    .list-card { background: white; border-radius: 12px; border: 1px solid #e7eaf3; margin-top: 25px; }
    .list-header { padding: 15px 20px; border-bottom: 1px solid #e7eaf3; font-weight: 700; color: #111b3d; }
    .list-row { display: flex; align-items: center; padding: 15px 20px; border-bottom: 1px solid #e7eaf3; font-size: 14px; }
    
    .btn-view-all { display: block; width: 100%; text-align: center; padding: 12px; background: #f8f9fa; color: #6c757d; font-size: 13px; text-decoration: none; border-radius: 0 0 12px 12px; }
</style>
""", unsafe_allow_html=True)

# ====================== DATA FETCHING ======================
def fetch_data():
    data = {"latest_block": 0, "balance": 0, "blocks": []}
    try:
        if w3.is_connected():
            latest = w3.eth.block_number
            data["latest_block"] = latest
            data["balance"] = w3.from_wei(w3.eth.get_balance(ALITH_WALLET), 'ether')
            for i in range(6):
                if latest - i < 0: break
                block = w3.eth.get_block(latest - i)
                data["blocks"].append({"number": block.number, "tx": len(block.transactions)})
    except: pass
    return data

chla_data = fetch_data()

# ====================== TOP PARTNER SECTION ======================
st.markdown(f"""
<div class="partner-section">
    <div class="partner-row">
        <span class="partner-tag">🇹🇭 TH EXCHANGES:</span>
        <div class="partner-links">
            <a href="https://www.bitkub.com" target="_blank">Bitkub</a>
            <a href="https://bitazza.com" target="_blank">Bitazza</a>
            <a href="https://www.orbixofficial.com" target="_blank">Orbix</a>
            <a href="https://www.xspringdigital.com" target="_blank">Coinbay</a>
        </div>
    </div>
    <div class="partner-row">
        <span class="partner-tag">🌍 GLOBAL:</span>
        <div class="partner-links">
            <a href="https://www.binance.com" target="_blank">Binance</a>
            <a href="https://www.okx.com" target="_blank">OKX</a>
            <a href="https://www.bybit.com" target="_blank">Bybit</a>
            <a href="https://www.coinbase.com" target="_blank">Coinbase Pro</a>
            <a href="https://www.gate.io" target="_blank">Gate.io</a>
            <a href="https://t.me" target="_blank">Telegram</a>
            <a href="https://google.com" target="_blank">Google</a>
        </div>
    </div>
</div>
<h2 style="color: #0a2540; margin-left: 20px; display: flex; align-items: center;">
    <span style="background:#0a2540; color:white; border-radius:50%; width:32px; height:32px; display:inline-flex; align-items:center; justify-content:center; margin-right:10px; font-size:16px;">C</span>
    CHLA<span style="color:#0784c3;">scan</span>
</h2>

<div class="hero-section">
    <h2 style="margin:0; font-weight: 500;">The CHELA Blockchain Explorer</h2>
    <input type="text" class="search-bar" placeholder="Search by Address / Txn Hash / Block / Token">
</div>

<div class="stats-card">
    <div class="stat-col">
        <div class="stat-label">CHLA PRICE</div>
        <div class="stat-value">$0.0042 <span style="color:#00a186; font-size:12px;">(+0.80%)</span></div>
    </div>
    <div class="stat-col">
        <div class="stat-label">LATEST BLOCK</div>
        <div class="stat-value">{chla_data['latest_block']:,}</div>
    </div>
    <div class="stat-col">
        <div class="stat-label">ADMIN BALANCE</div>
        <div class="stat-value">{chla_data['balance']:,.2f} CHLA</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ====================== MAIN CONTENT ======================
col1, col2 = st.columns(2)

with col1:
    html = '<div class="list-card"><div class="list-header">Latest Blocks</div>'
    for b in chla_data["blocks"]:
        html += f"""<div class="list-row">
            <div style="background:#f8f9fa; padding:10px; border-radius:8px; margin-right:15px;">📦</div>
            <div style="flex:1;"><b style="color:#0784c3;">{b['number']}</b><br><small style="color:#6c757d;">{0.5 * (chla_data['latest_block'] - b['number']):.1f}s ago</small></div>
            <div style="text-align:right;"><span style="background:#f8f9fa; padding:4px 8px; border:1px solid #e7eaf3; border-radius:6px; font-size:11px; font-weight:600;">{b['tx']} Txns</span></div>
        </div>"""
    html += '<a href="#" class="btn-view-all">VIEW ALL BLOCKS →</a></div>'
    st.markdown(html, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="list-card"><div class="list-header">UHU+ Social & Tools</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("🚀 UHU Layer-2 Portal", "https://uhu-mainnet.vercel.app", use_container_width=True)
        st.link_button("🟢 Line Official", "https://line.me", use_container_width=True)
    with c2:
        st.link_button("🐦 Follow X (Twitter)", "https://twitter.com", use_container_width=True)
        st.link_button("📂 GitHub Repository", "https://github.com", use_container_width=True)
    st.markdown('<div style="padding: 20px; border-top: 1px solid #e7eaf3; font-size:13px; color:#6c757d;">'
                '<b>Tip:</b> คุณสามารถตรวจสอบสถานะโหนดผ่านทาง <a href="https://t.me" style="color:#0784c3;">Telegram Bot</a> ได้ตลอด 24 ชม.'
                '</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== FOOTER ======================
st.markdown('<div style="margin-top:50px; text-align:center; color:#6c757d; font-size:12px;">'
            'CHLAscan • Data provided by CHELA Layer-1 Node (X99 Performance)</div>', unsafe_allow_html=True)

time.sleep(2) # รีเฟรชไวขึ้นเพื่อให้สมกับความเร็ว 500ms
st.rerun()
