FROM tiangolo/uwsgi-nginx-flask

COPY ./x628 /app
WORKDIR /app

RUN pip install wtforms \
&& pip install psycopg2 \
&& pip install psycopg2-binary 

CMD ["./run.sh"]
EXPOSE 8080