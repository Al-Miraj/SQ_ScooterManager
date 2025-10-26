import os
import sys
import sqlite3


class DCM:
    """
    DCM stands for Database Connection Manager.

    This file should be in the same directory are the database for self.connect to generate the correct path.
    """
    def __init__(self, dbFile):
        self.dbFile = dbFile
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), self.dbFile))

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None