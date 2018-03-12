@ECHO OFF

goto start

:start
cls
if not exist installedrequirements.txt (
	echo Installing requirements from requirements.txt
	python -m pip install -r requirements.txt
	echo - >installedrequirements.txt
)
if not exist databases (
	mkdir databases
)
python hpybot.py
ping -n 2 127.0.0.1 >nul
goto start