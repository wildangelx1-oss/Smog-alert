
import json
import urllib.request

URL = "https://smogtok.com/apprest/probedata/429760"
PROG = 15

with urllib.request.urlopen(URL, timeout=20) as response:
    dane = json.load(response)

pm25 = next(
    float(pomiar["VALUE"])
    for pomiar in dane["REGS"]
    if pomiar["REGNAME"] == "PM 2,5"
)

print(f"SmogTok 429760: PM2.5 = {pm25} µg/m³")

if pm25 > PROG:
    print("ALARM: Przekroczono prog PM2.5!")
else:
    print("Jakosc powietrza ponizej progu alarmowego.")
