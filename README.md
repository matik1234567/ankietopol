# ankietopol
- install python > 3.9.x (select 'add to path' in installation options)\
https://www.python.org/downloads/

- open cmd and type following\
  pip install virtualenv\
  pip install virtualenvwrapper\
- create folder for project\
  open folder in cmd\
  type commands\
  virtualenv . -p python3\
  git clone (repo HTTP/SSH etc)\
  cd ankietopol\
  pip install -r requirements.txt
- run local server\
  open ankitopol directory in terminal and type: python manage.py runserver\
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
  pip install library_name\
