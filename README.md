## This is the application developed during this [course](https://www.udemy.com/course/rest-api-flask-and-python).

#### running the application locally

- flask run

#### docker commands

- list images
    - docker image list

- build container
    - docker build -t flask_course_rest_api .

- run container
    - docker run -p 5000:5000 flask_course_rest_api

- run container with volume for fast reloading
    - docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask_course_rest_api