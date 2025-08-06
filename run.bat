@echo off
echo Stopping existing containers...
docker-compose down --remove-orphans

echo Cleaning up networks...
docker network prune -f 

echo Building and starting container...
docker-compose up -d --build

echo.
echo Waiting for container to start...
timeout /t 3 /nobreak > nul

echo.
echo Checking container status...
docker-compose ps

echo.
echo Checking logs (last 20 lines)...
docker-compose logs --tail=20

echo.
echo Application should be available at http://localhost:5000
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down
pause