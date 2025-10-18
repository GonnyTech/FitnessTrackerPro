@echo off
echo Building executable with PyInstaller...
python -m PyInstaller --onefile --windowed --icon=icon.ico --name=FitnessTrackerPro main.py

echo.
echo Creating release package...
if exist release rmdir /s /q release
mkdir release

echo.
echo Moving executable to release folder...
move dist\FitnessTrackerPro.exe release\

echo.
echo Creating installer script...
(
    echo @echo off
    echo.
    echo set INSTALL_DIR="%%LOCALAPPDATA%%\FitnessTrackerPro"
    echo echo Installing to: %%INSTALL_DIR%%
    echo.
    echo echo Removing previous installation (if any)...
    echo if exist %%INSTALL_DIR%% rmdir /s /q %%INSTALL_DIR%%
    echo.
    echo echo Creating application directory...
    echo mkdir %%INSTALL_DIR%%
    echo.
    echo echo Copying application files...
    echo copy "FitnessTrackerPro.exe" %%INSTALL_DIR%%
    echo.
    echo echo Creating Desktop Shortcut...
    echo set SCRIPT="%%TEMP%%\%%RANDOM%%.vbs"
    echo echo Set oWS = WScript.CreateObject^("WScript.Shell"^) ^> %%SCRIPT%%
    echo echo sLinkFile = "%%USERPROFILE%%\Desktop\FitnessTrackerPro.lnk" ^>^> %%SCRIPT%%
    echo echo Set oLink = oWS.CreateShortcut^(sLinkFile^) ^>^> %%SCRIPT%%
    echo echo oLink.TargetPath = %%INSTALL_DIR%%\FitnessTrackerPro.exe ^>^> %%SCRIPT%%
    echo echo oLink.IconLocation = %%INSTALL_DIR%%\FitnessTrackerPro.exe,0 ^>^> %%SCRIPT%%
    echo echo oLink.WorkingDirectory = %%INSTALL_DIR%% ^>^> %%SCRIPT%%
    echo echo oLink.Save ^>^> %%SCRIPT%%
    echo cscript /nologo %%SCRIPT%%
    echo del %%SCRIPT%%
    echo.
    echo echo Installation complete!
    echo echo You can find FitnessTrackerPro on your Desktop.
    echo echo.
    echo pause
) > release\install.bat

echo.
echo Cleaning up build files...
rmdir /s /q dist
rmdir /s /q build
del FitnessTrackerPro.spec

echo.
echo Build complete! 
echo The 'release' folder contains the application and an 'install.bat' script.
echo To install, run 'install.bat'.
echo.
pause 