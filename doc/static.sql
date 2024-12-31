DROP TABLE IF EXISTS `t_static`;
CREATE TABLE IF NOT EXISTS `t_static` (
  `id_sta` int NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `title_sta` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `url_sta` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_sta` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_sta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT into `t_static` (`id_sta`, `title_sta`, `url_sta`, `content_sta`)
VALUES (1, 'A propos', 'about', 'Contenu de la page about');
