# -*- coding: utf-8 -*-
import time
import os
import sys
from web3 import Web3
from dotenv import load_dotenv

os.environ["PYTHONIOENCODING"] = "utf-8"
load_dotenv()

RPC_URL = "http://127.0.0.1:9944"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

ALITH_WALLET = "0xf24FF3a9CF04c71Dbc94D0b566f7A27B94566cac"
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

RECIPIENTS = [
    "0x3245000000000000000000000000000000003245", 
    "0x7de95a882D706859e924dF523456789012345678"
]

def send_auto_tx(to_address, amount_ether):
    try:
        nonce = w3.eth.get_transaction_count(ALITH_WALLET)
        tx = {
            'nonce': nonce,
            'to': w3.to_checksum_address(to_address),
            'value': w3.to_wei(amount_ether, 'ether'),
            'gas': 21000,
            'gasPrice': w3.eth.gas_price,
            'chainId': 42
        }
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        
        # 🛠️ แก้ไขตรงนี้: เปลี่ยนเป็น .raw_transaction สำหรับ Web3 v6
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"[SUCCESS] Block: {w3.eth.block_number} | Hash: {tx_hash.hex()[:14]}...")
    except Exception as e:
        error_msg = repr(e)
        print(f"[ERROR CALLBACK] {error_msg}")

print("--- CHELA Auto-Feeder is now Running ---")

while True:
    if not PRIVATE_KEY:
        print("⚠️ PRIVATE_KEY not found in .env!")
        break
    for addr in RECIPIENTS:
        send_auto_tx(addr, 0.001)
        time.sleep(15)
