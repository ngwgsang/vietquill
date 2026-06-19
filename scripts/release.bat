@echo off

call scripts\build.bat

twine upload dist/*