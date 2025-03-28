import subprocess
import sys

def install_packages(packages):
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    packages = ["requests", "pynput", "pyinstaller"]
    install_packages(packages)
