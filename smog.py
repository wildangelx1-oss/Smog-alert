
import json
import os
import urllib.request

URL = "https://smogtok.com/apprest/probedata/429760"
PROG = 15

topic = os.environ["NTFY_TOPIC"].strip()
if topic.startswith("https://ntfy.sh/"):
    topic = topic.removeprefix("https://ntfy.sh/")
topic = topic.strip("/")

with urllib.request.urlopen(URL, timeout=20) as response:
    dane = json.load(response)

pm25 = next(
    float(pomiar["VALUE"])
    for pomiar in dane["REGS"]
    if pomiar["REGNAME"] == "PM 2,5"
)

print(f"SmogTok 429760: PM2.5 = {pm25} µg/m³")

if pm25 > PROG:
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

    with urllib.request.urlopen(req, timeout=20) as response:
        print("Powiadomienie wysłane:", response.status)
else:
    print("Powietrze poniżej progu alarmowego.")

