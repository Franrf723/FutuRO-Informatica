@echo off
:: Color verde para que parezca hacker (opcional)
color 0A

echo ==========================================
echo    AUTOMATIZADOR DE SUBIDA A GITHUB
echo ==========================================
echo.

:: Muestra qué archivos han cambiado
git status
echo.
echo ------------------------------------------

:: Pide el mensaje por teclado
set /p mensaje="Escribe el mensaje del commit: "

:: Ejecuta la secuencia sagrada de 3 pasos
git add .
git commit -m "%mensaje%"
git push

echo.
echo ==========================================
echo    PROCESO FINALIZADO
echo ==========================================
:: El pause es vital para que la ventana no se cierre y puedas leer si hubo errores
pause