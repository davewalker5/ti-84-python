@ECHO OFF
SET PROJECT_ROOT=%~p0
CALL %PROJECT_ROOT%\venv\Scripts\activate.bat
SET PYTHONPATH=

REM Add all the source sub-folders *except* the desktop implementation of the TI packages to PYTHONPATH
SETLOCAL ENABLEDELAYEDEXPANSION
FOR /D %%F IN (%PROJECT_ROOT%src\*) DO (
    IF NOT %%F == %PROJECT_ROOT%src\ti_desktop (
        IF NOT %%F == %PROJECT_ROOT%src\__pycache__ (
            SET PYTHONPATH=%%F;!PYTHONPATH!
        )
    )
)

REM Add the mocks for the TI packages to PYTHONPATH
SET PYTHONPATH=%PROJECT_ROOT%tests\mocks;%PYTHONPATH%

ECHO Project root      = %PROJECT_ROOT%
ECHO Python Path       = %PYTHONPATH%

coverage run --branch --source src -m unittest discover
coverage html -d cov_html
ECHO ON