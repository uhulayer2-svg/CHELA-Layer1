
#!/bin/bash

echo "🚀 กำลังปลุกกองทัพ CHELA-Layer1 (Firefox Edition)..."

# 1. เข้าสู่ Environment
# ตรวจสอบว่ามีโฟลเดอร์ myenv หรือไม่ก่อนรัน
if [ -d "myenv" ]; then
    source myenv/bin/activate
else
    echo "❌ ไม่พบโฟลเดอร์ myenv กรุณาตรวจสอบตำแหน่งไฟล์"
    exit 1
fi

# 2. เคลียร์พอร์ต 8502 (Dashboard) และ 9944 (RPC Node) ให้ว่าง
echo "🧹 กำลังตรวจสอบและเคลียร์พอร์ตที่ค้างอยู่..."
fuser -k 8502/tcp > /dev/null 2>&1
fuser -k 9944/tcp > /dev/null 2>&1
sleep 1

# 3. รันตัว Chain (Node) ใน Background
# ใช้ PATH จริงที่ท่านประธานเพิ่งคอมไพล์สำเร็จบน SSD 1TB
echo "🌐 เริ่มรัน Blockchain Node (CHELA-Layer1)..."
nohup /mnt/ssd_1tb/workspace/web3_labs/chela-layer1/target/release/frontier-template-node --dev > node.log 2>&1 &

# รอให้ Node สตาร์ทตัวสักครู่ก่อนรัน Dashboard
sleep 3

# 4. รัน Dashboard (Streamlit) และบังคับให้เปิดด้วย Firefox
echo "📊 เริ่มรัน Dashboard ที่พอร์ต 8502..."
# บังคับ Environment BROWSER ให้เป็น firefox สำหรับสคริปต์นี้
export BROWSER=firefox

# รัน streamlit โดยสั่งเปิดเบราว์เซอร์อัตโนมัติ
nohup python3 -m streamlit run dashboard/dashboard.py --server.port 8502 --server.headless false > dashboard.log 2>&1 &

echo "---------------------------------------------------"
echo "✅ ทุกอย่างเรียบร้อยครับท่านประธาน!"
echo "🦊 ระบบกำลังเปิด Dashboard บน Firefox ให้โดยอัตโนมัติ"
echo "🔗 หากไม่เปิดเอง เข้าไปที่: http://localhost:8502"
echo "📝 ดูสถานะบล็อก (Node): tail -f node.log"
echo "📝 ดูสถานะหน้าเว็บ (Dashboard): tail -f dashboard.log"
echo "---------------------------------------------------"
