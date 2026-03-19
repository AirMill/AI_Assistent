import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def stop():
    print("Stopping AI Assistant...")
    subprocess.run(
        ["docker", "compose", "down"],
        cwd=BASE_DIR
    )

if __name__ == "__main__":
    stop()