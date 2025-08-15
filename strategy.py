import sys
import subprocess
import importlib.util

def pip_install(*packages):
    """Install packages into the current Python environment."""
    subprocess.run([sys.executable, "-m", "pip", "install", *packages], check=True)

def ensure_installed(package_spec, import_name=None):
    """
    Install the given package_spec (e.g. 'cpz-ai==1.2.3') if it's not already installed.
    If import_name is different from the PyPI name, pass it explicitly.
    """
    name = import_name or package_spec.split("==")[0].split(">=")[0].split("~=")[0]
    if importlib.util.find_spec(name) is None:
        print(f"📦 Installing {package_spec} ...")
        pip_install(package_spec)
    else:
        print(f"✅ {name} already installed.")

if __name__ == "__main__":
    ensure_installed("cpz-ai")  # Pin version if needed: cpz-ai==x.y.z
    import cpz  # Use the actual import name
    print(f"cpz-ai version: {getattr(cpz, '__version__', 'unknown')}")
