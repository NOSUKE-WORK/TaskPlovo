"""
TaskPlovo - エントリーポイント
"""
import sys
import os

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, BASE_DIR)

from app import TaskPlovoApp

if __name__ == "__main__":
    app = TaskPlovoApp()
    app.run()
