from cx_Freeze import *

bdist_msi_options = {
    "summary_data": {"author": "1is7ac3", "comments": "by OIQ SERVICES"},
    "upgrade_code": "{00000000-AAAA-AAAA-AA13-8A233A3F0001}",
}

executables = [
    Executable(
        "main.py", icon="inventory.ico",
        copyright="Copyright (C) 2024 company_name", base="gui",
        shortcut_name="OIQ Inventory tk",
        shortcut_dir="DesktopFolder",
    )
]

setup(
    name="OIQ Inventory tk",
    version="1.0",
    description="Sistema de inventario para pernosteel",
    executables=executables,
    options={
        "bdist_msi": bdist_msi_options,
    },
)
