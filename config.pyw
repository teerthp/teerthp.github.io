import requests, os, time, subprocess, sys

M_ID = 5
db_url = "https://rpcc-dep-default-rtdb.asia-southeast1.firebasedatabase.app/"

path = os.path.abspath(sys.argv[0])
to_delete = False
batFileName = "temp.bat"
batFileContent = f"""timeout /t 10
if exist "{path}" del /q "{path}"
del "%~f0"
"""

while True:
    try:
        data = requests.get(db_url + "control.json", timeout = 10).json()
        cmd = data.get("cmd")
        isThisMachine = data.get("M_ID") == M_ID or data.get("M_ID") == 0

        if isThisMachine:
            if(cmd == 0):
                time.sleep(data.get("sleep_time"))
                continue

            elif cmd != 0:
                if cmd in [1, 2, 3] or cmd == -1:
                    requests.put(db_url + "control/res.json", json = cmd)

                    if data.get("run_once") or cmd == -1:
                        requests.put(db_url + "control/cmd.json", json = 0)

                    if cmd == 1:
                        os.system("shutdown /s /t 0")
                    elif cmd == 2:
                        os.system("shutdown /r /t 0")
                    elif cmd == 3:
                        os.system("shutdown /l")

                    elif cmd == -1:
                        to_delete = True
                        break
        else:
            try:
                time.sleep(data.get("default_sleep_time"))
            except Exception as e:
                exp = e
                time.sleep(60)

    except Exception as e:
        exp = e
        time.sleep(1)

if to_delete:
    with open(batFileName, "w") as f:
        f.write(batFileContent)
    subprocess.Popen([batFileName], shell = True, creationflags = subprocess.CREATE_NO_WINDOW)
