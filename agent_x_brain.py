import os
import time
from web3 import Web3
from dotenv import load_dotenv

# โหลดค่าคอนฟิกจาก .env ของเครื่อง X99
load_dotenv()
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
private_key = os.getenv("PRIVATE_KEY")
sender_address = '0x2Eeb0f207C8CF5Fe5F74F50D54572183FDF1087c'
token_address = '0x7bA3EfA6ecd194bEeBcD5d91D62f0DF5C6ecB4a4'

# ข้อมูลเงื่อนไข (Threshold)
ECOSYSTEM_WALLET = "0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65"
MIN_BALANCE = 3000000 * 10**18  # เกณฑ์ขั้นต่ำ: 5 แสน CHLA
REFILL_AMOUNT = 1000000 * 10**18 # จำนวนที่เติม: 1 ล้าน CHLA

# ABI สำหรับเช็คยอดและโอน
abi = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]'
contract = w3.eth.contract(address=token_address, abi=abi)

def autonomous_decision():
    print(f"🤖 Agent X กำลังวิเคราะห์สภาพคล่องในระบบ...")
    balance = contract.functions.balanceOf(ECOSYSTEM_WALLET).call()
    print(f"📊 Ecosystem Reward Balance: {balance / 10**18:,.2f} CHLA")

    if balance < MIN_BALANCE:
        print(f"⚠️ ตรวจพบยอดต่ำกว่าเกณฑ์! เริ่มกระบวนการเติมทุนอัตโนมัติ...")
        nonce = w3.eth.get_transaction_count(sender_address)
        tx = contract.functions.transfer(ECOSYSTEM_WALLET, REFILL_AMOUNT).build_transaction({
            'chainId': 31337,
            'gas': 100000,
            'gasPrice': w3.to_wei('2', 'gwei'),
            'nonce': nonce,
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"✅ เติมทุนสำเร็จ! Hash: {tx_hash.hex()}")
    else:
        print(f"✅ สภาพคล่องยังอยู่ในระดับปกติ")

if __name__ == "__main__":
    while True:
        autonomous_decision()
        time.sleep(60) # ตรวจสอบทุกๆ 1 นาที
