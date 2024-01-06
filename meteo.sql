-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Sty 06, 2024 at 03:50 PM
-- Wersja serwera: 10.5.21-MariaDB-0+deb11u1
-- Wersja PHP: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `meteo`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `readings`
--

CREATE TABLE `readings` (
  `id` int(11) NOT NULL,
  `read_time` datetime NOT NULL DEFAULT current_timestamp(),
  `bme280_temperature` float DEFAULT NULL,
  `bme280_humidity` float DEFAULT NULL,
  `bme280_pressure` float DEFAULT NULL,
  `ds18b20_temperature` float DEFAULT NULL,
  `pms5003_pm_1_0` int(11) DEFAULT NULL,
  `pms5003_pm_2_5` int(11) DEFAULT NULL,
  `pms5003_pm_10` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `readings`
--
ALTER TABLE `readings`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `readings`
--
ALTER TABLE `readings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
