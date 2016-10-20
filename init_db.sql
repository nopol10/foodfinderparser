CREATE DATABASE foodfinder;
CREATE USER 'foodfinder'@'localhost' IDENTIFIED BY 'foodfinder';
grant all privileges on foodfinder.* to 'foodfinder'@'localhost';

USE foodfinder;

CREATE TABLE `restaurants` (
      `restaurant_id` INT PRIMARY KEY AUTO_INCREMENT,
      `restaurant_name` varchar(256) NOT NULL,
      `country` varchar(256),
      `web_rating` FLOAT,
      `address` varchar(256),
      `average_price` FLOAT,
      `food_type` VARCHAR(256),
      `source_website` varchar(256)
) ENGINE=InnoDB;

