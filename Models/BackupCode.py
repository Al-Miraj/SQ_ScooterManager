
class BackupCode():
    def __init__(self, filename, hash, username, code, used):
        self.code = code
        self.used = used
        self.filename = filename
        self.hash = hash
        self.username = username
