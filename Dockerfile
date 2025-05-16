FROM python:3.11.11

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#make the project dir
RUN mkdir userprofile

# # install dependencies
# RUN pip install --upgrade pip
# COPY ./requirements.txt /userprofile
# RUN pip install -r /userprofile/requirements.txt

# copy project
COPY ./userprofile /userprofile

RUN pip install -r /userprofile/requirements.txt

# Run Server
# CMD [ "fastapi", "dev", "/userprofile/main.py" ]