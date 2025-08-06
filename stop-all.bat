@echo off
echo === Stopping ALL Docker containers and cleaning up ===
echo.

echo Stopping AI Assistant container...
docker-compose down

echo.
echo Stopping ALL running Docker containers...
docker stop $(docker ps -aq) 2>nul
if %errorlevel% neq 0 (
    echo No other containers running
)

echo.
echo Removing stopped containers...
docker container prune -f

echo.
echo Cleaning up unused networks...
docker network prune -f

echo.
echo Docker cleanup complete!
echo.
echo To also remove unused images, run: docker image prune
echo To remove everything unused (including volumes), run: docker system prune -a
echo.
pause