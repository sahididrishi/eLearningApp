
1. install all requirements using
pip install -r requirements.text

2.  activate the .venv / your virtual env

3. start redis-server ```redis-server``` 


4. run the server using ```daphne elearning.asgi:application```



## Test_----
### 1.coverage run --source='.' --omit='*/asgi.py,*/wsgi.py,*/manage.py' manage.py test   
### or 
### coverage run --source='.' manage.py test
### 2.coverage report
### 3.coverage html
