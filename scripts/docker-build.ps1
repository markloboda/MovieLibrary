Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

docker build -t login-register-service:latest ..\src\login_register_service\
docker build -t browse-library-service:latest ..\src\browse_library_service\
docker build -t watchlist-watched-service:latest ..\src\watchlist_watched_service\