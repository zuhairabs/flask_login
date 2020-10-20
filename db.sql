--
-- MySQL 5.5.5
-- Tue, 20 Oct 2020 06:48:29 +0000
--

CREATE TABLE `testapi` (
   `id` int(11) not null auto_increment,
   `name` varchar(100),
   `email` varchar(100),
   `username` varchar(100) not null,
   `password` varchar(100) not null,
   PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4