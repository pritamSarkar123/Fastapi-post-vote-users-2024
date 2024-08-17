FROM python:3.10.5

WORKDIR /user/src/app 

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 


CMD [ "alembic", "upgrade", "head"]