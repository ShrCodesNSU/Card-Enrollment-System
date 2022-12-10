-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 10, 2022 at 04:45 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `metroraileticket`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `accId` int(255) NOT NULL,
  `NID` int(255) DEFAULT NULL,
  `DOB` timestamp(3) NOT NULL DEFAULT current_timestamp(3) ON UPDATE current_timestamp(3),
  `Gender` char(7) DEFAULT NULL,
  `Password1` varchar(16) DEFAULT NULL,
  `Username` varchar(255) DEFAULT NULL,
  `AccType` varchar(7) DEFAULT NULL,
  `PhoneNum1` int(11) DEFAULT NULL,
  `PhoneNum2` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`accId`, `NID`, `DOB`, `Gender`, `Password1`, `Username`, `AccType`, `PhoneNum1`, `PhoneNum2`) VALUES
(1, 1831100642, '2022-12-10 03:31:27.509', 'Male', '319C*wVD', 'AdminRaiyan', 'Admin', 1722465849, 1968628835),
(2, 1831100643, '2022-12-10 03:34:47.356', 'Male', '319C*wVD', 'AdminRaiyan1', 'Admin', 1722465850, 1968628837),
(3, 1831100644, '2022-12-10 03:34:47.356', 'Male', '319C*wVD', 'AdminRaiyan2', 'Admin', 1722465851, 1968628838),
(4, 1831100645, '2022-12-10 03:34:47.356', 'Male', '319C*wVD', 'AdminRaiyan3', 'Admin', 1722465852, 1968628838),
(5, 1831100646, '2022-12-10 03:34:47.356', 'Male', '319C*wVD', 'AdminRaiyan4', 'Admin', 1722465853, 1968628839);

-- --------------------------------------------------------

--
-- Table structure for table `accountstatus`
--

CREATE TABLE `accountstatus` (
  `accId` int(255) NOT NULL,
  `cardId` int(255) NOT NULL,
  `verifId` int(255) DEFAULT NULL,
  `numTrips` int(255) DEFAULT NULL,
  `expenditure` int(255) DEFAULT NULL,
  `balance` int(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `accountstatus`
--

INSERT INTO `accountstatus` (`accId`, `cardId`, `verifId`, `numTrips`, `expenditure`, `balance`) VALUES
(0, 0, 1, 5, 10000, 20000);

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `AccId` int(255) NOT NULL,
  `TripID` char(255) NOT NULL,
  `BookingNum` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `phone`
--

CREATE TABLE `phone` (
  `accId` int(255) NOT NULL,
  `phonenumber` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `transId` int(255) NOT NULL,
  `accId` int(255) DEFAULT NULL,
  `cardID` int(255) DEFAULT NULL,
  `amount` int(255) DEFAULT NULL,
  `transdate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `trip`
--

CREATE TABLE `trip` (
  `TripId` int(255) NOT NULL,
  `TripName` char(255) DEFAULT NULL,
  `tripDate` date DEFAULT NULL,
  `tripTime` time(3) DEFAULT NULL,
  `Dest` varchar(255) DEFAULT NULL,
  `Start` varchar(255) DEFAULT NULL,
  `AvailSeat` varchar(255) DEFAULT NULL,
  `TotSeat` int(255) DEFAULT NULL,
  `Cost` int(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `verification`
--

CREATE TABLE `verification` (
  `verfId` int(255) NOT NULL,
  `accId` int(255) DEFAULT NULL,
  `requestStat` char(255) DEFAULT NULL,
  `bioStat` char(255) DEFAULT NULL,
  `bioDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`accId`);

--
-- Indexes for table `accountstatus`
--
ALTER TABLE `accountstatus`
  ADD PRIMARY KEY (`accId`,`cardId`);

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`AccId`,`TripID`);

--
-- Indexes for table `phone`
--
ALTER TABLE `phone`
  ADD PRIMARY KEY (`accId`,`phonenumber`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`transId`);

--
-- Indexes for table `trip`
--
ALTER TABLE `trip`
  ADD PRIMARY KEY (`TripId`);

--
-- Indexes for table `verification`
--
ALTER TABLE `verification`
  ADD PRIMARY KEY (`verfId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `accId` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `transaction`
--
ALTER TABLE `transaction`
  MODIFY `transId` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `trip`
--
ALTER TABLE `trip`
  MODIFY `TripId` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `verification`
--
ALTER TABLE `verification`
  MODIFY `verfId` int(255) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
