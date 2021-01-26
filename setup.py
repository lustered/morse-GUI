import pip

pip_packages = ["tk", "cx_freeze"]
pip.main(["install", *pip_packages])

import cx_Freeze

shortcut_table = [
    (
        "DesktopShortcut",  # Shortcut
        "DesktopFolder",  # Directory_
        "MorseTranslator",  # Name
        "TARGETDIR",  # Component_
        "[TARGETDIR]MorseTranslator.exe",  # Target
        None,  # Arguments
        None,  # Description
        None,  # Hotkey
        None,  # Icon
        None,  # IconIndex
        None,  # ShowCmd
        "TARGETDIR",  # WkDir
    )
]

msi_data = {"Shortcut": shortcut_table}

bdist_msi_options = {
    "data": msi_data,
    "add_to_path": True,
    "dist_dir": "MorseCode-setup",
    "initial_target_dir": r"[DesktopFolder]\MorseTranslator",
}

options = {
    "packages": ["tkinter"],
    "includes": [],
    "excludes": [],
    "include_files": ["translator.py", 'icon.png'],
}

executables = [cx_Freeze.Executable("app.py", base=None, icon=r"icon.svg")]

cx_Freeze.setup(
    name="Morse Translator",
    options={"build_exe": options, 'bdist_msi': bdist_msi_options},
    version="1.0",
    author="Ernesto Rodriguez",
    description="A morse code translator interface",
    executables=executables,
)
