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
-- Struktur dari tabel `kelompok__tani`
--

CREATE TABLE `kelompok__tani` (
  `id` bigint(20) NOT NULL,
  `nama` varchar(200) DEFAULT NULL,
  `no_sk` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `kelompok__tani`
--

INSERT INTO `kelompok__tani` (`id`, `nama`, `no_sk`) VALUES
(7317051001102, 'Anggeraja', '\r'),
(7317051001104, 'Anugrah 1', '\r'),
(7317051001105, 'Attaqwa Noling', '\r'),
(7317051001106, 'Hikmah Bupon', '\r'),
(7317051001109, 'Karya Muda', '\r'),
(7317051001116, 'Lumak', '\r'),
(7317051001117, 'Lumika Damai', '\r'),
(7317051001125, 'Mingkede', '\r'),
(7317051001129, 'Noling Mujur', '\r'),
(7317051001131, 'Pemuda Tani Berkarya', '\r'),
(7317051001132, 'Rahmat Prima', '\r'),
(7317051001133, 'Salumakarra', '\r'),
(7317051001135, 'Selalu Bersatu', '\r'),
(7317051001137, 'Setia Kawan', '\r'),
(7317051001138, 'Sinar Prima', '\r'),
(7317051001141, 'Sipakatau', '\r'),
(7317051001143, 'Sipatuo', '\r'),
(7317051001144, 'Sipatuo', '\r'),
(7317051001145, 'Sipatuo 1', '\r'),
(7317051001147, 'Siwata Group', '\r'),
(7317051001148, 'Syuhada', '\r'),
(7317051001149, 'Tani Bugis', '\r'),
(7317051001210, 'KWT Al-Munawwarah Salu Makarra', '\r'),
(7317051001211, 'KWT Flamboyan', '\r'),
(7317051001212, 'KWT Latulip', '\r'),
(7317051001213, 'KWT Melati', '\r'),
(7317051001214, 'KWT Permata Noling', '\r'),
(7317051001301, 'Abd. Aziz Abdullah', '\r'),
(7317051001303, 'Anugrah', '\r'),
(7317051001307, 'Hikmah Noling', '\r'),
(7317051001308, 'Jaya Bersama', '\r'),
(7317051001315, 'Lubis', '\r'),
(7317051001318, 'Mabbarakka', '\r'),
(7317051001319, 'Mabbulo Sipeppa', '\r'),
(7317051001320, 'Mabulo Sibatang', '\r'),
(7317051001321, 'Maloloe', '\r'),
(7317051001322, 'Mappatuo', '\r'),
(7317051001323, 'Masagena', '\r'),
(7317051001324, 'Mattoangin Lumika', '\r'),
(7317051001326, 'Mujur', '\r'),
(7317051001327, 'Noling Abadi', '\r'),
(7317051001328, 'Noling Buana', '\r'),
(7317051001330, 'Noling Rejeki Bersama', '\r'),
(7317051001334, 'Saro Mase', '\r'),
(7317051001336, 'Semangat Baru', '\r'),
(7317051001339, 'Sipakaboro', '\r'),
(7317051001340, 'Sipakalabbi Lumika', '\r'),
(7317051001342, 'Sipatokkong', '\r'),
(7317051001346, 'Sipurennu', '\r'),
(7317051001350, 'Tolajuk', '\r'),
(7317051001351, 'Tunas Prima', '\r'),
(7317051001352, 'Wanua Mappatuo', '\r'),
(7317052002101, '72 Pammase', '\r'),
(7317052002103, 'Cahaya Sukses', '\r'),
(7317052002104, 'Harapan Baru', '\r'),
(7317052002105, 'Karya Mandula', '\r'),
(7317052002107, 'Maju Bersama', '\r'),
(7317052002108, 'Maju Bersama', '\r'),
(7317052002113, 'Sinar Baru', '\r'),
(7317052002120, 'Tunas Baru', '\r'),
(7317052002206, 'Kwt Tanjong Melati', '\r'),
(7317052002302, 'Annur Kakao', '\r'),
(7317052002309, 'Mammase', '\r'),
(7317052002310, 'Nurul Rea', '\r'),
(7317052002311, 'Redo Jaya', '\r'),
(7317052002312, 'Redo Sejahtera', '\r'),
(7317052002314, 'Sinar Harapan', '\r'),
(7317052002315, 'Sinar Maju', '\r'),
(7317052002316, 'Tani Mulya', '\r'),
(7317052002317, 'Tani Subur', '\r'),
(7317052002318, 'Tani Tanjong', '\r'),
(7317052002319, 'Tanjung Harapan', '\r'),
(7317052003101, 'Batu Rondong', '\r'),
(7317052003102, 'Buntu Arre', '\r'),
(7317052003103, 'Buntu Arre II', '\r'),
(7317052003104, 'Buntu Batu', '\r'),
(7317052003108, 'Cahaya Sejati', '\r'),
(7317052003111, 'Ihlas', '\r'),
(7317052003114, 'Mandiri', '\r'),
(7317052003115, 'Mandiri', '\r'),
(7317052003116, 'Mappideceng', '\r'),
(7317052003117, 'Mappideceng', '\r'),
(7317052003119, 'Mekar I', '\r'),
(7317052003120, 'Nusa Tani', '\r'),
(7317052003123, 'Pumbau Jaya', '\r'),
(7317052003124, 'Pumbau Palattae', '\r'),
(7317052003127, 'Samaturu II', '\r'),
(7317052003128, 'Sangmata', '\r'),
(7317052003131, 'Sejahtera', '\r'),
(7317052003133, 'Sijunjung', '\r'),
(7317052003212, 'KWT Sawerigading', '\r'),
(7317052003305, 'Buntu Kamiri', '\r'),
(7317052003306, 'Buntu Kamiri I', '\r'),
(7317052003307, 'Buntu Matinulu', '\r'),
(7317052003309, 'Home Base', '\r'),
(7317052003310, 'Home Base', '\r'),
(7317052003313, 'Manannungang Manai', '\r'),
(7317052003318, 'Mekar', '\r'),
(7317052003321, 'Pc Almanar', '\r'),
(7317052003322, 'Pengkambuangan', '\r'),
(7317052003325, 'Rampungan Tekkeng', '\r'),
(7317052003326, 'Samaturu', '\r'),
(7317052003329, 'Sari Jaya', '\r'),
(7317052003330, 'Sawerigading Jaya', '\r'),
(7317052003332, 'Siangkaran', '\r'),
(7317052003334, 'Sobok', '\r'),
(7317052003335, 'Subur Jaya', '\r'),
(7317052004101, 'Bangkit Mandiri', '\r'),
(7317052004103, 'Bina Mandiri', '\r'),
(7317052004104, 'Bukit Sutra', '\r'),
(7317052004105, 'Harapan Jaya', '\r'),
(7317052004107, 'Karya Bersama', '\r'),
(7317052004108, 'Karya Mandiri', '\r'),
(7317052004111, 'Selalu Bersama', '\r'),
(7317052004114, 'Tani Beru', '\r'),
(7317052004302, 'Bersama', '\r'),
(7317052004306, 'Hikmah Bersatu', '\r'),
(7317052004309, 'Padaelo', '\r'),
(7317052004310, 'Sama Enre', '\r'),
(7317052004312, 'Sipatuo Dua', '\r'),
(7317052004313, 'Tampumia Jaya', '\r'),
(7317052005108, 'Mamminasae', '\r'),
(7317052005109, 'Mamminasae 1', '\r'),
(7317052005112, 'Pembaharuan', '\r'),
(7317052005113, 'Sipakainge', '\r'),
(7317052005203, 'KWT Bintang Tani', '\r'),
(7317052005204, 'KWT Kamboja', '\r'),
(7317052005205, 'KWT Mutiara', '\r'),
(7317052005206, 'KWT Permata', '\r'),
(7317052005301, 'Bahagia Bersama', '\r'),
(7317052005302, 'Bahagia Selalu', '\r'),
(7317052005307, 'Makmur Bersama', '\r'),
(7317052005310, 'Nurul Ummy', '\r'),
(7317052005311, 'Pammase', '\r'),
(7317052005314, 'Sipakilala', '\r'),
(7317052006101, 'Cahaya Prima', '\r'),
(7317052006102, 'Maccolli Loloe', '\r'),
(7317052006103, 'Malomoe', '\r'),
(7317052006104, 'Pammesaran', '\r'),
(7317052006106, 'Yasibarue', '\r'),
(7317052006305, 'Salu Pore', '\r'),
(7317052007101, 'Komunitas Pakkek', '\r'),
(7317052007102, 'Maroangin', '\r'),
(7317052007103, 'Masuka Sejahtera', '\r'),
(7317052007104, 'Mattirodeceng', '\r'),
(7317052007105, 'Pemerhati LH', '\r'),
(7317052007106, 'Puncak Malenggang', '\r'),
(7317052007108, 'Salu Salaka Pakkek', '\r'),
(7317052007109, 'Sipakainga', '\r'),
(7317052007110, 'Sipatuju', '\r'),
(7317052007111, 'Sipatuju', '\r'),
(7317052007112, 'Siporennu', '\r'),
(7317052007213, 'Wana Tani', '\r'),
(7317052007307, 'Putri Jaya Masuka', '\r'),
(7317052008206, 'KWT Tulip', '\r'),
(7317052008301, 'Amanah', '\r'),
(7317052008302, 'Amessangeng', '\r'),
(7317052008303, 'Balutan Abadi', '\r'),
(7317052008304, 'Bilante Jaya', '\r'),
(7317052008305, 'Jaya Bakti', '\r'),
(7317052008307, 'Montong Utama', '\r'),
(7317052008308, 'Payung Hijau', '\r'),
(7317052008309, 'Sipajunjung', '\r'),
(7317052008310, 'Sipakendek', '\r'),
(7317052009101, 'Bulu Marannu', '\r'),
(7317052009102, 'Kabut Rimba', '\r'),
(7317052009103, 'Mapato', '\r'),
(7317052009104, 'Pra Sejahtera', '\r'),
(7317052009105, 'Tunas Kakao', '\r'),
(7317052010101, 'Al-Hidayah', '\r'),
(7317052010102, 'Barokah Jaya', '\r'),
(7317052010103, 'Karya Usaha Mandiri', '\r'),
(7317052010104, 'Langda', '\r'),
(7317052010105, 'Pangi Indah', '\r'),
(7317052010107, 'Sikamali', '\r'),
(7317052010108, 'Subur Tani', '\r'),
(7317052010109, 'Suka Harapan', '\r'),
(7317052010110, 'Suka Harapan II', '\r'),
(7317052010306, 'Samonggo Jaya II', '\r');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `kelompok__tani`
--
ALTER TABLE `kelompok__tani`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
