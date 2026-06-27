-- 🧊 3D Data Cube Relational Database Initialization Script
-- Target Engine: MariaDB 10.x+

CREATE DATABASE IF NOT EXISTS cube_management_db;
USE cube_management_db;

-- -----------------------------------------------------
-- Table 1: employees (The Parent Root Index)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `employees` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `employee_id_str` VARCHAR(50) NOT NULL UNIQUE,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table 2: compensation_matrix (Side 1 Expanded)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `compensation_matrix` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `employee_id` INT NOT NULL,
    `contract_year` INT NOT NULL,
    `btc_amount` DECIMAL(16,8) NOT NULL DEFAULT 0.00000000,
    `gold_ounces` DECIMAL(10,4) NOT NULL DEFAULT 0.0000,
    `silver_ounces` DECIMAL(10,4) NOT NULL DEFAULT 0.0000,
    `fiat_amount` DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    `fiat_ticker` VARCHAR(10) NOT NULL DEFAULT 'USD',
    `job_description` TEXT NULL,
    CONSTRAINT `fk_comp_employee` 
        FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table 3: treasury_allocation (Side 2)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `treasury_allocation` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `contract_year` INT NOT NULL,
    `target_currency` VARCHAR(20) NOT NULL,
    `liquidity_source` VARCHAR(100) NULL,
    `hedging_strategy` TEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table 4: operations_infrastructure (Side 3)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `operations_infrastructure` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `employee_id` INT NOT NULL,
    `hardware_tier` VARCHAR(50) NULL,
    `os_environment` VARCHAR(50) NULL,
    `infrastructure_access` VARCHAR(100) NULL,
    `annual_ops_budget` DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT `fk_ops_employee` 
        FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table 5: product_routing (Side 4)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `product_routing` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `employee_id` INT NOT NULL,
    `contract_year` INT NOT NULL,
    `primary_project` VARCHAR(100) NULL,
    `core_deliverable` TEXT NULL,
    `phase` VARCHAR(50) NULL,
    CONSTRAINT `fk_product_employee` 
        FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table 6: risk_compliance (Side 5)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `risk_compliance` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `employee_id` INT NOT NULL,
    `risk_category` VARCHAR(100) NULL,
    `threat_level` VARCHAR(20) NULL,
    `mitigation_protocol` TEXT NULL,
    CONSTRAINT `fk_risk_employee` 
        FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table 7: executive_kpis (Side 6)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `executive_kpis` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `employee_id` INT NOT NULL,
    `contract_year` INT NOT NULL,
    `q1_metric` VARCHAR(200) NULL,
    `q2_metric` VARCHAR(200) NULL,
    `q3_metric` VARCHAR(200) NULL,
    `q4_metric` VARCHAR(200) NULL,
    CONSTRAINT `fk_kpi_employee` 
        FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS application_audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_ip VARCHAR(50),
    action_performed VARCHAR(100),
    records_synthesized INT,
    saved_plan_text TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

