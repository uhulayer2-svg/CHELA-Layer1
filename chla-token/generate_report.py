import time

def save_daily_report(balance):
    report_date = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("CHELA_Daily_Report.txt", "a") as f:
        f.write(f"[{report_date}] Status: Online | Treasury: {balance:,.2f} CHLA\n")
    print(f"📝 บันทึกรายงานประจำวันเรียบร้อยแล้ว!")

# เรียกใช้ฟังก์ชัน
save_daily_report(9996997000.00)
