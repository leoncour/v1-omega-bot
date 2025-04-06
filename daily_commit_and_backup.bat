@echo off
cd /d "C:\Users\allst\OneDrive\Desktop\trading\trading\new EA"

set "DATE=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%"
set "TIME=%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%"
set "ZIPFILE=backup_%DATE%_%TIME%.zip"
set "BACKUPFOLDER=backups"

git add .
git commit -m "Daily backup - %DATE%"

IF %ERRORLEVEL% EQU 0 (
    echo Committing successful. Creating backup zip...

    if not exist "%BACKUPFOLDER%" mkdir "%BACKUPFOLDER%"

    REM Create version.txt with commit hash and date
    for /f "tokens=* delims=" %%i in ('git log -1 --pretty^=format:"%%h - %%s"') do set "COMMIT=%%i"
    echo Date: %DATE% > version.txt
    echo Commit: %COMMIT% >> version.txt
    timeout /t 1 >nul

    REM Zip current folder including version.txt
    powershell -Command "Compress-Archive -Path '.', 'version.txt' -DestinationPath '%BACKUPFOLDER%\%ZIPFILE%' -Force"

    del version.txt

    REM Validate ZIP file creation
    if exist "%BACKUPFOLDER%\%ZIPFILE%" (
        echo Backup complete: %BACKUPFOLDER%\%ZIPFILE%
    ) else (
        echo Failed to create backup ZIP file.
        exit /b 1
    )

    REM Delete backups older than 30 days
    forfiles /p "%BACKUPFOLDER%" /m "backup_*.zip" /d -30 /c "cmd /c del @file"

) ELSE (
    echo No code changes detected today. Nothing to back up.
)

pause