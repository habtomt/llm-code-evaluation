`python

import os

from pathlib import Path

BASE_DIR =Path (__file__ ).resolve ().parent .parent

DEBUG =False

ALLOWED_HOSTS =['your_domain.com']

INSTALLED_APPS =[

...

]

DATABASES ={

'default':{

'ENGINE':'django.db.backends.postgresql',

'NAME':'your_db_name',

'USER':'your_db_user',

'PASSWORD':'your_db_password',

'HOST':'your_db_host',

'PORT':'your_db_port',

}

}

FROM python :3.8 -slim

WORKDIR /code

COPY ./code

RUN pip install -r requirements .txt

EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"]

eb init -p python -3.8 your -eb -environment -name

eb create your -application -name