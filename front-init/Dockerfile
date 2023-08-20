FROM python:3.11
ENV APP_HOME /web_app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "web_app.py"]