# ankietopol
- install python > 3.9.x (select 'add to path' in installation options)
https://www.python.org/downloads/

- create folder
- open cmd\
  pip install virtualenv\
  pip install virtualenvwrapper\
  create folder for project
  open folder in cmd
  type commends
  
- go to cloned repository forlder in cmd
- type following commends
  virtualenv . -p python3
  git clone (repo HTTP/SSH etc)
  cd ankietopol
  pip install -r requirements.txt
- run local server

  in ankitopol directory type: python manage.py runserver
  
- after each github pull/clone
  pip install -r requirements.txt
- before each github push if libraries was added on you local machine
  pip freeze > requirements.txt
- library installation on local machine
  go to project directory and type
  .\Scripts\activate
  pip install library_name
  

