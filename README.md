list images

docker image list

build container

docker build -t flask_course_rest_api .

run container

docker run -p 5000:5000 flask_course_rest_api

run container with volume for fast reloading

docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask_course_rest_api