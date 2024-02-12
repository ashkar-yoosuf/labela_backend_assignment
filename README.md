# labela_backend_assignment
E-Commerce webapp MVP

## Setup guide
- clone the repo using the following command:
    > git clone https://github.com/ashkar-yoosuf/labela_backend_assignment.git
- Go to the project folder using the following command:
    > cd labela_backend_assignment/
- Execute the following commands in the given order to get the app up and running (may need superuser permission):
    > docker-compose build --no-cache<br>
    docker-compose up -d

## Versions
- Python 3.9
- Django==4.1.1
- psycopg2-binary>=2.8
- djangorestframework==3.14.0
- sqlparse==0.4.2
- pandas==1.5.0

## Links
[Postman Collection](https://www.getpostman.com/collections/d484284ba1e6d7de5e95)<br>
[User stories and API endpoints](https://docs.google.com/document/d/1jSVEN6K-AmqfhiToekbeflu9WcOocKH2-0C5RrZ1Ce4/edit?usp=sharing)

## Notes
- Once the app is running test product records will be available.
- Use the following command to run the unit tests (may need superuser permission):
    > docker-compose run web python manage.py test
- Use the following command to stop the app (may need superuser permission):
    > docker-compose down
