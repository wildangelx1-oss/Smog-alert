
import json
import os
import urllib.request
from pathlib import Path

URL = "https://smogtok.com/apprest/probedata/429760"
PROG = 15
PLIK = Path("alarm_state.json")

topic = os.environ["NTFY_TOPIC"].strip()
topic = topic.removeprefix("https://ntfy.sh/").strip("/")

with urllib.request.urlopen(URL, timeout=20) as response:
    dane = json.load(response)

pm25 = next(
    float(p["VALUE"])
    for p in dane["REGS"]
    if p["REGNAME"] == "PM 2,5"
)

print(f"SmogTok 429760: PM2.5 = {pm25} µg/m³")

if PLIK.exists():
    stan = json.loads(PLIK.read_text())
    alarm_aktywny = stan.get("alarm_aktywny", False)
else:
    alarm_aktywny = False

if pm25 > PROG:
    if not alarm_aktywny:
        wiadomosc = (
            f"ALARM SMOGOWY! PM2.5: {pm25} µg/m³. "
            f"Próg: {PROG} µg/m³. Tuchów, Leśna."
        )
        req = urllib.request.Request(
            f"https://ntfy.sh/{topic}",
            data=wiadomosc.encode("utf-8"),
            headers={
                "Title": "Alarm smogowy",
                "Priority": "high",
                "Tags": "warning"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            print("Powiadomienie wysłane:", r.status)
    else:
        print("Smog nadal trwa. Bez nowego alarmu.")

    alarm_aktywny = True
else:
    print("Powietrze poniżej progu. Alarm zresetowany.")
    alarm_aktywny = False

PLIK.write_text(json.dumps({
    "alarm_aktywny": alarm_aktywny
}))
