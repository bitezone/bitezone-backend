docker stop bitezone-backend-service
docker rm bitezone-backend-service
docker build -t bitezone-backend .
docker run  -p 7779:8000 --name bitezone-backend-service bitezone-backend