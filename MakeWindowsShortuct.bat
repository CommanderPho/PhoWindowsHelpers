@REM Creates a Windows shortcut by generating a temporary Visual Basic .vbs file, running it, and then deleting it to clean up.
@REM 2021-11-10 - Solution from https://stackoverflow.com/questions/30028709/how-do-i-create-a-shortcut-via-command-line-in-windows
@REM Requres no 3rd Party Dependencies, entirely self-contained
@REM Note that Visual Basic escapes double quotes using another double quote, hence the two quotes before and after  ""%USERPROFILE%/""
@REM 
set "curr_conda_env_name=NeuroPy"

@REM %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@REM "Jupyter-lab" Shortcut:
@REM %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
set "start_in_dir=%%HOMEPATH%%"
set "shortcut_target=C:\Users\Pho\anaconda3\python.exe"
set shortcut_arguments=C:\Users\Pho\anaconda3\cwp.py C:\Users\Pho\anaconda3\envs\%curr_conda_env_name% C:\Users\Pho\anaconda3\envs\%curr_conda_env_name%\python.exe C:\Users\Pho\anaconda3\envs\%curr_conda_env_name%\Scripts\jupyter-lab-script.py ""%%USERPROFILE%%/""
set "shortcut_name=(%curr_conda_env_name%) Jupyter-lab"
set "shortcut_icon=%USERPROFILE%\anaconda3\Menu\jupyter.ico"
set "shortcut_comment=%shortcut_name%"

@REM %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@REM "Anaconda Prompt" Shortcut:
@REM %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
set "start_in_dir=%%HOMEPATH%%"
set "shortcut_target=%windir%\System32\cmd.exe"
@REM Note that Visual Basic escapes double quotes using another double quote, hence the two quotes before and after  ""%USERPROFILE%/""
set shortcut_arguments=""/K"" C:\Users\Pho\anaconda3\Scripts\activate.bat C:\Users\Pho\anaconda3\envs\%curr_conda_env_name%
set "shortcut_name=(%curr_conda_env_name%) Anaconda Prompt"
set "shortcut_icon=%USERPROFILE%\anaconda3\Menu\Iconleak-Atrous-Console.ico"
set "shortcut_comment=%shortcut_name%"


@echo off
@REM cd c:\MyApp
@REM cd "%start_in_dir%"
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
@REM echo sLinkFile = "%userprofile%\Desktop\MyApp.lnk" >> CreateShortcut.vbs
echo sLinkFile = "%userprofile%\Desktop\%shortcut_name%.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
@REM echo oLink.TargetPath = "C:\MyApp\MyApp.bat" >> CreateShortcut.vbs
echo oLink.TargetPath = "%shortcut_target%" >> CreateShortcut.vbs
@REM oLink.Arguments = """File1.vbs"""
@REM echo oLink.Arguments = """%shortcut_arguments%""" >> CreateShortcut.vbs 
echo oLink.Arguments = "%shortcut_arguments%" >> CreateShortcut.vbs
@REM echo oLink.WorkingDirectory = "C:\MyApp" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%start_in_dir%" >> CreateShortcut.vbs
@REM echo oLink.Description = "My Application" >> CreateShortcut.vbs
echo oLink.Description = "%shortcut_comment%" >> CreateShortcut.vbs
@REM echo oLink.IconLocation = "C:\MyApp\MyApp48.bmp" >> CreateShortcut.vbs
echo oLink.IconLocation = "%shortcut_icon%" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs