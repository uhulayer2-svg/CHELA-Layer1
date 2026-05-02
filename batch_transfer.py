import os
from web3 import Web3

# 1. เชื่อมต่อระบบ
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
token_address = '0x7bA3EfA6ecd194bEeBcD5d91D62f0DF5C6ecB4a4'
# ดึง Private Key จาก .env ที่เราตั้งค่าไว้
from dotenv import load_dotenv
load_dotenv()
private_key = os.getenv("PRIVATE_KEY")
sender_address = '0x2Eeb0f207C8CF5Fe5F74F50D54572183FDF1087c'

# 2. รายชื่อกระเป๋าเป้าหมาย (จาก MetaMask ของท่าน)
recipients = {
    "UHU_Ecosystem_Reward": "0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65", # ตัวอย่างกระเป๋า
    "UHU_Team_Dev": "0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc"
}

# 3. ABI สำหรับส่งเหรียญ
abi = '[{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]'
contract = w3.eth.contract(address=token_address, abi=abi)

def send_chla(name, to_address, amount_chla):
    amount_wei = amount_chla * 10**18
    nonce = w3.eth.get_transaction_count(sender_address)
    
    tx = contract.functions.transfer(to_address, amount_wei).build_transaction({
        'chainId': 31337,
        'gas': 100000,
        'gasPrice': w3.to_wei('2', 'gwei'),
        'nonce': nonce,
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"✅ Transferred {amount_chla:,.0f} CHLA to {name} | Hash: {tx_hash.hex()}")

# รันการโอน
print(f"🚀 Starting Batch Transfer for CHELA Ecosystem...")
send_chla("Ecosystem Reward", recipients["UHU_Ecosystem_Reward"], 1000000)
send_chla("Team Dev", recipients["UHU_Team_Dev"], 500000)
print(f"✨ All transfers completed!")
