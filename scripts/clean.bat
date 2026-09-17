@echo off

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist src\vietquill.egg-info rmdir /s /q src\vietquill.egg-info
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
