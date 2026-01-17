import os
import platform
import shutil

def get_browser_path():
    """
    Attempts to automatically find the path to the Brave browser or Google Chrome
    executable based on the operating system.
    Returns None if not found.
    """
    system = platform.system()
    
    # Define common paths for different OSs
    # Priority: Brave -> Chrome -> Chromium
    possible_paths = []

    if system == "Windows":
        # Check standard installation paths and user-specific paths
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        program_files = os.environ.get("PROGRAMFILES", "")
        program_files_x86 = os.environ.get("PROGRAMFILES(X86)", "")

        possible_paths = [
            os.path.join(local_app_data, r"BraveSoftware\Brave-Browser\Application\brave.exe"),
            os.path.join(program_files, r"BraveSoftware\Brave-Browser\Application\brave.exe"),
            os.path.join(program_files_x86, r"BraveSoftware\Brave-Browser\Application\brave.exe"),
            os.path.join(program_files, r"Google\Chrome\Application\chrome.exe"),
            os.path.join(program_files_x86, r"Google\Chrome\Application\chrome.exe"),
        ]
    elif system == "Darwin":  # macOS
        possible_paths = [
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        ]
    elif system == "Linux":
        # On Linux, shutil.which is the best way to find binaries in PATH
        binaries = ["brave-browser", "brave", "google-chrome", "google-chrome-stable", "chromium", "chromium-browser"]
        for binary in binaries:
            path = shutil.which(binary)
            if path:
                return path
        
    # Check the list for Windows/Mac
    for path in possible_paths:
        if path and os.path.exists(path):
            return path

    return None
