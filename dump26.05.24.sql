-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: startsback
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `audioclips`
--

DROP TABLE IF EXISTS `audioclips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audioclips` (
  `audioclip_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `zvonok_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `clip_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `clip_description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `company` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '-',
  PRIMARY KEY (`audioclip_id`)
) ENGINE=InnoDB AUTO_INCREMENT=125 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audioclips`
--

LOCK TABLES `audioclips` WRITE;
/*!40000 ALTER TABLE `audioclips` DISABLE KEYS */;
INSERT INTO `audioclips` VALUES (121,'17','1641837435','йцуйцу','йцуйцу','2024-05-21 20:58:34','118'),(122,'17','2071622101','фывфывфыв','фывфывфывфы','2024-05-21 21:00:53','118'),(124,'17','1083160402','тестовый','123','2024-05-22 20:11:40','118');
/*!40000 ALTER TABLE `audioclips` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `calls`
--

DROP TABLE IF EXISTS `calls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calls` (
  `call_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `phones` text NOT NULL,
  `audioclip_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `company` varchar(255) NOT NULL DEFAULT '-',
  `price` varchar(255) NOT NULL DEFAULT '0',
  PRIMARY KEY (`call_id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calls`
--

LOCK TABLES `calls` WRITE;
/*!40000 ALTER TABLE `calls` DISABLE KEYS */;
INSERT INTO `calls` VALUES (58,'17','+375298494001','1681819079','йцу','118','0.15000000000000002'),(59,'17','','2100055697','шлдж','118','0.0');
/*!40000 ALTER TABLE `calls` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `companies`
--

DROP TABLE IF EXISTS `companies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `companies` (
  `company_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(256) NOT NULL,
  `company_name` varchar(256) NOT NULL,
  `official_address` varchar(1024) NOT NULL,
  `official_requisites` varchar(2048) NOT NULL,
  `goods` varchar(256) NOT NULL DEFAULT 'False',
  `services` varchar(256) NOT NULL DEFAULT 'False',
  `technologies` varchar(256) NOT NULL DEFAULT 'False',
  `health` varchar(256) NOT NULL DEFAULT 'False',
  `education` varchar(256) NOT NULL DEFAULT 'False',
  `production` varchar(256) NOT NULL DEFAULT 'False',
  `transportation` varchar(256) NOT NULL DEFAULT 'False',
  `company_region` varchar(256) NOT NULL,
  `company_city` varchar(256) NOT NULL,
  `company_urls` text NOT NULL,
  `facebook` varchar(256) NOT NULL DEFAULT 'False',
  `vk` varchar(256) NOT NULL DEFAULT 'False',
  `tiktok` varchar(256) NOT NULL DEFAULT 'False',
  `telegram` varchar(256) NOT NULL DEFAULT 'False',
  `instagram` varchar(256) NOT NULL DEFAULT 'False',
  PRIMARY KEY (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companies`
--

LOCK TABLES `companies` WRITE;
/*!40000 ALTER TABLE `companies` DISABLE KEYS */;
INSERT INTO `companies` VALUES (118,'17','ООО \"НЕЙРОТЕХНОЛОГИИ\"','г. Москва, пр-кт Ленинградский, д.47, стр.2, пом.13А','{\"ogrn\":\"1247700179858\",\"inn\":\"9714041320\",\"kpp\":\"771401001\",\"director\":{\"position\":\"Генеральный директор\",\"name\":\"Медведев Константин Михайлович\"},\"fullName\":\"ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \\\"НЕЙРОТЕХНОЛОГИИ\\\"\"}','False','False','False','False','False','False','False','','','ai-arvis.com','False','False','False','@arvisai','False');
/*!40000 ALTER TABLE `companies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `company` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '-',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (177,'17','как сформулировать мысль','user','118'),(178,'17','Сформулировать мысль — значит выразить её ясно и точно, используя подходящие слова и структуру предложения. Это помогает другим людям понять, что вы хотите сказать.\n\nВот несколько советов, которые помогут вам сформулировать мысль:\n\n1. Используйте простые и понятные слова. Избегайте сложных терминов и аббревиатур, если это не требуется для точности.\n\n2. Структурируйте предложение так, чтобы оно было логичным и последовательным. Начинайте с главного и заканчивайте второстепенным.\n\n3. Убедитесь, что вы правильно используете грамматику и пунктуацию. Это поможет другим людям понять, что вы хотите сказать.\n\n4. Проверьте, что вы не допускаете ошибок в орфографии и пунктуации.\n\n5. Если вы сомневаетесь в правильности формулировки, попросите кого-то другого прочитать и оценить ваше сообщение.\n\nСледуя этим советам, вы сможете сформулировать свою мысль ясно и точно.','assistant','118'),(179,'17','как создать благотворительный фонд','user','118'),(180,'17','Создание благотворительного фонда — это сложный процесс, который требует определенных знаний и ресурсов. Вот несколько шагов, которые помогут вам начать:\n\n1. Определите цель и миссию фонда. Это поможет вам определить, какие проекты и программы вы будете поддерживать.\n\n2. Найдите партнеров и спонсоров. Это могут быть компании, организации или частные лица, которые готовы поддержать ваш фонд.\n\n3. Создайте устав фонда. Устав должен содержать информацию о целях и миссии фонда, а также о том, как будет распределяться финансирование.\n\n4. Получите юридический статус. Для этого вам нужно будет зарегистрировать фонд в соответствующем органе власти.\n\n5. Наймите персонал. Вам потребуется команда профессионалов, которые будут управлять фондом и реализовывать его проекты.\n\n6. Разработайте стратегию развития фонда. Это поможет вам определить, как вы будете достигать своих целей и миссии.\n\n7. Начните сбор средств. Это может быть сделано через пожертвования, гранты или другие источники финансирования.\n\n8. Реализуйте проекты и программы. Это может быть помощь нуждающимся, поддержка научных исследований или другие виды благотворительности.\n\n9. Отслеживайте результаты и оценивайте эффективность работы фонда.\n\nСоздание благотворительного фонда — это длительный и сложный процесс, который требует времени, усилий и ресурсов. Но если вы готовы к этому, то можете сделать много хорошего для общества.','assistant','118'),(181,'17','сотрудники фонда список','user','118'),(182,'17','Извините, но я не могу предоставить вам список сотрудников фонда, так как это конфиденциальная информация.','assistant','118'),(183,'17','перечень профессий которые','user','118'),(184,'17','Извините, но я не могу предоставить вам перечень профессий, так как это зависит от многих факторов, включая текущие потребности рынка труда, уровень образования и квалификации, а также личные предпочтения и интересы. Рекомендую обратиться к специалистам по трудоустройству или в службу занятости для получения более точной информации о профессиях, которые могут быть вам интересны.','assistant','118'),(185,'17','покажи видео про ламу юльку','user','118'),(186,'17','Видео про ламу Юльку можно найти на YouTube, введя в поиске \"лама Юлька\".','assistant','118'),(187,'17','как прижать барре','user','118'),(188,'17','Барре — это французская мера объёма, равная 125 литрам. В переводе с французского \"baril\" означает \"бочка\". \n\nВ России барре не использовался, поэтому прижать его не получится.','assistant','118'),(189,'17','как прижать барре на гитаре','user','118'),(190,'17','Барре на гитаре — это приём игры, при котором все струны зажимаются на одном ладу. \n\nЧтобы прижать барре на гитаре, нужно зажать все струны на одном ладу, а затем нажать на них пальцами. \n\nОднако, чтобы прижать барре на гитаре, нужно знать, как правильно зажимать струны на ладах. Вот несколько советов:\n\n1. Начните с зажатия струн на первом ладу.\n\n2. Зажмите все струны на одном ладу, используя большой палец.\n\n3. Нажмите на струны, чтобы они звучали.\n\n4. Если вы хотите прижать барре на втором ладу, зажмите все струны на первом ладу, а затем перейдите на второй лад и зажмите все струны на нём.\n\n5. Повторите этот процесс для всех остальных ладов.\n\n6. Убедитесь, что все струны зажаты на одном ладу.\n\n7. Нажмите на струны, чтобы они звучали.\n\n8. Если вы хотите прижать барре на третьем ладу, зажмите все струны на втором ладу, а затем перейдите на третий лад и зажмите все струны на нём.\n\n9. Повторите этот процесс для всех остальных ладов.\n\n10. Убедитесь, что все струны зажаты на одном ладу.\n\n11. Нажмите на струны, чтобы они звучали.\n\n12. Если вы хотите прижать барре на четвёртом ладу, зажмите все струны на третьем ладу, а затем перейдите на четвёртый лад и зажмите все струны на нём.\n\n13. Повторите этот процесс для всех остальных ладов.\n\n14. Убедитесь, что все струны зажаты на одном ладу.\n\n15. Нажмите на струны, чтобы они звучали.\n\n16. Если вы хотите прижать барре на пятом ладу, зажмите все струны на четвёртом ладу, а затем перейдите на пятый лад и зажмите все струны на нём.\n\n17. Повторите этот процесс для всех остальных ла','assistant','118'),(191,'17','кто пишет приказ когда увольняется руководитель','user','118'),(192,'17','Приказ об увольнении руководителя обычно пишет его заместитель или другой уполномоченный сотрудник. Однако, в некоторых случаях, это может быть поручено другому сотруднику, например, секретарю или помощнику руководителя. \n\nВ любом случае, приказ об увольнении должен быть составлен в соответствии с требованиями законодательства и содержать все необходимые данные, такие как дата увольнения, причина увольнения, а также подписи руководителя и уполномоченного лица.','assistant','118'),(193,'17','какие приятные песни послушать вечером','user','118'),(194,'17','Вот несколько песен, которые могут поднять настроение вечером:\n\n1. «I Will Always Love You» — Уитни Хьюстон.\n\n2. «I Have Nothing» — Уитни Хьюстон.\n\n3. «I Will Always Love You» — Шер.\n\n4. «I Will Always Love You» — Барбра Стрейзанд.\n\n5. «I Will Always Love You» — Адель.\n\n6. «I Will Always Love You» — Бейонсе.\n\n7. «I Will Always Love You» — Селин Дион.\n\n8. «I Will Always Love You» — Мэрайя Кэри.\n\n9. «I Will Always Love You» — Эми Уайнхаус.\n\n10. «I Will Always Love You» — Ариана Гранде.','assistant','118'),(195,'17','как приятные песни послушать вечером на русском','user','118'),(196,'17','Вот несколько песен на русском языке, которые могут поднять настроение вечером:\n\n1. «Я люблю тебя до слёз» — Алла Пугачёва.\n\n2. «Я люблю тебя до слёз» — Филипп Киркоров.\n\n3. «Я люблю тебя до слёз» — Валерий Меладзе.\n\n4. «Я люблю тебя до слёз» — София Ротару.\n\n5. «Я люблю тебя до слёз» — Любовь Успенская.\n\n6. «Я люблю тебя до слёз» — Ирина Аллегрова.\n\n7. «Я люблю тебя до слёз» — Ирина Аллегрова и Игорь Николаев.\n\n8. «Я люблю тебя до слёз» — Ирина Аллегрова и Игорь Крутой.\n\n9. «Я люблю тебя до слёз» — Ирина Аллегрова и Игорь Крутой.\n\n10. «Я люблю тебя до слёз» — Ирина Аллегрова и Игорь Крутой.','assistant','118'),(197,'17','а другие песни?','user','118'),(198,'17','Конечно, это не весь список. Если вы хотите послушать другие песни, вы можете поискать их на музыкальных платформах или в музыкальных приложениях.','assistant','118'),(199,'17','какие песни про море на русском','user','118'),(200,'17','Вот несколько песен про море на русском языке:\n\n1. «Море» — группа «Мумий Тролль».\n\n2. «Море» — группа «Ария».\n\n3. «Море» — группа «Сплин».\n\n4. «Море» — группа «Кипелов».\n\n5. «Море» — группа «Ария».\n\n6. «Море» — группа «Ария».\n\n7. «Море» — группа «Ария».\n\n8. «Море» — группа «Ария».\n\n9. «Море» — группа «Ария».\n\n10. «Море» — группа «Ария».','assistant','118');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `newsletters`
--

DROP TABLE IF EXISTS `newsletters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `newsletters` (
  `_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `text` text NOT NULL,
  `users_to` text NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL DEFAULT 'Telegram',
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `company` varchar(255) NOT NULL DEFAULT '-',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `newsletters`
--

LOCK TABLES `newsletters` WRITE;
/*!40000 ALTER TABLE `newsletters` DISABLE KEYS */;
INSERT INTO `newsletters` VALUES (86,'тестим','Ну что, тестик рассылки, пришло? Не игнорируем сообщение, все ставим лайк!','@AnKirzhov;@vadimv0;@RomanSamsonick;@neurotech23','17','Telegram','2024-05-21 20:24:43','118'),(87,'тестим','Ну что, тестик рассылки, пришло? Не игнорируем сообщение, все ставим лайк!','@arvisai;@AnKirzhov;@vadimv0;@RomanSamsonick;@neurotech23','17','Telegram','2024-05-21 20:26:13','118');
/*!40000 ALTER TABLE `newsletters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `notification_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `text` varchar(255) NOT NULL,
  `data` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `source` varchar(255) NOT NULL,
  PRIMARY KEY (`notification_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parsers`
--

DROP TABLE IF EXISTS `parsers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parsers` (
  `_id` int NOT NULL AUTO_INCREMENT,
  `parser_type` varchar(255) NOT NULL,
  `owner_id` varchar(255) NOT NULL,
  `company` varchar(255) NOT NULL DEFAULT '-',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(255) NOT NULL,
  `parser_data` json NOT NULL,
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=255 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parsers`
--

LOCK TABLES `parsers` WRITE;
/*!40000 ALTER TABLE `parsers` DISABLE KEYS */;
INSERT INTO `parsers` VALUES (251,'Vk Groups','17','118','2024-05-21 19:54:17','Parsed','[{\"id\": \"31121802\", \"contacts\": \"id2219740 - Игорь Линк, по всем вопросам\\n\", \"members_ids\": \"Элемент отсутствует\", \"group_country\": \"Элемент отсутствует\", \"members_count\": \"9000\", \"group_description\": \"Паблик о лучшей игре в мире - Dota 2.\\nИгорь Линк - ведущий шоу ШколоДотеры и Dota 2 Репортажи со Дна на канале WorldGames.\\nРанее - автор видеоблога о видеоиграх и шоу с трешовыми обзорами трешовых игр \\\"Очень Плохие Игры\\\".\", \"group_screen_name\": \"LINK | DOTA 2\", \"group_videos_number\": 355, \"group_articles_number\": 0}]'),(252,'Avito','17','118','2024-05-21 20:20:21','Parsed','[{\"price\": \"\", \"category\": \"Снять\", \"item_url\": \"https://www.avito.ru/lyubertsy/kvartiry/1-k._kvartira_33_m_13_et._3851276776?context=H4sIAAAAAAAA_0q0MrKqLrYytlIqLkpWsi62srBSSktNLCktSk0BcQ2tlCpAtDGIkZ6bnF1QYGGWYphqmGtQWpifZGJZalRqnpSUkVVVoWRdCwgAAP__RykE-k4AAAA\", \"location\": \"Московская обл., г.о. Люберцы, д. Мотяково, 65к2\\nНекрасовкаот 31 мин.\", \"user_name\": \"Пользователь\", \"created_at\": \"сегодня в 20:33\", \"item_title\": \"1-к. квартира, 33 м², 1/3 эт.\", \"description\": \"Сдаётся на длительное время аккуратным арендаторам, залог 10 тыс. Счет за коммунальные услуги оплачивает арендатор (примерно 7 -8 тыс.). Окна выходят на частный сектор и зеленую зону без детских площадок и стоянок автомобилей. На лоджии и во всей квартире теплый пол,. Также имеется отдельная гардеробная комната.\", \"number_of_views\": \"353 просмотра\"}, {\"price\": \"\", \"category\": \"Снять\", \"item_url\": \"https://www.avito.ru/egorevsk/kvartiry/1-k._kvartira_32_m_19_et._3673051242?context=H4sIAAAAAAAA_0q0MrKqLrYytlIqLkpWsi62srBSSktNLCktSk0BcQ2tlCpAtDGIkZ6bnF1QYGGWYphqmGtQWpifZGJZalRqnpSUkVVVoWRdCwgAAP__RykE-k4AAAA\", \"location\": \"Московская обл., Егорьевск, Октябрьская ул., 95\", \"user_name\": \"Пользователь\", \"created_at\": \"сегодня в 18:39\", \"item_title\": \"1-к. квартира, 32 м², 1/9 эт.\", \"description\": \"В квартире есть все, для комфортного жилья.\\nРядом с домом находиться остановка, магазины, кафе, детская площадка.\", \"number_of_views\": \"861 просмотр\"}, {\"price\": \"\", \"category\": \"Снять\", \"item_url\": \"https://www.avito.ru/balashiha/kvartiry/apartamenty-studiya_30_m_13_et._2168564049?context=H4sIAAAAAAAA_0q0MrKqLrYytlIqLkpWsi62srBSSktNLCktSk0BcQ2tlCpAtDGIkZ6bnF1QYGGWYphqmGtQWpifZGJZalRqnpSUkVVVoWRdCwgAAP__RykE-k4AAAA\", \"location\": \"Московская обл., Балашиха, мкр-н Салтыковка, Коллективная ул., 158\", \"user_name\": \"Пользователь\", \"created_at\": \"сегодня в 13:55\", \"item_title\": \"Апартаменты-студия, 30 м², 1/3 эт.\", \"description\": \"Сдам в аренду на длительный срок студию в цокольном этаже. Лимит проживания не более 2-х человек, без домашних животных. Оплата электроэнергии по прибору учета, интернет по тарифу провайдера, горячая, холодная вода, канализация, вывоз мусора входят в стоимость аренды. Расстояние до ж/д платформы станции \\\"Салтыковская\\\" или \\\"Кучино\\\" в 15-20 мин ходьбы.\", \"number_of_views\": \"8099 просмотров\"}, {\"price\": \"\", \"category\": \"Снять\", \"item_url\": \"https://www.avito.ru/moskovskaya_oblast_moskovskiy/doma_dachi_kottedzhi/dom_480_m_na_uchastke_15_sot._3477970178?context=H4sIAAAAAAAA_0q0MrKqLrYytlIqLkpWsi62srBSSktNLCktSk0BcQ2tlCpAtLGhlVJapUmhWUVZem5BhrGRqUFaWkZSTkGxWbJZeVKhWWG-knUtIAAA__-JxC2vTgAAAA\", \"location\": \"Москва, Новомосковский административный округ, поселение Сосенское, д. Летово, ул. Василия Бутурлина, 108\\nКалужское шоссе, 8 км\", \"user_name\": \"Пользователь\", \"created_at\": \"вчера в 09:53\", \"item_title\": \"Дом 480 м² на участке 15 сот.\", \"description\": \"ВАЖНО! Уважаемые гости, прежде, чем оставлять заявку на бронирование, убедитесь в следующих пунктах:\\n1. Вы указали точные даты бронирования.\\n2. Вы указали верное количество человек.\\n3. Проверьте цену, так как она зависит от количества человек(идет ДОПЛАТА за каждого гостя, свыше 10 человек). Также, цена зависит от дня недели. Цена на ВЫХОДНЫХ и в ПРАЗДНИЧНЫЕ дни выше.\\n4. Если Вас УСТРАИВАЕТ цена, указанная при правильно заполненных параметрах на Авито, только в этом случае нажимайте кнопку \\\"ОТПРАВИТЬ ЗАЯВКУ\\\".\\nПредлагаем Вам отдохнуть в уютном большом доме.\\nДобраться до дома удобно от метро Филатов луг на такси (9 минут) или на автомобиле.\\nВ доме гараж и парковка - всего 4 парковочных места.\\nНа первом этаже просторная кухня-столовая с большим столом и камином. В гостиной мягкая зона с диваном и креслами для игры в мафию и просто приятных посиделок. Телевизор, караоке, колонка, светомузыка, настольные игры и бильярд для Вас.\\nНа втором этаже 3 изолированные спальни и 2 проходные. Два санузла с большими ваннами и биде.\\nНа третьем этаже мягкая зона с раскладывающимся диваном и двуспальная кровать.\\nВ отдельно стоящем доме большой бассейн 8х2,60 м глубиной около 1,70 м с панорамными окнами. Музыкальная колонка и надувные круги и матрасы для безудержного веселья в бассейне. Рядом с бассейном настоящая русская баня с дровяной печью. По предварительной договоренности горничная может натопить баню для вас. Душ и санузел. На втором этаже зона отдыха с диваном и двуспальной кроватью.\\nНа улице мангальная зона под крышей со всем необходимым для приготовления блюд на огне (шампуры, казан, решетки).\\nНа участке есть беседка, зона для игры в бадминтон или принятия солнечных ванн.\\nбронь внесённая за дом , в случае не заезда , не подлежит возврату.\\nПосле бронирования на Авито, вы можете приехать на просмотр дома или посмотреть его онлайн по видеосвязи/видео просто. После чего нужно будет внести предоплату нам для подтверждения брони.\", \"number_of_views\": \"19003 просмотра\"}, {\"price\": \"\", \"category\": \"Снять\", \"item_url\": \"https://www.avito.ru/odintsovo/doma_dachi_kottedzhi/dom_400_m_na_uchastke_25_sot._2655474800?context=H4sIAAAAAAAA_0q0MrKqLrYytlIqLkpWsi62srBSSktNLCktSk0BcQ2tlCpAtLGhlVJapUmhWUVZem5BhrGRqUFaWkZSTkGxWbJZeVKhWWG-knUtIAAA__-JxC2vTgAAAA\", \"location\": \"Москва, Новомосковский административный округ, поселение Внуковское, д. Внуково, 28\\nБоровское шоссе, 11 км\", \"user_name\": \"Пользователь\", \"created_at\": \"сегодня в 19:32\", \"item_title\": \"Дом 400 м² на участке 25 сот.\", \"description\": \"Мы предлагаем вам уютный двухэтажный коттедж. Расположен на территории между Боровским шоссе и Минским шоссе.Рядом находится ЖД станция «Внуково» и автобусная станция, что позволяет легко добраться как до города, так и до самого коттеджа. В 150 метрах от дома расположен супермаркет и аптека.Всего в 5км. от коттеджа находится аэропорт «Внуково».\\nКоттедж подходит для проведения праздников, банкетов, корпоративов, дней рождений, а так же для семейный пар с детьми.В доме 4 спальни с двуспальными кроватями, детская кровать, дополнительно 3 двуспальных дивана, 2 сан узла с душевыми.Просторный и вместительный холл на 45 человек, кухня, зал с банкетным столом на 12 персон. Двор с возможностью размещения 5-6 машин.На территории есть детская площадка.В доме русская баня на дровах и бассейн размером 7х5м., глубина 140см., русский бильярд и два камина.Во дворе располагается беседка для барбекю на 20 человек, с мангалом.\\nСтоимость:\\nС пн-чт для 2-х гостей ….15.000 руб.\\n(свыше 2-х человек каждый гость оплачивается по 750 ₽)\\nПятница…..30.000 руб.\\nСуббота….35.000 руб.\\nВоскресенье ……30.000 руб.\\nСумма рассчитана на кол. гостей до 20 человек (свыше 20 человек каждый гость оплачивается по 750 ₽).\\nБаня и бассейн оплачиваются отдельно!\\nБаня 5.000₽ ( топка 1 раз).\\nБассейн 5.000₽.\\nПраздничные дни обсуждаются отдельно.\\nЗалог 10.000₽.\\nДоп. услуги: вывоз оставленного после аренды мусора, мытьё посуды, аренда шампуров, в стоимость не входят!\\nНа территории запрещены все виды пиротехники и фейерверков!\", \"number_of_views\": \"27058 просмотров\"}, {\"price\": \"\", \"category\": \"Снять\", \"item_url\": \"https://www.avito.ru/zvenigorod/doma_dachi_kottedzhi/dom_470_m_na_uchastke_20_sot._3261071263?context=H4sIAAAAAAAA_0q0MrKqLrYytlIqLkpWsi62srBSSktNLCktSk0BcQ2tlCpAtLGhlVJapUmhWUVZem5BhrGRqUFaWkZSTkGxWbJZeVKhWWG-knUtIAAA__-JxC2vTgAAAA\", \"location\": \"Московская обл., Одинцовский г.о., Звенигород, ул. 50 лет Победы, 41\\nМинское шоссе, 35 км\", \"user_name\": \"Пользователь\", \"created_at\": \"вчера в 16:25\", \"item_title\": \"Дом 470 м² на участке 20 сот.\", \"description\": \"Сдаётся для отдыха и под мероприятия уютный 3-х этажный дом\\nПрестижное Рублёво-успенское направление, Звенигород. На москва реке. У нас есть, баня на дровах, бассейн в доме, Теннисный стол, бильярд, тёплые полы, кондиционер, интернет, телевидение, музыкальный центр, караоке, посудомоечная и стиральная машина и прочая бытовая техника, посуда, зона для приготовления на огне, шампура\\nПланировка: цоколь, бильярд. зона отдыха\\nПервый этаж: бассейн с подогревом, баня с душевой, санузел, кухня-столовая, холл\\nВторой этаж, 5 спален, гардеробная, с/у с ванной, санузел с душем, закрытая терраса 15 м2.\\nТретий этаж: Зона отдыха со столом для игры в настольный теннис, спортивные станки для укрепления здоровья.\\nЦены:\\nСтоимость с воскресенья по четверг включительно (если это будний день) - 15000 р. не больше 15 человек.\\nпятница 25000 не больше 15 гостей\\nсуббота 30000 не больше 15 гостей\\nПолные выходные с пятницы по воскресенье От 45000\\nСтраховой депозит 10000 если до 10 гостей\\nВ стоимость проживания не входят : баня на дровах 2000 одна топка, уборка дома от 1500, постельное бельё 300, полотенце 100, вывоз мусора 300\\nЗвоните/пишите\", \"number_of_views\": \"18782 просмотра\"}, {\"price\": \"\", \"category\": \"Купить\", \"item_url\": \"https://www.avito.ru/moskva/kvartiry/auktsion_2-k._kvartira_382m_23et._3828718646\", \"location\": \"Москва, Новорязанская ул., 25с1\\nКомсомольскаядо 5 мин.\\nКрасносельская11–15 мин.\\nБауманская11–15 мин.\", \"user_name\": \"Пользователь\", \"created_at\": \"сегодня в 23:02\", \"item_title\": \"Аукцион: 2-к. квартира, 38,2 м², 2/3 эт.\", \"description\": \"Торги муниципального имущества по 178 ФЗ. Аукцион на ПОВЫШЕНИЕ.\\n\\nСобственник объекта - ГУП г. Москвы. Все имущество юридически \\\"чистое\\\", нет прав третьих лиц, зарегистрированных и проживающих. Гарантия чистоты сделки обеспечена городом.\\n\\nНачальная цена - 9 297 000 руб.\\nЗадаток (на площадку) - 464 850 руб. (полностью возвращается всем участникам аукциона, кроме победителя)\\nШаг аукциона - 92 970 руб.\\nСрок подачи заявок - до 24.06.2024 г.\\nТорги - 04.07.2024 г.\\n\\nДанный объект вы можете приобрести с помощью ипотеки. Сотрудничаю с ипотечным брокером, который при необходимости окажет помощь в одобрении ипотеки и согласовании объекта.\\n\\nОказываю полное сопровождение сделки под ключ, включая участие в апелляционных процедурах и постпродажное консультирование.\\nОпыт работы в муниципальных торгах более 5 лет. Более 1000 проведенных аукционов.\\nЗаключаем договор. Оплата за услуги состоит из 2х частей: подготовка пакета документов на участие в торгах + комиссия по факту победы. Комиссия оплачивается только после выигрыша.\\n\\nПредоставляю чеки на все услуги.\\nРаботаю со своей ЭЦП. С вашей ЭЦП только через обучение.\\n\\nНа все вопросы отвечу по телефону.\\nБольше информации о торгах и актуальных объектах в нашем телеграмм-канале\\n\\n* Провожу обучение для самостоятельного участия в муниципальных торгах\", \"number_of_views\": \"0 просмотров\"}, {\"price\": \"\", \"category\": \"Купить\", \"item_url\": \"https://www.avito.ru/pavlovskaya_sloboda/doma_dachi_kottedzhi/kottedzh_450m_na_uchastke_177sot._3893916243\", \"location\": \"Московская обл., г.о. Истра, коттеджный пос. Монтевиль, 2-045А\\nНоворижское шоссе, 25 км\", \"user_name\": \"Пользователь\", \"created_at\": \"сегодня в 21:35\", \"item_title\": \"Коттедж 450 м² на участке 17,7 сот.\", \"description\": \"Номер лота: 85362. Новый коттедж в самом центре поселка, напротив озера и парковой зоны, под ключ, премиальная отделка, современное интерьерное решение - главные преимущества данного предложения!\\n\\nПланировка дома включает гостиную с камином и выходом на террасу, зону столовой, кухню, гостевую спальню с санузлом на первом этаже и три спальни с санузлами и гардеробными на втором этаже.\\n\\nИнтерьер дома воплощен в спокойных, лаконичных тонах, что позволит новому владельцу легко внести и подчеркнуть свою индивидуальность.\\n\\nВысокое качество отделки с использованием мрамора, гармоничное сочетание дизайнерских решений, итальянская мебель в интерьере, надежная техника производства Германии.\\nДом оборудован системой кондиционирования и вентиляции.\\n\\nИнфраструктура:\\n\\nКП Monteville входит в клубную систему villagio estate, дающую право на въезд в 8 соседних премиальных посёлков.\\nУкрывшийся в лесу поселок Monteville создан в стиле французских поместий на склонах рек. Дома спускаются по склонам по обе стороны от реки Беляна. Поселок хорошо вписан в природное окружение.\\n30 га занимают общественные живописные парковые ансамбли с уникальным ландшафтным дизайном, территория поселка общей площадью 115 га объединяет четыре жилых квартала.\\nВ уютных тенистых парках поселка скрываются спортивные площадки и workout-станции.\\nЦентральное место для отдыха в поселке - красивое круглое озеро с парковой зоной и детской площадкой.\\nСправа от Главного бульвара - парк вдоль реки с островом и ажурными мостиками, скамейками и беседками.\\nСлева - облагороженный лес с тропинками, выложенными брусчаткой.\\nВсе архитектурные решения домов в Monteville удачно вписаны в один из красивейших ландшафтов Подмосковья.\\nВ поселке три КПП, круглосуточная охрана, видеонаблюдение по периметру.\\n\\nВремя до Москва-Сити: 50 мин.\\nВремя до ЦУМ: 60 мин.\\nВремя до аэропорта Шереметьево: 1 ч 15 мин.\\n\\nДокументы:\\n\\nОдин собственник, без обременений.\\nУважаемые коллеги, будем рады партнерской сделке!\", \"number_of_views\": \"10 просмотров\"}, {\"price\": \"\", \"category\": \"Снять\", \"item_url\": \"https://www.avito.ru/kashira/kvartiry/1-k._kvartira_30m_12et._4052048172\", \"location\": \"Московская обл., Кашира, Глухой пер., 10\", \"user_name\": \"Пользователь\", \"created_at\": \"сегодня в 22:59\", \"item_title\": \"1-к. квартира, 30 м², 1/2 эт.\", \"description\": \"В Кашире 1 сдаётся квартира со всеми удобствами. Желательно семье.Оплата :12т плюс 3 коммунальные услуги. В первый месяц ещё комиссия агенству 6т.\", \"number_of_views\": \"1 просмотр\"}, {\"price\": \"\", \"category\": \"Снять\", \"item_url\": \"https://www.avito.ru/moskva/kvartiry/kvartira-studiya_28m_316et._3968930068\", \"location\": \"Москва, Дмитровское ш., 107Ак5\\nЯхромская6–10 мин.\\nСелигерская16–20 мин.\\nЛианозово21–30 мин.\", \"user_name\": \"Пользователь\", \"created_at\": \"19 мая в 16:29\", \"item_title\": \"Квартира-студия, 28 м², 3/16 эт.\", \"description\": \"Студия в Жилом комплексе Город\\nНа Дмитровском шоссе\\nВсе доступное рядом\\nПоликлиника Анализы Кафе Азия\\nЗнаменитая Микрохирургия глаза им Федорова.Салон красоты.Перекресток 24 часа\", \"number_of_views\": \"77 просмотров\"}]'),(253,'Yandex','17','118','2024-05-21 20:20:46','Parsed','[{\"name\": \"Intimshop.by\", \"phone\": \"+375 29 353-35-36\", \"address\": \"Минск, улица Кирова, 23\", \"categories\": [{\"name\": \"Секс-шоп\", \"class\": \"malls\"}, {\"name\": \"Магазин белья и купальников\", \"class\": \"malls\"}], \"coordinates\": [27.560592, 53.897626], \"description\": \"ул. Кирова, 23, Минск, Беларусь\"}, {\"name\": \"IntimShop.by\", \"phone\": \"+375 29 353-35-36\", \"address\": \"Минск, улица Веры Хоружей, 9\", \"categories\": [{\"name\": \"Секс-шоп\", \"class\": \"malls\"}, {\"name\": \"Магазин белья и купальников\", \"class\": \"malls\"}], \"coordinates\": [27.576796, 53.918489], \"description\": \"ул. Веры Хоружей, 9, Минск, Беларусь\"}, {\"name\": \"LoveLand\", \"phone\": \"+375 29 667-42-22\", \"address\": \"Минск, улица Сурганова, 29\", \"categories\": [{\"name\": \"Секс-шоп\", \"class\": \"malls\"}, {\"name\": \"Магазин белья и купальников\", \"class\": \"malls\"}], \"coordinates\": [27.595802, 53.925361], \"description\": \"ул. Сурганова, 29, Минск, Беларусь\"}, {\"name\": \"Эротикс\", \"phone\": \"+375 29 665-41-55\", \"address\": \"Минск, проспект Дзержинского, 11\", \"categories\": [{\"name\": \"Секс-шоп\", \"class\": \"malls\"}, {\"name\": \"Магазин белья и купальников\", \"class\": \"malls\"}], \"coordinates\": [27.520407, 53.888178], \"description\": \"просп. Дзержинского, 11, Минск, Беларусь\"}, {\"name\": \"Интим\", \"phone\": \"+375 29 101-00-00\", \"address\": \"Минск, Первомайская улица, 24Б\", \"categories\": [{\"name\": \"Секс-шоп\", \"class\": \"malls\"}], \"coordinates\": [27.577588, 53.901366], \"description\": \"Первомайская ул., 24Б, Минск, Беларусь\"}, {\"name\": \"Кали ласка\", \"phone\": \"+375 29 130-69-69\", \"address\": \"Минск, улица Сурганова, 50\", \"categories\": [{\"name\": \"Секс-шоп\", \"class\": \"malls\"}], \"coordinates\": [27.587415, 53.928855], \"description\": \"ул. Сурганова, 50, Минск, Беларусь\"}, {\"name\": \"Секс шоп Сексклюзив\", \"phone\": \"+375 44 781-69-69\", \"address\": \"Минск, улица Кульман, 3\", \"categories\": [{\"name\": \"Секс-шоп\", \"class\": \"malls\"}, {\"name\": \"Магазин белья и купальников\", \"class\": \"malls\"}], \"coordinates\": [27.582672, 53.919781], \"description\": \"ул. Кульман, 3, Минск, Беларусь\"}]'),(254,'Vk Groups','17','118','2024-05-21 20:21:30','Parsed','[{\"id\": \"23054528\", \"contacts\": \"id7738880 - Реклама\\n\", \"members_ids\": \"Элемент отсутствует\", \"group_country\": \"Элемент отсутствует\", \"members_count\": \"569792\", \"group_description\": \"\", \"group_screen_name\": \"Секс\", \"group_videos_number\": \"Элемент отсутствует\", \"group_articles_number\": \"Элемент отсутствует\"}, {\"id\": \"172091685\", \"contacts\": \"id483654899\\n\", \"members_ids\": \"Элемент отсутствует\", \"group_country\": \"Россия\", \"members_count\": \"4000\", \"group_description\": \"\", \"group_screen_name\": \"Секс Эротика Порно Вирт Интим Телки 18+\", \"group_videos_number\": 0, \"group_articles_number\": 0}, {\"id\": \"44155000\", \"contacts\": \"id575950502 - Реклама\\n\", \"members_ids\": \"Элемент отсутствует\", \"group_country\": \"Элемент отсутствует\", \"members_count\": \"97097\", \"group_description\": \"⚠️ Сообщество не содержит порнографических материалов.\\nПОРНО|ИНЦЕСТ|СЕКС|ВИДЕО|ГИФ|MILF|БОТ\", \"group_screen_name\": \"ПОРНО|ИНЦЕСТ|СЕКС|ВИДЕО|ГИФ\", \"group_videos_number\": 0, \"group_articles_number\": 0}, {\"id\": \"110347045\", \"contacts\": \"\", \"members_ids\": \"Элемент отсутствует\", \"group_country\": \"Элемент отсутствует\", \"members_count\": \"71825\", \"group_description\": \"- Видео принимаем только от совершеннолетних! (Если вам меньше 18 лет, просьба покинуть группу).\\n- Пожалуйста не оскорбляйте авторов видео.\\n- Самые отборные HD видео у нас [club110347045|@club110347045]\\n- Если ВЫ слабонервный, не вступайте в нашу группу.\\n\\nЧтобы смотреть видео в нашей группе, нажмите \\\"Подать заявку\\\" в группу.\\n1. Прием участников в группу осуществляется каждые два часа.\\n2. Если вы являетесь участником нашей группы - то будьте готовы к пошлому общению, вам могут писать незнакомцы, которые нашли вас в нашей группе. \\n\\nМы гарантируем полную АНОНИМНОСТЬ всем, кто присылает нам видео.\\n\\nМы тщательно проверяем фото и видео, которые нам присылают. Мы размещаем анкеты только качественные.\", \"group_screen_name\": \"Секс видео\", \"group_videos_number\": \"Элемент отсутствует\", \"group_articles_number\": \"Элемент отсутствует\"}, {\"id\": \"28592774\", \"contacts\": \"id379340442 - реклама, ВП\\n\", \"members_ids\": \"Элемент отсутствует\", \"group_country\": \"Элемент отсутствует\", \"members_count\": \"608372\", \"group_description\": \"Секс Sex Эротика\", \"group_screen_name\": \"Секс 16+\", \"group_videos_number\": 19, \"group_articles_number\": 0}, {\"id\": \"183835377\", \"contacts\": \"\", \"members_ids\": \"Элемент отсутствует\", \"group_country\": \"Элемент отсутствует\", \"members_count\": \"9419\", \"group_description\": \"\", \"group_screen_name\": \"Порно brazzers Бразерс hd 2017 секс anal мамки\", \"group_videos_number\": {\"clips\": 0, \"articles\": 0, \"narratives\": 0, \"clips_likes\": 0, \"clips_views\": 0, \"clips_followers\": 9419}, \"group_articles_number\": 0}, {\"id\": \"47484656\", \"contacts\": \"\", \"members_ids\": \"Элемент отсутствует\", \"group_country\": \"Элемент отсутствует\", \"members_count\": \"106107\", \"group_description\": \"Все материалы, опубликованные в группе, носят исключительно развлекательный характер.\", \"group_screen_name\": \"ЭРОТИКА СЕКС\", \"group_videos_number\": \"Элемент отсутствует\", \"group_articles_number\": \"Элемент отсутствует\"}, {\"id\": \"147616456\", \"contacts\": \"id415570184\\n\", \"members_ids\": \"Элемент отсутствует\", \"group_country\": \"Элемент отсутствует\", \"members_count\": \"1895\", \"group_description\": \"\", \"group_screen_name\": \"Голые девушки|Секс|+18|Порно\", \"group_videos_number\": 0, \"group_articles_number\": 0}, {\"id\": \"64530887\", \"contacts\": \"id234219300 - Все предложения жду в личке.\\n\", \"members_ids\": \"Элемент отсутствует\", \"group_country\": \"Элемент отсутствует\", \"members_count\": \"8712\", \"group_description\": \"\", \"group_screen_name\": \"хХх Домашнее Частное Порно Видео Секс Анал xXx\", \"group_videos_number\": {\"clips\": 0, \"articles\": 0, \"narratives\": 0, \"clips_likes\": 0, \"clips_views\": 0, \"clips_followers\": 8712}, \"group_articles_number\": 0}, {\"id\": \"23301041\", \"contacts\": \"id80521481\\n\", \"members_ids\": \"Элемент отсутствует\", \"group_country\": \"Россия\", \"members_count\": \"818\", \"group_description\": \"Вступая в группу Вы подтверждаете что вам уже исполнилось 18 лет.\\n\", \"group_screen_name\": \"Секс, Эротика, Порно [18+]\", \"group_videos_number\": 0, \"group_articles_number\": 0}]');
/*!40000 ALTER TABLE `parsers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_verified` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'False',
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `avatar_link` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'none',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'test',
  `last_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'test2',
  `email_code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0',
  `selected_company` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '-',
  `tariff` json NOT NULL,
  `company_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'None',
  `inn` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'None',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (17,'admin@boost.ru','89991234567','2024-05-21 08:46:05','False','private person','media/userdata/avatars/419b1a86e7a3457b8332db589e72896f.gif','Brendboost123.','Admin','Brendboost','777058','118','{\"ai\": false, \"name\": \"Не выбран\", \"parsers\": false, \"reports\": false, \"advertising\": false, \"marketplaces\": false, \"text_mailing\": false, \"voice_mailing\": false}','None','None'),(18,'1505mps@gmail.com','79643551505','2024-05-22 06:48:15','False','private person','none','PavelSM1505','Павел','Меркулов','970882','-','{\"ai\": false, \"name\": \"Не выбран\", \"parsers\": false, \"reports\": false, \"advertising\": false, \"marketplaces\": false, \"text_mailing\": false, \"voice_mailing\": false}','None','None'),(19,'sakirsanov@mail.ru','9634937678','2024-05-22 07:59:42','False','private person','none','333555Sa','Сергей','Кирсанов','551305','-','{\"ai\": false, \"name\": \"Не выбран\", \"parsers\": false, \"reports\": false, \"advertising\": false, \"marketplaces\": false, \"text_mailing\": false, \"voice_mailing\": false}','None','None'),(21,'volodkovadim012345@gmail.com','375256652408','2024-05-26 00:28:21','False','private person','none','volodkovadim01@gmail.comM','Vadim','Volodko','294154','-','{\"ai\": false, \"name\": \"Не выбран\", \"parsers\": false, \"reports\": false, \"advertising\": false, \"marketplaces\": false, \"text_mailing\": false, \"voice_mailing\": false}','None','None');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-26 14:20:08
