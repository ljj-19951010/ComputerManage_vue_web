/*
 Navicat Premium Data Transfer

 Source Server         : fastapi
 Source Server Type    : MySQL
 Source Server Version : 80043
 Source Host           : localhost:3306
 Source Schema         : computer_manage

 Target Server Type    : MySQL
 Target Server Version : 80043
 File Encoding         : 65001

 Date: 26/05/2026 10:57:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admins
-- ----------------------------
DROP TABLE IF EXISTS `admins`;
CREATE TABLE `admins`  (
  `id` int unsigned NOT NULL COMMENT '用户ID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '账号',
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'bcrypt密码哈希',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮箱地址',
  `is_supper` tinyint(0) NOT NULL DEFAULT 0 COMMENT '角色:1管理员0普通用户',
  `is_active` tinyint(0) NOT NULL DEFAULT 1 COMMENT '状态:激活1未激活0',
  `is_delete` tinyint(0) NOT NULL DEFAULT 0 COMMENT '删除1 未删除0',
  `last_login_at` datetime(0) NULL DEFAULT NULL COMMENT '最后登录时间',
  `created_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admins
-- ----------------------------
INSERT INTO `admins` VALUES (9, 'user', 'scrypt:32768:8:1$FE2Cl1oM4SoJ06iO$714c4608b0dd4f1c24df39214d7ef7588409e1ad6bdc6ea5798da5454b40177e161359d899b989d35ea7ec2a946bb45f413a7a78b16e5c31bea412abbefb0eb2', 'user@system.com', 0, 1, 0, NULL, '2026-05-20 14:09:33', '2026-05-20 14:26:35');
INSERT INTO `admins` VALUES (10, 'admin', 'scrypt:32768:8:1$WYEeZ7DlxB65PnBY$bff0b90605cad6723148d25dade1337ef2ef8aea3f897bf01bbf95fe78266bcaa8ffc606e2b629dfa253c314c441e2a43d9b5258cca9d00c846a000699fba2bc', 'admin@system.com', 1, 1, 0, '2026-05-22 16:34:13', '2026-05-20 14:09:33', '2026-05-22 16:34:13');
INSERT INTO `admins` VALUES (11, 'test', 'scrypt:32768:8:1$1k6IeuYTUxLA7Z6B$1e6ce271897cdaba6c4e6878b0ff59e75a157e7cc246eb794414a3f5e3c14d162d9f487080af47063a566ff5bedae60ae0f44458473c53425ef9b01d348853eb', 'test@example.com', 0, 0, 1, NULL, '2026-05-20 15:50:30', '2026-05-22 16:29:34');
INSERT INTO `admins` VALUES (12, 'ljj', 'scrypt:32768:8:1$JkOqviP6fQra5aq7$feba31e42e8553f3812ab06745430ba8cbed2823c1aad3e78a9428d3a89949c173e4b61f58534eaaf644e75461a882e88419bc8197afe97f6adfc275b79b60db', 'ljj@system.com', 1, 1, 0, '2026-05-22 17:17:10', '2026-05-22 08:59:01', '2026-05-22 17:17:10');
INSERT INTO `admins` VALUES (13, 'china', 'scrypt:32768:8:1$6VI2RH40peUQ8ysl$3b4ac4adec7afc3e22438eee9dcc7f874bff3e98204a7bae6b9fb80f861ced4cd6db2d04529005f4526be20e1f3b7a1fa9b675649bf866a53556e0fcb9d64f20', 'china@example.com', 1, 1, 0, NULL, '2026-05-26 02:43:13', '2026-05-26 10:44:23');
INSERT INTO `admins` VALUES (14, 'china1', 'scrypt:32768:8:1$lCSft9R8Y71BkgH2$9742b31c34ded8d8d55854a32e0df9bc4f6d2501fe333064d553d183235d87f2245f12056cf7a400eeac6fc5424bdf75d7aa3f01c89b7484547e2829c8a11fbd', 'china1@example.com', 0, 1, 0, NULL, '2026-05-26 02:43:13', '2026-05-26 10:47:55');

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version`  (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('989a67ada6d6');

-- ----------------------------
-- Table structure for asset_logs
-- ----------------------------
DROP TABLE IF EXISTS `asset_logs`;
CREATE TABLE `asset_logs`  (
  `id` bigint unsigned NOT NULL,
  `asset_type` enum('computer','monitor') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '资产类型',
  `asset_id` int unsigned NOT NULL COMMENT '资产ID',
  `action` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '操作类型：assign/reclaim/repair/retire/update/create/delete',
  `old_value` json NULL COMMENT '变更前的关键字段（如user_id, status）',
  `new_value` json NULL COMMENT '变更后的关键字段',
  `operator_id` int unsigned NOT NULL COMMENT '操作人ID',
  `operator_type` enum('admin','user') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '操作人类型',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '备注',
  `created_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_asset`(`asset_type`, `asset_id`) USING BTREE,
  INDEX `idx_operator`(`operator_id`, `operator_type`) USING BTREE,
  INDEX `idx_created_at`(`created_at`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '资产操作日志表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of asset_logs
-- ----------------------------
INSERT INTO `asset_logs` VALUES (2, 'computer', 12, 'add', 'null', '{\"asset_tag\": \"MDPI-TZ-LAPTOP-2027\", \"serial_number\": \"PW0MTRA7\"}', 11, 'user', '用户test添加资产编号为MDPI-TZ-LAPTOP-2027的电脑', '2026-05-22 11:29:30');
INSERT INTO `asset_logs` VALUES (4, 'computer', 12, 'update', '{\"user_id\": null}', '{\"user_id\": 15}', 11, 'user', '用户test更新电脑MDPI-TZ-LAPTOP-2027信息', '2026-05-22 12:06:29');
INSERT INTO `asset_logs` VALUES (6, 'computer', 13, 'delete', 'null', '{\"deleted_at\": \"2026-05-22T13:34:29.289057\"}', 10, 'admin', '用户admin删除了资产编号为MDPI-TZ-LAPTOP-2028的电脑', '2026-05-22 13:34:29');
INSERT INTO `asset_logs` VALUES (8, 'monitor', 6, 'add', 'null', '{\"ass_tag\": \"MDPI-TZ-LCD-807\", \"serial_number\": \"BZUUH4TR608798\"}', 11, 'user', '用户test添加资产编号为MDPI-TZ-LCD-807的显示器', '2026-05-22 14:45:47');
INSERT INTO `asset_logs` VALUES (9, 'monitor', 7, 'add', 'null', '{\"ass_tag\": \"MDPI-TZ-LCD-807\", \"serial_number\": \"BZUUH4TR608798\"}', 11, 'user', '用户test添加资产编号为MDPI-TZ-LCD-807的显示器', '2026-05-22 14:47:54');
INSERT INTO `asset_logs` VALUES (10, 'monitor', 8, 'add', 'null', '{\"ass_tag\": \"MDPI-TZ-LCD-015\", \"serial_number\": \"WDDA1752003586KKD\"}', 11, 'user', '用户test添加资产编号为MDPI-TZ-LCD-015的显示器', '2026-05-22 14:51:49');
INSERT INTO `asset_logs` VALUES (13, 'monitor', 10, 'update', '{\"remark\": \"test\", \"status\": \"available\"}', '{\"remark\": \"测试数据已标记为删除\", \"status\": \"deleted\"}', 11, 'user', '用户test更新资产编号为MDPI-TZ-LCD-0122的信息', '2026-05-22 15:15:31');
INSERT INTO `asset_logs` VALUES (14, 'monitor', 1, 'delete', 'null', '{\"deleted_at\": \"2026-05-22T16:23:19.998478\"}', 10, 'admin', '用户admin删除资产编号为MDPI-TZ-LCD-001的信息', '2026-05-22 16:23:20');

-- ----------------------------
-- Table structure for brands
-- ----------------------------
DROP TABLE IF EXISTS `brands`;
CREATE TABLE `brands`  (
  `id` int unsigned NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '品牌名称',
  `created_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '品牌表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of brands
-- ----------------------------
INSERT INTO `brands` VALUES (1, 'Acer', '2026-05-20 09:22:43', '2026-05-20 09:22:43');
INSERT INTO `brands` VALUES (2, 'Dell', '2026-05-20 09:22:50', '2026-05-20 09:22:50');
INSERT INTO `brands` VALUES (3, 'HP', '2026-05-20 09:23:01', '2026-05-20 09:23:01');
INSERT INTO `brands` VALUES (4, 'Lenovo', '2026-05-20 09:23:06', '2026-05-20 09:23:06');
INSERT INTO `brands` VALUES (5, 'HUAWEI', '2026-05-20 09:23:31', '2026-05-20 09:23:31');
INSERT INTO `brands` VALUES (6, 'MacBookAir', '2026-05-20 09:24:25', '2026-05-20 09:24:25');
INSERT INTO `brands` VALUES (7, '优派', '2026-05-20 09:41:54', '2026-05-20 09:41:54');
INSERT INTO `brands` VALUES (8, 'PHILIPS', '2026-05-20 09:41:57', '2026-05-20 09:41:57');
INSERT INTO `brands` VALUES (9, 'AOC', '2026-05-20 09:42:36', '2026-05-20 09:42:36');
INSERT INTO `brands` VALUES (10, 'Redmi', '2026-05-20 09:42:41', '2026-05-20 09:42:41');
INSERT INTO `brands` VALUES (11, 'Samsung', '2026-05-20 09:43:23', '2026-05-20 09:43:23');
INSERT INTO `brands` VALUES (12, '几硕', '2026-05-20 09:44:05', '2026-05-20 09:44:05');

-- ----------------------------
-- Table structure for computers
-- ----------------------------
DROP TABLE IF EXISTS `computers`;
CREATE TABLE `computers`  (
  `id` int unsigned NOT NULL,
  `asset_tag` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '资产编号',
  `serial_number` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '序列号',
  `user_id` int unsigned NULL COMMENT '当前使用者ID',
  `model_id` int unsigned NOT NULL COMMENT '型号ID',
  `status` enum('available','in_use','repair','retired','deleted') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'available' COMMENT '状态',
  `price` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '单价',
  `assigned_at` datetime(0) NULL DEFAULT NULL COMMENT '最近分配时间',
  `purchase_date` date NULL DEFAULT NULL COMMENT '购买日期',
  `warranty_end` date NULL DEFAULT NULL COMMENT '保修截止',
  `remark` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '备注',
  `created_at` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  `deleted_at` datetime(0) NULL DEFAULT NULL COMMENT '软删除时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_asset_tag`(`asset_tag`) USING BTREE,
  UNIQUE INDEX `uk_serial_number`(`serial_number`) USING BTREE,
  INDEX `idx_model_id`(`model_id`) USING BTREE,
  INDEX `idx_user_id`(`user_id`) USING BTREE,
  INDEX `idx_status`(`status`) USING BTREE,
  INDEX `idx_deleted_at`(`deleted_at`) USING BTREE,
  CONSTRAINT `fk_computer_model` FOREIGN KEY (`model_id`) REFERENCES `models` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_computer_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '电脑资产表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of computers
-- ----------------------------
INSERT INTO `computers` VALUES (1, 'MDPI-TZ-LAPTOP-001', 'NXMV2CN0035430381E3400', NULL, 1, 'retired', '4000', NULL, NULL, NULL, '已报废', '2026-05-20 10:16:27', '2026-05-21 15:55:34', '2022-12-01 10:16:56');
INSERT INTO `computers` VALUES (2, 'MDPI-TZ-LAPTOP-002', 'NXMV2CN003517032013400', NULL, 1, 'retired', '4000', NULL, NULL, NULL, '已报废', '2026-05-20 10:17:06', '2026-05-21 15:55:38', '2022-12-01 10:16:56');
INSERT INTO `computers` VALUES (3, 'MDPI-TZ-LAPTOP-016', '3JJ8QJ2', 4, 16, 'available', '5699', NULL, NULL, NULL, NULL, '2026-05-20 10:18:42', '2026-05-20 10:19:58', NULL);
INSERT INTO `computers` VALUES (4, 'MDPI-TZ-LAPTOP-007', 'NXMV2CN00351608CEC3400', NULL, 1, 'retired', '4000', NULL, '2026-05-21', '2027-05-21', '已报废', '2026-05-21 15:54:55', '2026-05-21 15:55:52', NULL);
INSERT INTO `computers` VALUES (5, 'MDPI-TZ-LAPTOP-008', 'NXMV2CN00351703FC43400', NULL, 1, 'retired', '4000', NULL, '2020-05-21', '2021-05-21', '已报废', '2026-05-21 15:57:18', '2026-05-21 15:57:18', NULL);
INSERT INTO `computers` VALUES (8, 'MDPI-TZ-LAPTOP-1417', '36XBB24527801211', 14, 46, 'in_use', '4000', NULL, '2025-08-26', '2026-08-27', NULL, '2026-05-21 16:07:27', '2026-05-21 16:07:27', NULL);
INSERT INTO `computers` VALUES (12, 'MDPI-TZ-LAPTOP-2027', 'PW0MTRA7', 15, 42, 'available', '5699', NULL, '2026-02-07', '2028-02-08', NULL, '2026-05-22 11:29:30', '2026-05-22 12:06:29', NULL);
INSERT INTO `computers` VALUES (13, 'MDPI-TZ-LAPTOP-2028', 'UND6MCQ00251300F1B1W01', NULL, 1, 'deleted', NULL, NULL, NULL, NULL, NULL, '2026-05-22 12:15:51', '2026-05-22 13:35:13', '2026-05-22 13:35:14');

-- ----------------------------
-- Table structure for departments
-- ----------------------------
DROP TABLE IF EXISTS `departments`;
CREATE TABLE `departments`  (
  `id` int unsigned NOT NULL COMMENT '科室ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '科室名称',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '科室邮箱',
  `remark` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '备注',
  `status` tinyint(0) NOT NULL DEFAULT 1 COMMENT '状态：1-启用，0-停用',
  `created_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新时间',
  `deleted_at` datetime(0) NULL DEFAULT NULL COMMENT '软删除时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_name`(`name`) USING BTREE,
  INDEX `idx_status`(`status`) USING BTREE,
  INDEX `idx_deleted_at`(`deleted_at`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '科室表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of departments
-- ----------------------------
INSERT INTO `departments` VALUES (1, '1科', NULL, NULL, 1, '2026-05-19 17:08:40', '2026-05-19 17:08:40', NULL);
INSERT INTO `departments` VALUES (2, 'Cells', 'cells@mdpi.com', NULL, 1, '2026-05-20 10:09:52', '2026-05-20 10:14:14', NULL);
INSERT INTO `departments` VALUES (3, 'Social Sciences', 'social@mdpi.com', NULL, 1, '2026-05-20 10:14:09', '2026-05-20 10:14:09', NULL);
INSERT INTO `departments` VALUES (4, 'Communications & Marketing (China)', 'communications@mdpi.com', NULL, 1, '2026-05-20 10:19:46', '2026-05-20 10:19:46', NULL);
INSERT INTO `departments` VALUES (5, 'Mechanical Engineering', 'mechanical@mdpi.com', NULL, 1, '2026-05-21 09:12:52', '2026-05-21 09:12:52', NULL);
INSERT INTO `departments` VALUES (6, 'Sustainability', 'sustainability@mdpi.com', NULL, 1, '2026-05-22 11:39:20', '2026-05-22 11:39:20', NULL);

-- ----------------------------
-- Table structure for models
-- ----------------------------
DROP TABLE IF EXISTS `models`;
CREATE TABLE `models`  (
  `id` int unsigned NOT NULL,
  `brand_id` int unsigned NOT NULL COMMENT '品牌ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '型号名称',
  `category` enum('computer','monitor') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '适用设备类型',
  `created_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_brand_model_category`(`brand_id`, `name`, `category`) USING BTREE,
  CONSTRAINT `fk_model_brand` FOREIGN KEY (`brand_id`) REFERENCES `brands` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 89 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '型号表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of models
-- ----------------------------
INSERT INTO `models` VALUES (1, 1, 'Aspire E5-572G', 'computer', '2026-05-20 09:25:06', '2026-05-20 09:25:06');
INSERT INTO `models` VALUES (2, 1, 'E5-471 ZQ', 'computer', '2026-05-20 09:25:21', '2026-05-20 09:25:21');
INSERT INTO `models` VALUES (3, 1, 'TravelMate P248-MG', 'computer', '2026-05-20 09:25:34', '2026-05-20 09:25:34');
INSERT INTO `models` VALUES (4, 1, 'TravelMate P249-MG', 'computer', '2026-05-20 09:25:48', '2026-05-20 09:25:48');
INSERT INTO `models` VALUES (5, 1, 'FUN-S40-51-54WR', 'computer', '2026-05-20 09:26:11', '2026-05-20 09:26:11');
INSERT INTO `models` VALUES (6, 1, 'EX215-51G-59WK', 'computer', '2026-05-20 09:26:23', '2026-05-20 09:26:23');
INSERT INTO `models` VALUES (7, 1, 'Extensa 215-53G', 'computer', '2026-05-20 09:26:50', '2026-05-20 09:26:50');
INSERT INTO `models` VALUES (8, 1, 'funN20C4', 'computer', '2026-05-20 09:27:09', '2026-05-20 09:27:09');
INSERT INTO `models` VALUES (9, 1, 'EX214-52-59W3', 'computer', '2026-05-20 09:27:22', '2026-05-20 09:27:22');
INSERT INTO `models` VALUES (10, 1, ' EX214-53-56PK', 'computer', '2026-05-20 09:27:52', '2026-05-20 09:27:52');
INSERT INTO `models` VALUES (11, 1, 'SFL14-71', 'computer', '2026-05-20 09:28:15', '2026-05-20 09:28:15');
INSERT INTO `models` VALUES (12, 1, 'AL14-72', 'computer', '2026-05-20 09:28:36', '2026-05-20 09:28:36');
INSERT INTO `models` VALUES (13, 1, 'N23J5', 'computer', '2026-05-20 09:28:42', '2026-05-20 09:28:42');
INSERT INTO `models` VALUES (14, 1, 'S14-75L-5GU3', 'computer', '2026-05-20 09:28:57', '2026-05-20 09:28:57');
INSERT INTO `models` VALUES (15, 2, 'INSPIRON 7460', 'computer', '2026-05-20 09:29:48', '2026-05-20 09:29:48');
INSERT INTO `models` VALUES (16, 2, '7570', 'computer', '2026-05-20 09:30:02', '2026-05-20 09:30:02');
INSERT INTO `models` VALUES (17, 2, 'Inspiron 5509', 'computer', '2026-05-20 09:30:29', '2026-05-20 09:30:29');
INSERT INTO `models` VALUES (18, 2, '成就5000', 'computer', '2026-05-20 09:30:51', '2026-05-20 09:30:51');
INSERT INTO `models` VALUES (19, 2, 'Vostro 14-3400', 'computer', '2026-05-20 09:31:05', '2026-05-20 09:31:05');
INSERT INTO `models` VALUES (20, 3, 'HP15-be012TX', 'computer', '2026-05-20 09:31:46', '2026-05-20 09:31:46');
INSERT INTO `models` VALUES (21, 3, 'ZHAN 66 Pro 14 G5', 'computer', '2026-05-20 09:32:37', '2026-05-20 09:32:37');
INSERT INTO `models` VALUES (22, 4, 'ideapad-310', 'computer', '2026-05-20 09:33:14', '2026-05-20 09:33:14');
INSERT INTO `models` VALUES (23, 4, 'v110', 'computer', '2026-05-20 09:33:26', '2026-05-20 09:33:26');
INSERT INTO `models` VALUES (24, 4, 'ThinkPad E40', 'computer', '2026-05-20 09:33:39', '2026-05-20 09:33:39');
INSERT INTO `models` VALUES (25, 4, 'X270-20K6A00ECD', 'computer', '2026-05-20 09:33:54', '2026-05-20 09:33:54');
INSERT INTO `models` VALUES (26, 4, 'V130-14IKB', 'computer', '2026-05-20 09:34:10', '2026-05-20 09:34:10');
INSERT INTO `models` VALUES (27, 4, 'NEW14-2019', 'computer', '2026-05-20 09:34:21', '2026-05-20 09:34:21');
INSERT INTO `models` VALUES (28, 4, 'V720-14IKB', 'computer', '2026-05-20 09:34:34', '2026-05-20 09:34:34');
INSERT INTO `models` VALUES (29, 4, '小新Air13', 'computer', '2026-05-20 09:34:57', '2026-05-20 09:34:57');
INSERT INTO `models` VALUES (30, 4, '小新AIR-15 2019', 'computer', '2026-05-20 09:35:08', '2026-05-20 09:35:08');
INSERT INTO `models` VALUES (31, 4, 'Thinkpad X13 Gen1 20T2-A006CD', 'computer', '2026-05-20 09:35:25', '2026-05-20 09:35:25');
INSERT INTO `models` VALUES (32, 4, 'ThinkPadE14', 'computer', '2026-05-20 09:35:46', '2026-05-20 09:35:46');
INSERT INTO `models` VALUES (33, 4, 'ThinkPad X1 Carbon 2022', 'computer', '2026-05-20 09:36:01', '2026-05-20 09:36:01');
INSERT INTO `models` VALUES (34, 4, 'Yoga Pro14s ', 'computer', '2026-05-20 09:36:12', '2026-05-20 09:36:12');
INSERT INTO `models` VALUES (35, 4, 'ThinkBook14', 'computer', '2026-05-20 09:36:22', '2026-05-20 09:36:22');
INSERT INTO `models` VALUES (36, 4, 'ThinkBook 14 Gen5+ IRH', 'computer', '2026-05-20 09:36:39', '2026-05-20 09:36:39');
INSERT INTO `models` VALUES (37, 3, 'ProBook 440 14 inch G10', 'computer', '2026-05-20 09:36:54', '2026-05-20 09:36:54');
INSERT INTO `models` VALUES (38, 4, 'ThinkBook 14 G6+ IMH', 'computer', '2026-05-20 09:37:09', '2026-05-20 09:37:09');
INSERT INTO `models` VALUES (42, 4, 'ThinkBook 14 G8 IAL', 'computer', '2026-05-20 09:37:50', '2026-05-20 09:37:50');
INSERT INTO `models` VALUES (43, 4, '小新14pro', 'computer', '2026-05-20 09:38:12', '2026-05-20 09:38:12');
INSERT INTO `models` VALUES (45, 5, 'MateBook 14', 'computer', '2026-05-20 09:39:10', '2026-05-20 09:39:10');
INSERT INTO `models` VALUES (46, 5, 'MateBook D 14 2024', 'computer', '2026-05-20 09:39:40', '2026-05-20 09:39:40');
INSERT INTO `models` VALUES (47, 6, 'MacBookAir13', 'computer', '2026-05-20 09:40:26', '2026-05-20 09:40:26');
INSERT INTO `models` VALUES (48, 7, 'VA2349 Series', 'monitor', '2026-05-20 09:44:47', '2026-05-20 09:44:47');
INSERT INTO `models` VALUES (51, 7, 'VA2478-H-2', 'monitor', '2026-05-20 09:46:11', '2026-05-20 09:46:11');
INSERT INTO `models` VALUES (52, 8, '245S9RB/93', 'monitor', '2026-05-20 09:46:47', '2026-05-20 09:46:47');
INSERT INTO `models` VALUES (53, 8, '246E9QHSW', 'monitor', '2026-05-20 09:47:19', '2026-05-20 09:47:19');
INSERT INTO `models` VALUES (54, 8, '243S7', 'monitor', '2026-05-20 09:47:29', '2026-05-20 09:47:29');
INSERT INTO `models` VALUES (56, 8, '237-e7', 'monitor', '2026-05-20 09:48:01', '2026-05-20 09:48:01');
INSERT INTO `models` VALUES (57, 8, '247E7', 'monitor', '2026-05-20 09:48:22', '2026-05-20 09:48:22');
INSERT INTO `models` VALUES (58, 8, 'Philips 233E4', 'monitor', '2026-05-20 09:48:34', '2026-05-20 09:48:34');
INSERT INTO `models` VALUES (59, 8, 'PHL 234E5', 'monitor', '2026-05-20 09:48:53', '2026-05-20 09:48:53');
INSERT INTO `models` VALUES (61, 8, 'hwv9190t', 'monitor', '2026-05-20 09:49:18', '2026-05-20 09:49:18');
INSERT INTO `models` VALUES (62, 8, 'PHL 240i5', 'monitor', '2026-05-20 09:49:33', '2026-05-20 09:49:33');
INSERT INTO `models` VALUES (64, 8, 'Philips 226VL', 'monitor', '2026-05-20 09:50:35', '2026-05-20 09:50:35');
INSERT INTO `models` VALUES (65, 9, 'VA2349 Series', 'monitor', '2026-05-20 09:51:01', '2026-05-20 09:51:01');
INSERT INTO `models` VALUES (66, 9, '2476WM', 'monitor', '2026-05-20 09:51:15', '2026-05-20 09:51:15');
INSERT INTO `models` VALUES (67, 9, '2470W', 'monitor', '2026-05-20 09:51:29', '2026-05-20 09:51:29');
INSERT INTO `models` VALUES (68, 9, 'I2490VXH/BS', 'monitor', '2026-05-20 09:52:34', '2026-05-20 09:52:34');
INSERT INTO `models` VALUES (69, 9, 'AOCI2490VXH/BS', 'monitor', '2026-05-20 09:54:45', '2026-05-20 09:54:45');
INSERT INTO `models` VALUES (70, 2, 'D2421H', 'monitor', '2026-05-20 09:55:15', '2026-05-20 09:55:15');
INSERT INTO `models` VALUES (71, 2, 'SE2422H', 'monitor', '2026-05-20 09:55:26', '2026-05-20 09:55:26');
INSERT INTO `models` VALUES (72, 2, 'SE2218HL', 'monitor', '2026-05-20 09:55:42', '2026-05-20 09:55:42');
INSERT INTO `models` VALUES (73, 2, 'SE2419HR', 'monitor', '2026-05-20 09:56:03', '2026-05-20 09:56:03');
INSERT INTO `models` VALUES (74, 2, 'IN2030M', 'monitor', '2026-05-20 09:56:37', '2026-05-20 09:56:37');
INSERT INTO `models` VALUES (75, 2, 'ST2320L', 'monitor', '2026-05-20 09:56:56', '2026-05-20 09:56:56');
INSERT INTO `models` VALUES (77, 2, 'E1909W', 'monitor', '2026-05-20 09:57:32', '2026-05-20 09:57:32');
INSERT INTO `models` VALUES (78, 2, 'E198WFP', 'monitor', '2026-05-20 09:57:43', '2026-05-20 09:57:43');
INSERT INTO `models` VALUES (79, 2, 'E2313H', 'monitor', '2026-05-20 09:58:02', '2026-05-20 09:58:02');
INSERT INTO `models` VALUES (80, 2, 'P2314H', 'monitor', '2026-05-20 09:58:16', '2026-05-20 09:58:16');
INSERT INTO `models` VALUES (81, 2, 'S2340L', 'monitor', '2026-05-20 09:59:17', '2026-05-20 09:59:17');
INSERT INTO `models` VALUES (82, 1, 'G226HQL', 'monitor', '2026-05-20 09:59:57', '2026-05-20 09:59:57');
INSERT INTO `models` VALUES (83, 1, 'S230HL', 'monitor', '2026-05-20 10:00:07', '2026-05-20 10:00:07');
INSERT INTO `models` VALUES (84, 1, 'K222HQL', 'monitor', '2026-05-20 10:00:27', '2026-05-20 10:00:27');
INSERT INTO `models` VALUES (85, 10, 'Redmi1A', 'monitor', '2026-05-20 10:01:41', '2026-05-20 10:01:41');
INSERT INTO `models` VALUES (86, 11, 'S24R352F', 'monitor', '2026-05-20 10:01:54', '2026-05-20 10:01:54');
INSERT INTO `models` VALUES (87, 11, 'S32AM700PC', 'monitor', '2026-05-20 10:02:07', '2026-05-20 10:02:07');
INSERT INTO `models` VALUES (88, 12, 'FlipGo', 'monitor', '2026-05-20 10:02:51', '2026-05-20 10:02:51');

-- ----------------------------
-- Table structure for monitors
-- ----------------------------
DROP TABLE IF EXISTS `monitors`;
CREATE TABLE `monitors`  (
  `id` int unsigned NOT NULL,
  `asset_tag` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '资产编号',
  `serial_number` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '序列号',
  `model_id` int unsigned NOT NULL COMMENT '型号ID',
  `user_id` int unsigned NULL COMMENT '当前使用者ID',
  `status` enum('available','in_use','repair','retired','deleted') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'available' COMMENT '状态',
  `price` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '单价',
  `assigned_at` datetime(0) NULL DEFAULT NULL COMMENT '最近分配时间',
  `purchase_date` date NULL DEFAULT NULL COMMENT '购买日期',
  `warranty_end` date NULL DEFAULT NULL COMMENT '保修截止',
  `remark` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '备注',
  `created_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  `deleted_at` datetime(0) NULL DEFAULT NULL COMMENT '软删除时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_asset_tag`(`asset_tag`) USING BTREE,
  UNIQUE INDEX `uk_serial_number`(`serial_number`) USING BTREE,
  INDEX `idx_model_id`(`model_id`) USING BTREE,
  INDEX `idx_user_id`(`user_id`) USING BTREE,
  INDEX `idx_status`(`status`) USING BTREE,
  INDEX `idx_deleted_at`(`deleted_at`) USING BTREE,
  CONSTRAINT `fk_monitor_model` FOREIGN KEY (`model_id`) REFERENCES `models` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_monitor_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '显示器资产表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of monitors
-- ----------------------------
INSERT INTO `monitors` VALUES (1, 'MDPI-TZ-LCD-001', 'TT0144920052', 48, NULL, 'deleted', '799', NULL, NULL, NULL, 'IT库房', '2026-05-20 10:07:17', '2026-05-22 16:23:20', '2026-05-22 16:23:20');
INSERT INTO `monitors` VALUES (2, 'MDPI-TZ-LCD-002', 'CN-0HMJEV-74445-399-AMPL', 80, 2, 'available', '1299', NULL, NULL, NULL, '', '2026-05-20 10:08:18', '2026-05-22 14:48:17', NULL);
INSERT INTO `monitors` VALUES (3, 'MDPI-TZ-LCD-003', 'CN-0CXCW0-72872-29K-C0YM', 74, NULL, 'deleted', NULL, NULL, NULL, NULL, '已报废', '2026-05-20 10:11:23', '2026-05-22 16:23:31', '2020-12-20 10:11:13');
INSERT INTO `monitors` VALUES (4, 'MDPI-TZ-LCD-004', 'CN-0F534F-72872-942-3J3S', 74, NULL, 'deleted', NULL, NULL, NULL, NULL, '已报废', '2026-05-20 10:12:10', '2026-05-22 16:23:34', '2020-12-20 10:12:01');
INSERT INTO `monitors` VALUES (5, 'MDPI-TZ-LCD-006', 'CN-0HMJEV-74445-37R-APDF', 80, 3, 'available', '1299', NULL, NULL, NULL, NULL, '2026-05-20 10:14:53', '2026-05-20 10:14:53', NULL);
INSERT INTO `monitors` VALUES (7, 'MDPI-TZ-LCD-807', 'BZUUH4TR608798', 86, 14, 'available', '799', NULL, '2021-07-09', NULL, NULL, '2026-05-22 14:47:54', '2026-05-22 14:47:54', NULL);
INSERT INTO `monitors` VALUES (8, 'MDPI-TZ-LCD-015', 'WDDA1752003586KKD', 57, 1, 'available', '809', NULL, '2021-12-09', NULL, NULL, '2026-05-22 14:51:49', '2026-05-22 14:51:49', NULL);
INSERT INTO `monitors` VALUES (10, 'MDPI-TZ-LCD-0122', 'test', 11, NULL, 'deleted', NULL, NULL, NULL, NULL, '测试数据已标记为删除', '2026-05-22 15:09:36', '2026-05-22 15:15:31', NULL);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int unsigned NOT NULL COMMENT '用户ID',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '姓名',
  `english_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '英文名',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮箱',
  `department_id` int unsigned NULL COMMENT '所属科室ID',
  `status` tinyint(0) NOT NULL DEFAULT 1 COMMENT '状态：1-在职，0-离职',
  `created_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '入职时间',
  `updated_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  `deleted_at` datetime(0) NULL DEFAULT NULL COMMENT '软删除时间(离职时间)',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_name`(`name`) USING BTREE,
  UNIQUE INDEX `uk_email`(`email`) USING BTREE,
  INDEX `idx_department_id`(`department_id`) USING BTREE,
  INDEX `idx_status`(`status`) USING BTREE,
  INDEX `idx_deleted_at`(`deleted_at`) USING BTREE,
  CONSTRAINT `fk_user_department` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '员工表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, '董玉', 'Charlene Dong', 'charlene.dong@mdpi.com', 5, 1, '2026-05-19 17:08:48', '2026-05-21 10:59:53', '2026-05-21 10:59:11');
INSERT INTO `users` VALUES (2, '边秀芳', 'Xenia Bian', 'xenia.bian@mdpi.com', 2, 1, '2026-05-20 10:10:00', '2026-05-20 10:13:29', NULL);
INSERT INTO `users` VALUES (3, '孙云凤', 'Farrah Sun', 'farrah.sun@mdpi.com', 3, 1, '2026-05-20 10:13:06', '2026-05-21 11:00:08', '2026-05-21 10:59:58');
INSERT INTO `users` VALUES (4, '左巧艳', 'Qiaoyan Zuo', 'qiaoyan.zuo@mdpi.com', 4, 1, '2026-05-20 10:19:52', '2026-05-20 10:19:52', NULL);
INSERT INTO `users` VALUES (10, '姚雨辰', 'Yuchen Yao', 'yuchen.yao@mdpi.com', 4, 1, '2026-05-21 02:39:42', '2026-05-21 10:40:57', NULL);
INSERT INTO `users` VALUES (12, '王若曦', 'Ruoxi Wang', 'ruoxi.wang@mdpi.com', 4, 1, '2026-05-21 02:43:47', '2026-05-21 10:47:23', NULL);
INSERT INTO `users` VALUES (14, '陈钰涵', 'Yuhan Chen', 'yuhan.chen@mdpi.com', 1, 1, '2026-05-21 15:59:13', '2026-05-21 15:59:13', NULL);
INSERT INTO `users` VALUES (15, '李颖', 'Elaine Li', 'elaine.li@mdpi.com', 6, 1, '2026-05-22 11:39:32', '2026-05-22 11:39:32', NULL);

SET FOREIGN_KEY_CHECKS = 1;
