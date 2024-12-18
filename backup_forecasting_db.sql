-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 18, 2024 at 08:11 AM
-- Server version: 8.0.40-0ubuntu0.22.04.1
-- PHP Version: 8.1.2-1ubuntu2.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `forecasting_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `forecast_data`
--

CREATE TABLE `forecast_data` (
  `id` int NOT NULL,
  `date` date NOT NULL,
  `value` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `forecast_data`
--

INSERT INTO `forecast_data` (`id`, `date`, `value`) VALUES
(1, '2019-01-01', 34402),
(2, '2019-02-01', 18300),
(3, '2019-03-01', 41222),
(4, '2019-04-01', 34759),
(5, '2019-05-01', 36466),
(6, '2019-06-01', 63172),
(7, '2019-07-01', 32652),
(8, '2019-08-01', 47527),
(9, '2019-09-01', 50415),
(10, '2019-10-01', 59648),
(11, '2019-11-01', 68161),
(12, '2019-12-01', 49004),
(13, '2020-01-01', 105873),
(14, '2020-02-01', 100527),
(15, '2020-03-01', 87490),
(16, '2020-04-01', 55696),
(17, '2020-05-01', 68786),
(18, '2020-06-01', 89509),
(19, '2020-07-01', 101099),
(20, '2020-08-01', 94370),
(21, '2020-09-01', 98981),
(22, '2020-10-01', 92752),
(23, '2020-11-01', 93740),
(24, '2020-12-01', 117391),
(25, '2021-01-01', 111100),
(26, '2021-02-01', 111034),
(27, '2021-03-01', 113964),
(28, '2021-04-01', 108454),
(29, '2021-05-01', 128108),
(30, '2021-06-01', 133040),
(31, '2021-07-01', 89687),
(32, '2021-08-01', 88650),
(33, '2021-09-01', 112175),
(34, '2021-10-01', 142116),
(35, '2021-11-01', 149469),
(36, '2021-12-01', 168243),
(37, '2022-01-01', 168287),
(38, '2022-02-01', 161501),
(39, '2022-03-01', 226416),
(40, '2022-04-01', 119442),
(41, '2022-05-01', 218851),
(42, '2022-06-01', 159315),
(43, '2022-07-01', 160356),
(44, '2022-08-01', 132748),
(45, '2022-09-01', 126987),
(46, '2022-10-01', 159926),
(47, '2022-11-01', 167030),
(48, '2022-12-01', 180735),
(49, '2023-01-01', 217229),
(50, '2023-02-01', 147888),
(51, '2023-03-01', 148625),
(52, '2023-04-01', 164130),
(53, '2023-05-01', 189552),
(54, '2023-06-01', 177951),
(55, '2023-07-01', 148327),
(56, '2023-08-01', 108488),
(57, '2023-09-01', 103211),
(58, '2023-10-01', 107285),
(59, '2023-11-01', 109650),
(60, '2023-12-01', 151709);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `forecast_data`
--
ALTER TABLE `forecast_data`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `forecast_data`
--
ALTER TABLE `forecast_data`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
