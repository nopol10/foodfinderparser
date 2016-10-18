CREATE DATABASE foodfinder;
CREATE USER 'foodfinder'@'localhost' IDENTIFIED BY 'foodfinder';
grant all privileges on foodfinder.* to 'foodfinder'@'localhost';