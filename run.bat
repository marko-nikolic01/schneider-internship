@echo off

start /B python.exe .\servers\adder.py
start /B python.exe .\servers\subtractor.py
start /B python.exe .\servers\multiplier.py
start /B python.exe .\servers\divider.py

python.exe .\servers\server.py
