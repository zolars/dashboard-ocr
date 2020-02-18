CREATE DATABASE dashboard CHARACTER SET utf8 COLLATE utf8_general_ci;
USE dashboard;

/*
 Navicat MySQL Data Transfer

 Source Server         : Test
 Source Server Type    : MySQL
 Source Server Version : 50562
 Source Host           : localhost:3306
 Source Schema         : dashboard

 Target Server Type    : MySQL
 Target Server Version : 50562
 File Encoding         : 65001

 Date: 18/02/2020 13:01:53
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for devices_info
-- ----------------------------
DROP TABLE IF EXISTS `devices_info`;
CREATE TABLE `devices_info` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `type` int(11) NOT NULL,
  `unit` varchar(255) NOT NULL,
  `minimum` int(11) DEFAULT NULL,
  `maximum` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
