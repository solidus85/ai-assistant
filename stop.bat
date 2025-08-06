@echo off
echo Stopping AI Assistant container...
docker-compose down

echo.
echo Container stopped successfully.
echo.
echo Optional cleanup commands:
echo   - Remove all stopped containers: docker container prune
echo   - Remove unused networks: docker network prune
echo   - Remove unused images: docker image prune
echo   - Remove everything unused: docker system prune
echo.
pause