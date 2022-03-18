-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 18 Mar 2022 pada 06.12
-- Versi server: 10.4.21-MariaDB
-- Versi PHP: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `stp`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `provinsi`
--

CREATE TABLE `provinsi` (
  `id` int(11) NOT NULL,
  `nama` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `provinsi`
--

INSERT INTO `provinsi` (`id`, `nama`) VALUES
(11, 'Aceh\r'),
(12, 'Sumatera Utara\r'),
(13, 'Sumatera Barat\r'),
(14, 'Riau\r'),
(15, 'Jambi\r'),
(16, 'Sumatera Selatan\r'),
(17, 'Bengkulu\r'),
(18, 'Lampung\r'),
(19, 'Kep. Bangka Belitung\r'),
(21, 'Kep. Riau\r'),
(31, 'Dki Jakarta\r'),
(32, 'Jawa Barat\r'),
(33, 'Jawa Tengah\r'),
(34, 'Di Yogyakarta\r'),
(35, 'Jawa Timur\r'),
(36, 'Banten\r'),
(51, 'Bali\r'),
(52, 'Nusa Tenggara Barat\r'),
(53, 'Nusa Tenggara Timur\r'),
(61, 'Kalimantan Barat\r'),
(62, 'Kalimantan Tengah\r'),
(63, 'Kalimantan Selatan\r'),
(64, 'Kalimantan Timur\r'),
(65, 'Kalimantan Utara\r'),
(71, 'Sulawesi Utara\r'),
(72, 'Sulawesi Tengah\r'),
(73, 'Sulawesi Selatan\r'),
(74, 'Sulawesi Tenggara\r'),
(75, 'Gorontalo\r'),
(76, 'Sulawesi Barat\r'),
(81, 'Maluku\r'),
(82, 'Maluku Utara\r'),
(91, 'Papua\r'),
(92, 'Papua Barat\r');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `provinsi`
--
ALTER TABLE `provinsi`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `provinsi`
--
ALTER TABLE `provinsi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=93;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
