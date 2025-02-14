import subprocess
import sys
import os

def install_package(package):
    """Installs the given package using pip."""
    print(f"-Installing {package}...")    
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print(f"-Installed {package}.")    

def run_py(file):
    """Runs file.py after installation."""
    if not file.endswith('.py'):
        file += '.py'
    if os.path.exists(file):
        print(f"--Running {file}...")
        subprocess.run([sys.executable, file])
        print(f"--Successfully Run {file}.")
    else:
        print(f"Error: {file} not found!")

if __name__ == "__main__":
    print("Installing Packages...")
    install_package("faker")
    install_package("mysql-connector-python")
    install_package("python-dotenv")
    print("Package Installation complete.")
    run_py("generate_faker")
    run_py("load_into_sql")
    print("---DONE---")
