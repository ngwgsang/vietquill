@echo off

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist src\vietquill.egg-info rmdir /s /q src\vietquill.egg-info

call scripts\clean.bat

python -m build
twine check dist/*