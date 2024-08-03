/*!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.2.4-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: iching
-- ------------------------------------------------------
-- Server version	11.2.4-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `xref_trigrams`
--

DROP TABLE IF EXISTS `xref_trigrams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xref_trigrams` (
  `bseq` int(11) NOT NULL,
  `pseq` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `trans` varchar(255) DEFAULT NULL,
  `t_element` varchar(32) DEFAULT NULL,
  `polarity` varchar(32) DEFAULT NULL,
  `planet` varchar(32) DEFAULT NULL,
  `archetype` varchar(32) DEFAULT NULL,
  `explanation` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`bseq`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xref_trigrams`
--

LOCK TABLES `xref_trigrams` WRITE;
/*!40000 ALTER TABLE `xref_trigrams` DISABLE KEYS */;
INSERT INTO `xref_trigrams` VALUES
(0,7,'K\'UN','The Receptive','Earth','Primal Feminine','Moon','Earth',''),
(1,4,'CHeN','The Arousing','Thunder','Masculine Expanding','Mars',NULL,'M'),
(2,2,'K\'AN','The Abysmal','Water','Feminine Demanding','Saturn',NULL,'F'),
(3,8,'TUI','The Joyous','Lake','Masculine Harmonious','Venus',NULL,'M'),
(4,3,'KeN','Keeping Still','Mountain','Feminine Creative','Earth',NULL,'F'),
(5,6,'LI','The Clinging','Fire','Masculine Benevolent','Jupiter',NULL,'M'),
(6,5,'SUN','The Gentle','Wind & Wood','Feminine Understanding','Mercury',NULL,'F'),
(7,1,'CH\'IEN','The Creative','Heaven','Primal Masculine','Sun','Sun and Moon','F');
/*!40000 ALTER TABLE `xref_trigrams` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-03 17:57:47
