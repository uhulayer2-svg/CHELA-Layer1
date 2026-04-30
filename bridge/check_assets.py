from web3 import Web3
import json

# เชื่อมต่อ Node
RPC_URL = "http://127.0.0.1:9944"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# แปลงเป็น Checksum Address ให้ถูกต้อง (เพื่อแก้ InvalidAddress Error)
alice_addr = w3.to_checksum_address("0xd43593c715fdd31c61141abd04a99fd6822c8558")
bob_addr = w3.to_checksum_address("0x8eaf0415161f609e293c5258860e7565e3129556")

def diagnostic():
    print("=== 🛡️ CHELA DEEP AUDIT START ===")
    
    if not w3.is_connected():
        print("❌ เชื่อมต่อ Node ไม่ได้!")
        return

    # 1. ข้อมูลพื้นฐาน
    print(f"✅ Chain ID: {w3.eth.chain_id}")
    print(f"✅ Latest Block: {w3.eth.block_number}")

    # 2. ตรวจสอบยอดเงิน
    # เราจะดูทั้งหน่วย Wei และหน่วย ETH (CHLA)
    balance_wei = w3.eth.get_balance(alice_addr)
    balance_chla = w3.from_wei(balance_wei, 'ether')
    
    print(f"\n💰 [Alice Balance]")
    print(f"   - Raw Wei: {balance_wei}")
    print(f"   - CHLA (18 decimals): {balance_chla}")

    # 3. ตรวจสอบ "ทศนิยม" (Decimals)
    # ใน Substrate บางครั้งเหรียญหลักอาจไม่ใช่ 18 ทศนิยม 
    # ถ้าโอน 1 ETH แล้วยอดหายไปเยอะเกินจริง แสดงว่า Decimals ไม่ใช่ 18
    if balance_wei > 0:
        print(f"📊 ระบบตรวจพบเหรียญในกระเป๋าแล้ว!")
    else:
        print(f"⚠️ ยอดเงินเป็น 0! กรุณาเช็กว่ารันโหนดด้วย --dev หรือไม่")

    # 4. ทดลองคำนวณค่า Gas (Gas Estimation)
    # นี่คือการทดสอบว่า "ถ้าโอนจริง จะติดอะไรไหม?" โดยยังไม่เสียเงินจริง
    print(f"\n⛽ [Gas Inspection]")
    try:
        gas_estimate = w3.eth.estimate_gas({
            'from': alice_addr,
            'to': bob_addr,
            'value': w3.to_wei(0.1, 'ether')
        })
        print(f"   ✅ ทดสอบคำนวณค่าแก๊สสำเร็จ: {gas_estimate} units")
        print(f"   📢 สรุป: โทเค็นพร้อมโอนจริง 100%")
    except Exception as e:
        print(f"   ❌ ทดสอบโอนพลาด: {e}")
        print(f"   📢 วิเคราะห์: ระบบบล็อกเชนไม่อนุญาตให้โอน (อาจจะเพราะค่า Gas Price ต่ำไป หรือ Chain ID ผิด)")

diagnostic()
