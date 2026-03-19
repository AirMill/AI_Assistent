import os
import webbrowser
import time
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def is_running():
    result = subprocess.run(
        ["docker", "ps"],
        capture_output=True,
        text=True
    )
    return "ai-assistant" in result.stdout.lower()

def run():
    if is_running():
        webbrowser.open("http://localhost:8000")
        return

    subprocess.run(
        ["docker", "compose", "up", "-d"],
        cwd=BASE_DIR
    )

    time.sleep(5)
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    run()