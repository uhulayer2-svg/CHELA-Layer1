from web3 import Web3

# 1. เชื่อมต่อโหนด
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:9944'))

# 2. กุญแจมาตรฐานของ Alith (ร่างอวตารมหาเศรษฐี)
alith_priv = "0x5fb92d6e98884f76de468fa3f6278f8807c48bebc13595d45af5bdc4da702133"
alith_address = "0xf24FF3a9CF04c71Dbc94D0b566f7A27B94566cac"

# 3. กระเป๋าเป้าหมายของเรา
evm_receiver = Web3.to_checksum_address("0x52f52c444f4f736bc195647154212d35ec51c89f")

print(f"🌍 สถานะการเชื่อมต่อโหนด EVM: {'✅ ปกติ' if w3.is_connected() else '❌ ล้มเหลว'}")

# เช็คยอดเงินของ Alith
balance_wei = w3.eth.get_balance(alith_address)
balance_chla = w3.from_wei(balance_wei, 'ether')
print(f"💰 เงินในคลัง Alith: {balance_chla} CHLA")

if balance_wei == 0:
    print("❌ คลังว่างเปล่า")
else:
    print(f"💸 กำลังโอน 5,000 CHLA ให้กระเป๋าของท่านประธาน...")
    
    tx = {
        'nonce': w3.eth.get_transaction_count(alith_address),
        'to': evm_receiver,
        'value': w3.to_wei(5000, 'ether'),
        'gas': 21000,
        'gasPrice': w3.eth.gas_price,
        'chainId': w3.eth.chain_id
    }

    try:
        # เซ็นธุรกรรม
        signed_tx = w3.eth.account.sign_transaction(tx, alith_priv)
        
        # --- จุดที่แก้คือตรงนี้ครับ: เปลี่ยนเป็น raw_transaction ---
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"⏳ กำลังรอให้บล็อกเชนบันทึก... (Hash: {w3.to_hex(tx_hash)})")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt.status == 1:
            print("🎉 [สำเร็จ!!!] เงิน 5,000 CHLA เข้ากระเป๋า EVM อย่างเป็นทางการแล้วครับ!")
        else:
            print("❌ ธุรกรรมล้มเหลว (Reverted)")
            
    except Exception as e:
        print(f"❌ พลาด: {e}")
