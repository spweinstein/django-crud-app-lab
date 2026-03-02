CREATE DATABASE electronicscollector;

CREATE USER electronics_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE electronicscollector TO electronics_admin;
