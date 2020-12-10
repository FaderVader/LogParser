@ECHO OFF
setlocal enableDelayedExpansion

for %%p in (
TX84402 TX82564 TX84398 TX80359 TX80360 TX84399 KX76767 TX80359 KX82337 AX76707 AX86504 AX86507 AX86502 AX86506 AX86501 AX86505 AX86499 AX86500
) do ( call :getlist %%p )

ECHO Cleaning up..
cd ..\logs\
del del *.txt

GOTO :END

:getlist
REM curl https://TX84399:5055/api/getlogs -k 
set client=%~1
set prefix=https://
set postfix=:5055/api/getlogs
set url=!prefix!!client!!postfix!

curl !url! -k --connect-timeout 2 --silent --output ..\logs\files-!client!.txt 
call :getfile !client! !url!
EXIT /B

:getfile
REM https://TX84399:5055/api/getlogs/file?filename=
set "amp=&"

set listname=%~1
set baseurl=%~2
set filearg=/file?filename=

set urllist=..\logs\files-!listname!.txt
for /f "tokens=*" %%a in (!urllist!) do (
	set fullpath=!baseurl!!filearg!%%a
	curl -k --connect-timeout 5 -o ..\logs\%%a !fullpath!
)
EXIT /B

:END
ECHO Done!