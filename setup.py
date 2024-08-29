from cx_Freeze import *

bdist_msi_options = {
    "summary_data": {"author": "1is7ac3", "comments": "by OIQ SERVICES"},
    "upgrade_code": "{00000000-AAAA-AAAA-AA13-8A233A3F8901}",
}

executables = [
    Executable(
        "login.py", icon="inventory.ico",
        copyright="Copyright (C) 2024 company_name", base="gui",
        shortcut_name="OIQ Inventory",
        shortcut_dir="DesktopFolder",
    )
]

setup(
    name="OIQ Inventory",
    version="0.1",
    description="Sistema de inventario para pernosteel",
    executables=executables,
    options={
        "bdist_msi": bdist_msi_options,
    },
)
