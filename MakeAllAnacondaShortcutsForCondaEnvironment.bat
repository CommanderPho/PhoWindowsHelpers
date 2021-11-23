@REM Creates a Windows shortcut by generating a temporary Visual Basic .vbs file, running it, and then deleting it to clean up.
@REM 2021-11-10 - Solution from https://stackoverflow.com/questions/30028709/how-do-i-create-a-shortcut-via-command-line-in-windows
@REM Requres no 3rd Party Dependencies, entirely self-contained
@REM Note that Visual Basic escapes double quotes using another double quote, hence the two quotes before and after  ""%USERPROFILE%/""
@REM 
@REM set "curr_conda_env_name=phoviz"
@REM Usage Examples: MakeAllAnacondaShortcutsForCondaEnvironment.bat PyQt6
@REM 	Example 2: MakeAllAnacondaShortcutsForCondaEnvironment.bat phoviz


@echo off
@REM Check for argument:
IF %1.==. GOTO No1
set arg1=%1
set "curr_conda_env_name=%arg1%"
@REM echo %curr_conda_env_name%

@REM %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@REM "Jupyter-Lab" Shortcut:
@REM %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
call MakeJupyterLabShortcutForCondaEnvironment.bat %curr_conda_env_name%
echo "done with Jupyter-lab shortcut"


@REM %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@REM "Anaconda Prompt" Shortcut:
@REM %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@REM MakeAnacondaPromptShortcutForCondaEnvironment.bat %curr_conda_env_name%
call MakeAnacondaPromptShortcutForCondaEnvironment.bat %curr_conda_env_name%
echo "done with Anaconda prompt shortcut"

GOTO End1

:No1
  ECHO No param 1
GOTO End1

:End1
	echo "done with all."