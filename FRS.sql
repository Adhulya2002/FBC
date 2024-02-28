CREATE DATABASE IF NOT EXISTS `FRS` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use FRS;
CREATE TABLE IF NOT EXISTS `userdata` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(255) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    `phoneno` varchar(255) NOT NULL,   
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `record` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`dob` varchar(255) NOT NULL,
  	`pname` varchar(255) NOT NULL,
  	`age` varchar(3) NOT NULL,
    `gender` varchar(255) NOT NULL, 
	`phy` varchar(255) NOT NULL,
  	`uni` varchar(255) NOT NULL,
    `ex` varchar(255) NOT NULL,
    `in` varchar(255) NOT NULL,
	`death` varchar(255) NOT NULL,
  	`evidence` varchar(255) NOT NULL,
    `result` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `bookdata` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(255) NOT NULL,
  	`address` varchar(255) NOT NULL,
  	`forensicdetail` varchar(255) NOT NULL,  
    `time` varchar(255) NOT NULL,
    `pat_id` varchar(255),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `panel` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(255) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    `phoneno` varchar(255) NOT NULL,   
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

select * from bookdata;
