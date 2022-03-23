# ankietopol
- install python > 3.9.x (select 'add to path' in installation options)\
https://www.python.org/downloads/

- open cmd and type following\
  pip install virtualenv\
  pip install virtualenvwrapper
- create folder for project\
  open folder in cmd\
  type commands\
  virtualenv . -p python3\
  git clone (repo HTTP/SSH etc)\
  cd ankietopol\
  pip install -r requirements.txt
- run local server\
  open ankitopol directory in terminal and type\
  python manage.py runserver
- after each github pull/clone\
  .\Scripts\activate\
  cd ankietopol\
  pip install -r requirements.txt *make sure you have installed all necessary libraries for current version*
- before each github push if you added libraries
  .\Scripts\activate\
  cd ankietopol\
  pip freeze > requirements.txt
- library installation on local machine\
  .\Scripts\activate\
  pip install library_name
- for Patryk Gacek\
  python manage.py collectstatic\
- Database\
 postgreSQL with pgAdmin4
 https://www.enterprisedb.com/downloads/postgres-postgresql-downloads *install with default options selected*\
 https://stackoverflow.com/questions/11769860/connect-to-a-heroku-database-with-pgadmin *how to connect database with pgAdmin4*\
 Database diagram:https://app.quickdatabasediagrams.com/#/d/364WXS\
 
        'ENGINE': 'django.db.backends.mysql',\
        'NAME': 'ankietopol',\
        'HOST': 'database-ankietopol.c3fozusj0ema.us-east-1.rds.amazonaws.com',\
        'PORT': 3306,\
        'USER': 'admin',\
        'PASSWORD': 'e8b1816da4e7e49b4655a7b2efcc95c7'\
python manage.py makemigrations --name <table_name>
python manage.py migrate
-Superuser\
admin\
ankiet2022polslSuperJestesmy
