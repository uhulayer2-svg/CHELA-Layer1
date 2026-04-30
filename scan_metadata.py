from substrateinterface import SubstrateInterface

# เชื่อมต่อโหนด CHELA
try:
    substrate = SubstrateInterface(url="ws://127.0.0.1:9944")
    print("=== 🛰️ CHELA METADATA SCANNER ===")
    
    # ดึง Metadata ทั้งหมด
    metadata = substrate.get_metadata()
    
    found_any = False
    print(f"🔍 กำลังค้นหา Pallet ที่เกี่ยวข้องกับบัญชีและการเงิน...\n")

    for pallet in metadata.pallets:
        p_name = pallet.name
        # ค้นหาคำที่น่าจะใช่: Balances, Assets, Tokens, System, EVM
        search_terms = ['balance', 'asset', 'token', 'currency', 'system', 'evm']
        
        if any(term in p_name.lower() for term in search_terms):
            found_any = True
            print(f"📦 พบ Pallet: **{p_name}**")
            
            if hasattr(pallet, 'calls') and pallet.calls:
                print("  ฟังก์ชันที่เรียกใช้ได้ (Calls):")
                for call in pallet.calls:
                    print(f"  - {call.name}")
            else:
                print("  (ไม่มีฟังก์ชันการเรียกใน Pallet นี้)")
            print("-" * 30)

    if not found_any:
        print("❌ ไม่พบ Pallet มาตรฐานเลย! นี่คือรายชื่อ Pallet ทั้งหมดที่มี:")
        for pallet in metadata.pallets:
            print(f" - {pallet.name}")

except Exception as e:
    print(f"❌ เชื่อมต่อโหนดไม่ได้: {e}")
