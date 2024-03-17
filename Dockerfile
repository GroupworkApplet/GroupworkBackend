# Django
FROM python:3.9-buster
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && apt-get install -y vim
WORKDIR /etc/uwsgi/django
RUN python3 -m pip install uwsgi uwsgi-tools -i https://pypi.tuna.tsinghua.edu.cn/simple/
ADD requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
ADD uwsgi.ini uwsgi.ini
ADD . /etc/uwsgi/django
EXPOSE 8084
CMD uwsgi --ini /etc/uwsgi/django/uwsgi.ini
