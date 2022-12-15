
CREATE TABLE `accounts` (
  `accId` int(255) NOT NULL,
  `NID` int(255) NOT NULL,
  `DOB` date DEFAULT NULL,
  `Gender` char(6) DEFAULT NULL,
  `Password1` varchar(16) NOT NULL,
  `Username` varchar(255) NOT NULL,
  `AccType` varchar(255) NOT NULL,
  `PhoneNum1` int(10) NOT NULL,
  `PhoneNum2` int(10) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL
) ;


INSERT INTO `accounts` (`accId`, `NID`, `DOB`, `Gender`, `Password1`, `Username`, `AccType`, `PhoneNum1`, `PhoneNum2`, `email`) VALUES
(1, 298424613, '0000-00-00', 'Male', '*6BB4837EB743291', 'Daniel K. Pemberton', 'user', 2147483647, 2147483647, 'boseto5479@nazyno.com'),
(2, 202562411, '1991-06-17', 'Male', '*6BB4837EB743291', 'Donny S. Hicks', 'user', 2147483647, 2147483647, 'nijim44167@randrai.com'),
(3, 215033233, '1994-04-17', 'FeMale', '*6BB4837EB743291', 'Kiley R. Smith', 'user', 2147483647, 2147483647, 'abc@xyz.com'),
(4, 561121135, '1966-01-29', 'FeMale', '*6BB4837EB743291', 'Donna W. Vandegrift', 'user', 2147483647, 2147483647, 'def@xyz.com'),
(5, 1831100642, '2000-01-07', 'Male', '*6BB4837EB743291', 'Md Raiyan Alam', 'Official', 2000017111, 2000017112, 'ghi@xyz.com');



CREATE TABLE `accountstatus` (
  `accId` int(255) NOT NULL,
  `cardId` int(255) NOT NULL,
  `verifId` int(255) NOT NULL,
  `numTrips` int(255) DEFAULT NULL,
  `expenditure` int(255) DEFAULT NULL,
  `balance` double(255,3) DEFAULT NULL
) ;



INSERT INTO `accountstatus` (`accId`, `cardId`, `verifId`, `numTrips`, `expenditure`, `balance`) VALUES
(1, 123, 1, 5, 1000, 9000.000),
(2, 124, 2, 6, 1100, 8900.000),
(3, 125, 3, 7, 1200, 8800.000),
(4, 126, 4, 8, 1300, 8700.000),
(5, 127, 5, 9, 1400, 8600.000);



CREATE TABLE `booking` (
  `accId` int(255) NOT NULL,
  `TripId` int(255) NOT NULL,
  `bookingNum` int(255) DEFAULT NULL
) ;


INSERT INTO `booking` (`accId`, `TripId`, `bookingNum`) VALUES
(1, 5, 123456),
(2, 4, 123457),
(3, 3, 123458),
(4, 2, 123459),
(5, 1, 123460);



CREATE TABLE `carddelivery` (
  `deliveryId` int(255) NOT NULL,
  `accId` int(255) NOT NULL,
  `verifId` int(255) NOT NULL,
  `delDate` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `delStat` varchar(255) DEFAULT NULL
); 


INSERT INTO `carddelivery` (`deliveryId`, `accId`, `verifId`, `delDate`, `delStat`) VALUES
(1, 1, 5, '0000-00-00 00:00:00', 'Pending'),
(2, 2, 4, '0000-00-00 00:00:00', 'Pending'),
(3, 3, 3, '0000-00-00 00:00:00', 'Pending'),
(4, 4, 2, '0000-00-00 00:00:00', 'Pending'),
(5, 5, 1, '0000-00-00 00:00:00', 'Pending');


CREATE TABLE `complaint` (
  `complaintId` int(11) NOT NULL,
  `accId` int(255) NOT NULL,
  `ComplaintText` text DEFAULT NULL
) ;



INSERT INTO `complaint` (`complaintId`, `accId`, `ComplaintText`) VALUES
(1, 1, 'Complain1. I hope this attributes works as a Paragraph attributes'),
(2, 2, 'Complain2. I hope this attributes works as a Paragraph attributes'),
(3, 3, 'Complain3. I hope this attributes works as a Paragraph attributes'),
(4, 4, 'Complain4. I hope this attributes works as a Paragraph attributes'),
(5, 5, 'Complain5. I hope this attributes works as a Paragraph attributes');



CREATE TABLE `phone` (
  `accId` int(255) NOT NULL,
  `phoneNumber` int(255) NOT NULL
) ;



INSERT INTO `phone` (`accId`, `phoneNumber`) VALUES
(1, 1720403937),
(2, 1720403938),
(3, 1720403939),
(4, 1720403940),
(5, 1720403941);



CREATE TABLE `trans` (
  `transId` int(255) NOT NULL,
  `accId` int(255) DEFAULT NULL,
  `cardID` int(255) NOT NULL,
  `transAmount` int(255) DEFAULT NULL,
  `transDate` timestamp(3) NOT NULL DEFAULT current_timestamp(3) ON UPDATE current_timestamp(3)
) ;



