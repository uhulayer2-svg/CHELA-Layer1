import time
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:9944"))

# กุญแจที่ให้ Address: 0x52F52c444F4F736Bc195647154212d35Ec51c89f
PRIVATE_KEY = "0xe5beee6930411a4d1b44d21628b15a7f9e13d11394562c129e924a259972c842"
sender = w3.eth.account.from_key(PRIVATE_KEY).address
receiver = w3.to_checksum_address("0x8eaf0415161f609e293c5258860e7565e3129556")

def run_test():
    try:
        balance = w3.eth.get_balance(sender)
        print(f"💰 Balance of {sender}: {w3.from_wei(balance, 'ether')} CHLA")
        
        if balance < w3.to_wei(0.1, 'ether'):
            print("❌ เงินไม่พอ! กรุณารันคำสั่ง curl เพื่อโอนเงินจากกระเป๋าใหญ่มาก่อน")
            return

        nonce = w3.eth.get_transaction_count(sender)
        tx = {
            'nonce': nonce,
            'to': receiver,
            'value': w3.to_wei(1, 'ether'),
            'gas': 21000,
            'gasPrice': w3.eth.gas_price,
            'chainId': w3.eth.chain_id
        }

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"🚀 [สำเร็จ!] โอนแล้ว! Hash: {tx_hash.hex()}")

    except Exception as e:
        print(f"❌ พลาด: {e}")

if __name__ == "__main__":
    print("========================================")
    print("💸 CHELA PRODUCTION TESTER")
    print("========================================")
    while True:
        run_test()
        time.sleep(10)
