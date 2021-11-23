@REM Creates a Windows shortcut by generating a temporary Visual Basic .vbs file, running it, and then deleting it to clean up.
@REM 2021-11-10 - Solution from https://stackoverflow.com/questions/30028709/how-do-i-create-a-shortcut-via-command-line-in-windows
@REM Requres no 3rd Party Dependencies, entirely self-contained
@REM Note that Visual Basic escapes double quotes using another double quote, hence the two quotes before and after  ""%USERPROFILE%/""
@REM 
@REM Usage Examples: MakeJupyterLabShortcutForCondaEnvironment.bat PyQt6
@REM 	Example 2: MakeJupyterLabShortcutForCondaEnvironment.bat phoviz


@echo off
@REM Check for argument:
IF %1.==. GOTO No1
set arg1=%1
set "curr_conda_env_name=%arg1%"
@REM echo %curr_conda_env_name%

@REM %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@REM "Jupyter-lab" Shortcut:
@REM %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
set "start_in_dir=%%HOMEPATH%%"
set "shortcut_target=C:\Users\Pho\anaconda3\python.exe"
set shortcut_arguments=C:\Users\Pho\anaconda3\cwp.py C:\Users\Pho\anaconda3\envs\%curr_conda_env_name% C:\Users\Pho\anaconda3\envs\%curr_conda_env_name%\python.exe C:\Users\Pho\anaconda3\envs\%curr_conda_env_name%\Scripts\jupyter-lab-script.py ""%%USERPROFILE%%/""
set "shortcut_name=(%curr_conda_env_name%) Jupyter-lab"
set "shortcut_icon=%USERPROFILE%\anaconda3\Menu\jupyter.ico"
set "shortcut_comment=%shortcut_name%"

@echo off
@REM cd c:\MyApp
@REM cd "%start_in_dir%"
echo Set oWS = WScript.CreateObject("WScript.Shell") > TempCreateShortcut.vbs
@REM echo sLinkFile = "%userprofile%\Desktop\MyApp.lnk" >> TempCreateShortcut.vbs
@REM @REM Creates link on **User's Desktop**:
@REM echo sLinkFile = "%userprofile%\Desktop\%shortcut_name%.lnk" >> TempCreateShortcut.vbs

@REM Creates link in **Anaconda's Start Menu folder**:
@REM 	%APPDATA%\Microsoft\Windows\Start Menu\Programs		(e.g. C:\Users\Pho\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit))
echo sLinkFile = "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit)\%shortcut_name%.lnk" >> TempCreateShortcut.vbs

echo Set oLink = oWS.CreateShortcut(sLinkFile) >> TempCreateShortcut.vbs
@REM echo oLink.TargetPath = "C:\MyApp\MyApp.bat" >> TempCreateShortcut.vbs
echo oLink.TargetPath = "%shortcut_target%" >> TempCreateShortcut.vbs
@REM oLink.Arguments = """File1.vbs"""
@REM echo oLink.Arguments = """%shortcut_arguments%""" >> TempCreateShortcut.vbs 
echo oLink.Arguments = "%shortcut_arguments%" >> TempCreateShortcut.vbs
@REM echo oLink.WorkingDirectory = "C:\MyApp" >> TempCreateShortcut.vbs
echo oLink.WorkingDirectory = "%start_in_dir%" >> TempCreateShortcut.vbs
@REM echo oLink.Description = "My Application" >> TempCreateShortcut.vbs
echo oLink.Description = "%shortcut_comment%" >> TempCreateShortcut.vbs
@REM echo oLink.IconLocation = "C:\MyApp\MyApp48.bmp" >> TempCreateShortcut.vbs
echo oLink.IconLocation = "%shortcut_icon%" >> TempCreateShortcut.vbs
echo oLink.Save >> TempCreateShortcut.vbs
cscript TempCreateShortcut.vbs
del TempCreateShortcut.vbs

GOTO End1

:No1
  ECHO No param 1
GOTO End1

:End1
	@REM echo "done."