INSERT INTO `transactionTab` (`transId`, `accId`, `cardID`, `transAmount`, `transDate`) VALUES
(1, 1, 123, 1000, '2022-12-10 14:44:06.294'),
(2, 2, 124, 2000, '2022-12-10 14:44:06.294'),
(3, 3, 125, 3000, '2022-12-10 14:44:06.294'),
(4, 4, 126, 4000, '2022-12-10 14:44:06.294');



CREATE TABLE `trip` (
  `TripId` int(255) NOT NULL,
  `TripName` char(255) DEFAULT NULL,
  `tripTimenDate` timestamp(3) NULL DEFAULT NULL,
  `dest` varchar(255) DEFAULT NULL,
  `start` varchar(255) DEFAULT NULL,
  `availSeat` int(255) DEFAULT NULL,
  `totSeat` int(255) DEFAULT NULL,
  `cost` int(255) DEFAULT NULL
) ;



INSERT INTO `trip` (`TripId`, `TripName`, `tripTimenDate`, `dest`, `start`, `availSeat`, `totSeat`, `cost`) VALUES
(1, 'Uttara North - Uttara Center', NULL, 'Uttara North', 'Uttara Center', 1000, 1000, 20),
(2, 'Uttara Center - Uttara South', NULL, 'Uttara Center', 'Uttara South', 990, 1000, 20),
(3, 'Uttara South - Pallabi', NULL, 'Uttara South', 'Pallabi', 980, 1000, 30),
(4, 'Pallabi - Mirpur 11', NULL, 'Pallabi', 'Mirpur 11', 970, 1000, 30),
(5, 'Mirpur 11 - Mirpur 10', NULL, 'Mirpur 11', 'Mirpur 10', 960, 1000, 40);


CREATE TABLE `verification` (
  `verfId` int(255) NOT NULL,
  `accId` int(255) DEFAULT NULL,
  `requestStat` char(255) DEFAULT NULL,
  `bioStat` char(255) DEFAULT NULL,
  `bioDate` date DEFAULT NULL
) ;



INSERT INTO `verification` (`verfId`, `accId`, `requestStat`, `bioStat`, `bioDate`) VALUES
(1, 1, 'Approved', 'Approved', '2022-12-16'),
(2, 2, 'Pending', 'Pending', '2022-12-17'),
(3, 3, 'Approved', 'Approved', '2022-12-18'),
(4, 4, 'Rejected', 'Rejected', '2022-12-19'),
(5, 5, 'Approved', 'Pending', '2022-12-20');


ALTER TABLE `accounts`
  ADD PRIMARY KEY (`accId`);

ALTER TABLE `accountstatus`
  ADD PRIMARY KEY (`accId`,`cardId`);


ALTER TABLE `booking`
  ADD PRIMARY KEY (`accId`,`TripId`),
  ADD KEY `TripId` (`TripId`);


ALTER TABLE `carddelivery`
  ADD PRIMARY KEY (`deliveryId`),
  ADD KEY `accId` (`accId`);


ALTER TABLE `complaint`
  ADD PRIMARY KEY (`complaintId`),
  ADD KEY `accId` (`accId`);


ALTER TABLE `phone`
  ADD PRIMARY KEY (`accId`,`phoneNumber`);


ALTER TABLE `transaction`
  ADD PRIMARY KEY (`transId`);


ALTER TABLE `trip`
  ADD PRIMARY KEY (`TripId`);


ALTER TABLE `verification`
  ADD PRIMARY KEY (`verfId`);


ALTER TABLE `accounts`
  MODIFY `accId` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

ALTER TABLE `carddelivery`
  MODIFY `deliveryId` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;


ALTER TABLE `complaint`
  MODIFY `complaintId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;


ALTER TABLE `transaction`
  MODIFY `transId` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;


ALTER TABLE `trip`
  MODIFY `TripId` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

ALTER TABLE `verification`
  MODIFY `verfId` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

ALTER TABLE `accountstatus`
  ADD CONSTRAINT `accountstatus_ibfk_1` FOREIGN KEY (`accId`) REFERENCES `accounts` (`accId`);

ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`accId`) REFERENCES `accounts` (`accId`),
  ADD CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`TripId`) REFERENCES `trip` (`TripId`);

ALTER TABLE `carddelivery`
  ADD CONSTRAINT `carddelivery_ibfk_1` FOREIGN KEY (`accId`) REFERENCES `accounts` (`accId`);

ALTER TABLE `complaint`
  ADD CONSTRAINT `complaint_ibfk_1` FOREIGN KEY (`accId`) REFERENCES `accounts` (`accId`);

ALTER TABLE `phone`
  ADD CONSTRAINT `phone_ibfk_1` FOREIGN KEY (`accId`) REFERENCES `accounts` (`accId`);
COMMIT;
