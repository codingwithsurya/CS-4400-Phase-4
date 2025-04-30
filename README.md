# CS-4400-Phase-4
cs 4400 phase 4 project shared github

## Instructions to setup your app

### Environment setup
```pip install django djangorestframework django-cors-headers```
### Start Server
``` python manage.py runserver ```

### Run migrations in case run into errors
```python manage.py makemigrations;```
```python manage.py migrate;```

### Setup DB Initially
```python manage.py inspectdb > models.py```

### Check which Apps are installed in settings
```python manage.py shell -c "from django.conf import settings; print(settings.INSTALLED_APPS)"```

### Current Admin Password
* Username: cs4400
* Password: data

### To reset password
```python manage.py createsuperuser```

### View Urls
* /alternative-airport/
* /flights-in-the-air/
* /flights-on-the-ground/
* /people-in-the-air/
* /people-on-the-ground/
* /route-summary/


## Technologies Used
- **Backend**: Django web framework with Python for form processing and server-side logic
- **Database**: MySQL database with custom stored procedures for all airport operations
- **Frontend**: Django templates with Bootstrap for responsive UI components

### Implementation Approach

1. **User Forms → Django Views**: Users enter data through HTML forms which are submitted to Django view functions. Django views receive HTTP requests triggered by user actions (e.g., form submissions, link clicks).

2. **Django Views → MySQL Stored Procedures**: The view functions validate form data and directly call the appropriate MySQL stored procedures with the submitted data.

3. **Results → User Interface**: After the database operation completes, Django shows a success message and redirects to the relevant page, or displays an error if something goes wrong.

### Misc

* [Google Doc](https://docs.google.com/document/d/1633UA-v3UTln1s15PQil72YFTob3CcfW-uWh_LKw8yI/edit?usp=sharing)
* [Video](https://www.youtube.com/watch?v=eXrwF4LXF5c)
* On minute 9 currently