-- MySQL dump 10.13  Distrib 5.5.54, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: microfin
-- ------------------------------------------------------
-- Server version	5.5.54-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `TMPREPORTESAL`
--

DROP TABLE IF EXISTS `TMPREPORTESAL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TMPREPORTESAL` (
  `SolicitudCreditoID` int(11) DEFAULT NULL COMMENT 'Solicitud de Credito. Sera una tabla de solicitudes\nPor el momento Es capturable, es un entero',
  `CreditoID` int(12) DEFAULT NULL,
  `ProductoCreditoID` int(12) DEFAULT NULL,
  `Descripcion` varchar(200) DEFAULT NULL,
  `ClienteID` int(12) DEFAULT NULL,
  `NombreCompleto` varchar(200) DEFAULT NULL,
  `SaldoCapVigent` decimal(16,2) DEFAULT NULL,
  `SaldoCapAtrasad` decimal(16,2) DEFAULT NULL,
  `SaldoCapVencido` decimal(16,2) DEFAULT NULL,
  `SaldCapVenNoExi` decimal(16,2) DEFAULT NULL,
  `SaldoInterProvi` decimal(16,2) DEFAULT NULL,
  `SaldoInterAtras` decimal(16,2) DEFAULT NULL,
  `SaldoInterVenc` decimal(16,2) DEFAULT NULL,
  `SaldoIntNoConta` decimal(16,2) DEFAULT NULL,
  `SaldoMoratorios` decimal(16,2) DEFAULT NULL,
  `SaldComFaltPago` decimal(16,2) DEFAULT NULL,
  `SaldoOtrasComis` decimal(16,2) DEFAULT NULL,
  `SaldoIVAInteres` decimal(16,2) DEFAULT NULL,
  `SaldoIVAMorator` decimal(16,2) DEFAULT NULL,
  `SalIVAComFalPag` decimal(16,2) DEFAULT NULL,
  `SaldoIVAComisi` decimal(16,2) DEFAULT NULL,
  `PasoCapAtraDia` decimal(16,2) DEFAULT NULL,
  `PasoCapVenDia` decimal(16,2) DEFAULT NULL,
  `PasoCapVNEDia` decimal(16,2) DEFAULT NULL,
  `PasoIntAtraDia` decimal(16,2) DEFAULT NULL,
  `PasoIntVenDia` decimal(16,2) DEFAULT NULL,
  `CapRegularizado` decimal(16,2) DEFAULT NULL,
  `IntOrdDevengado` decimal(16,2) DEFAULT NULL,
  `IntMorDevengado` decimal(16,2) DEFAULT NULL,
  `ComisiDevengado` decimal(16,2) DEFAULT NULL,
  `PagoCapVigDia` decimal(16,2) DEFAULT NULL,
  `PagoCapAtrDia` decimal(16,2) DEFAULT NULL,
  `PagoCapVenDia` decimal(16,2) DEFAULT NULL,
  `PagoCapVenNexDia` decimal(16,2) DEFAULT NULL,
  `PagoIntOrdDia` decimal(16,2) DEFAULT NULL,
  `PagoIntAtrDia` decimal(16,2) DEFAULT NULL,
  `PagoIntVenDia` decimal(16,2) DEFAULT NULL,
  `PagoIntCalNoCon` decimal(16,2) DEFAULT NULL,
  `PagoComisiDia` decimal(16,2) DEFAULT NULL,
  `PagoMoratorios` decimal(16,2) DEFAULT NULL,
  `PagoIvaDia` decimal(16,2) DEFAULT NULL,
  `IntCondonadoDia` decimal(16,2) DEFAULT NULL,
  `MorCondonadoDia` decimal(16,2) DEFAULT NULL,
  `IntDevCtaOrden` decimal(16,2) DEFAULT NULL,
  `CapCondonadoDia` decimal(16,2) DEFAULT NULL,
  `ComAdmonPagDia` decimal(16,2) DEFAULT NULL,
  `ComCondonadoDia` decimal(16,2) DEFAULT NULL,
  `DesembolsosDia` decimal(16,2) DEFAULT NULL,
  `FechaInicio` date DEFAULT NULL,
  `FechaVencimiento` date DEFAULT NULL,
  `FechaUltAbonoCre` date DEFAULT NULL,
  `MontoCredito` decimal(16,2) DEFAULT NULL,
  `DiasAtraso` int(12) DEFAULT NULL,
  `SaldoDispon` decimal(16,2) DEFAULT NULL,
  `SaldoBloq` decimal(16,2) DEFAULT NULL,
  `FechaUltDepCta` date DEFAULT NULL,
  `FrecuenciaCap` varchar(15) DEFAULT NULL,
  `FrecuenciaInt` varchar(15) DEFAULT NULL,
  `CapVigenteExi` decimal(16,2) DEFAULT NULL,
  `MontoTotalExi` decimal(16,2) DEFAULT NULL,
  `TasaFija` decimal(16,2) DEFAULT NULL,
  `PromotorID` int(12) DEFAULT NULL,
  `NombrePromotor` varchar(200) DEFAULT NULL,
  `FechaEmision` date DEFAULT NULL,
  `HoraEmision` time DEFAULT NULL,
  `MoraVencido` decimal(16,2) DEFAULT NULL,
  `MoraCarVen` decimal(16,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TMPREPORTESAL`
--

LOCK TABLES `TMPREPORTESAL` WRITE;
/*!40000 ALTER TABLE `TMPREPORTESAL` DISABLE KEYS */;
/*!40000 ALTER TABLE `TMPREPORTESAL` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-25  0:00:01
