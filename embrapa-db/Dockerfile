FROM mongo:8.0.0-rc13-jammy

WORKDIR /localfiles

COPY . /localfiles/

COPY ./initialize.sh /docker-entrypoint-initdb.d/

RUN chmod u+x /docker-entrypoint-initdb.d/initialize.sh

EXPOSE 27017