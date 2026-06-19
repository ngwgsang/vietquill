@echo off

call scripts\clean.bat

python -m build
twine check dist/*