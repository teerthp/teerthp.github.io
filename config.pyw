import requests, os, time, subprocess, sys

M_ID = 5
db_url = "https://remote-pc-cont-default-rtdb.asia-southeast1.firebasedatabase.app/"

path = os.path.abspath(sys.argv[0])
to_delete = False
batFileName = "temp.bat"
batFileContent = f"""timeout /t 10
if exist "{path}" del /q "{path}"
del "%~f0"
"""

while True:
    try:
        value = requests.get(db_url + "control/cmd.json", timeout = 15).json()

        if(value == 0):
            time.sleep(60)
            continue

        elif value != 0:
            machine_id = requests.get(db_url + "control/M_ID.json", timeout = 15).json()
            isThisMachine = machine_id == M_ID or machine_id == 0

            if isThisMachine:
                if value in [1, 2, 3] or value == -1:
                    requests.put(db_url + "control/res.json", json = value)

                    if requests.get(db_url + "control/run_once.json", timeout = 15).json() or value == -1:
                        requests.put(db_url + "control/cmd.json", json = 0)

                    if value == 1:
                        os.system("shutdown /s /t 0")
                    elif value == 2:
                        os.system("shutdown /r /t 0")
                    elif value == 3:
                        os.system("shutdown /l")

                    elif value == -1:
                        to_delete = True
                        break

    except Exception as e:
        exp = e
        time.sleep(1)

if to_delete:
    with open(batFileName, "w") as f:
        f.write(batFileContent)
    subprocess.Popen([batFileName], shell = True, creationflags = subprocess.CREATE_NO_WINDOW)