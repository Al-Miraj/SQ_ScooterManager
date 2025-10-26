import os
import json
from datetime import datetime
from Utils.security import encrypt, decrypt
from Database.MainDb import MainDb

logFilePath = MainDb.logFilePath

def _loadLogs():
    if not os.path.exists(logFilePath):
        return []
    with open(logFilePath, "r") as file:
        encrypted_data = file.read()
    try:
        decrypted_data = decrypt(encrypted_data)
        return json.loads(decrypted_data)
    except:
        return []

def _saveLogs(logs):
    data = json.dumps(logs)
    encrypted = encrypt(data)
    with open(logFilePath, "w") as file:
        file.write(encrypted)

def logEvent(username, description, suspicious=False):
    logs = _loadLogs()
    logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "description": description,
        "suspicious": suspicious,
        "read": False
    })
    _saveLogs(logs)

def getLogs():
    return _loadLogs()

def markLogAsRead():
    logs = _loadLogs()
    for log in logs:
        log["read"] = True
    _saveLogs(logs)

def getUnreadSuspisciousCount():
    logs = _loadLogs()
    return len([log for log in logs if log["suspicious"] and not log["read"]])
