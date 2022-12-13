@ECHO OFF
SET PROJECT_ROOT=%~p0
CALL %PROJECT_ROOT%\venv\Scripts\activate.bat
SET PYTHONPATH=%PROJECT_ROOT%src;%PROJECT_ROOT%src\common;%PROJECT_ROOT%src\mocks;%PROJECT_ROOT%src\maths

ECHO Project root      = %PROJECT_ROOT%
ECHO Python Path       = %PYTHONPATH%

python -m unittest
ECHO ON
