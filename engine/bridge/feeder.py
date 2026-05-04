import pandas as pd
import time
import os
from web3 import Web3

# --- 1. การเชื่อมต่อ ---
# เปลี่ยน URL เป็น RPC ของ CHELA Node (ปกติคือ 8545)
RPC_URL = "http://127.0.0.1:8545" 
w3 = Web3(Web3.HTTPProvider(RPC_URL))

CSV_PATH = "/media/mrnong/28e53eb6-2e49-4ad2-b2e1-f1c490db73b1/transactions.csv"

def get_real_data():
    if not w3.is_connected():
        print("❌ เชื่อมต่อ Node ไม่ได้! ตรวจสอบว่ารัน Node อยู่หรือไม่")
        return None

    # ดึงเลขบล็อกล่าสุด
    latest_block_num = w3.eth.block_number
    block = w3.eth.get_block(latest_block_num, full_transactions=True)
    
    new_txs = []
    for tx in block.transactions:
        new_txs.append({
            "Txn Hash": tx.hash.hex(),
            "Method": "Transfer", # หรือวิเคราะห์จาก Input data
            "Block": latest_block_num,
            "From": tx['from'],
            "Amount": f"{w3.from_wei(tx['value'], 'ether')} CHLA"
        })
    
    return pd.DataFrame(new_txs) if new_txs else None

print("🚀 CHELA Real-time Feeder is running...")

while True:
    real_df = get_real_data()
    
    if real_df is not None:
        if os.path.exists(CSV_PATH):
            old_df = pd.read_csv(CSV_PATH)
            # เอาข้อมูลใหม่วางบน ลบของซ้ำ และเก็บแค่ 50 รายการ
            combined_df = pd.concat([real_df, old_df]).drop_duplicates(subset=['Txn Hash']).head(50)
            combined_df.to_csv(CSV_PATH, index=False)
            print(f"✅ Updated: Block {w3.eth.block_number}")
    
    time.sleep(3) # เช็กทุก 3 วินาที
