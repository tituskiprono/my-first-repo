-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema HOSP_DB
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema HOSP_DB
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `HOSP_DB` DEFAULT CHARACTER SET utf8 ;
USE `HOSP_DB` ;

-- -----------------------------------------------------
-- Table `HOSP_DB`.`USER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HOSP_DB`.`USER` (
  `USERID` INT NOT NULL,
  `USERNAME` VARCHAR(255) NOT NULL,
  `PASSWORD` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`USERID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HOSP_DB`.`HOSPITAL_DB`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HOSP_DB`.`HOSPITAL_DB` (
  `HOSPID` INT NOT NULL,
  `HOSPITALNAME` VARCHAR(45) NOT NULL,
  `PRACREGNO` VARCHAR(45) NOT NULL,
  `HOSPITAL_DBcol` VARCHAR(45) NULL,
  PRIMARY KEY (`HOSPID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HOSP_DB`.`PRACTIONER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HOSP_DB`.`PRACTIONER` (
  `ID` INT NOT NULL,
  `NAME` VARCHAR(45) NOT NULL,
  `PRACREGNO` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `PRACREGNO`
    FOREIGN KEY ()
    REFERENCES `HOSP_DB`.`HOSPITAL_DB` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
