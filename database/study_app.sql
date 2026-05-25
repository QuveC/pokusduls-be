-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 15 Apr 2026 pada 16.41
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `study_app`
--

DELIMITER $$
--
-- Prosedur
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `addMessage` (IN `p_chat_history_id` INT, IN `p_role` VARCHAR(20), IN `p_content` TEXT)   BEGIN
    INSERT INTO chat_message (chat_history_id, role, content)
    VALUES (p_chat_history_id, p_role, p_content);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `analyzeFrame` (IN `p_monitoring_id` INT, IN `p_ear` FLOAT, IN `p_blink_count` INT, IN `p_head_pose` VARCHAR(50), IN `p_confidence` FLOAT)   BEGIN
    INSERT INTO face_data_model (monitoring_id, eye_aspect_ratio, blink_count, head_pose, confidence)
    VALUES (p_monitoring_id, p_ear, p_blink_count, p_head_pose, p_confidence);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `clearChatHistory` (IN `p_chat_history_id` INT)   BEGIN
    DELETE FROM chat_message WHERE chat_history_id = p_chat_history_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `fetchChatHistory` (IN `p_user_id` INT)   BEGIN
    SELECT ch.chat_history_id, ch.session_id, ch.timestamp,
           cm.message_id, cm.role, cm.content, cm.timestamp AS msg_time
    FROM chat_history ch
    LEFT JOIN chat_message cm ON ch.chat_history_id = cm.chat_history_id
    WHERE ch.user_id = p_user_id
    ORDER BY ch.timestamp DESC, cm.timestamp ASC;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `fetchContext` (IN `p_user_id` INT, IN `p_session_id` INT)   BEGIN
    SELECT 
        sd.method_type,
        sd.duration,
        us.avg_focus_score,
        us.total_xp,
        ms.drowsy_events
    FROM session_data sd
    LEFT JOIN user_statistics us ON sd.user_id = us.user_id
    LEFT JOIN monitoring_session ms ON sd.session_id = ms.session_id
    WHERE sd.user_id = p_user_id AND sd.session_id = p_session_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `fetchUserStats` (IN `p_user_id` INT)   BEGIN
    SELECT * FROM user_statistics WHERE user_id = p_user_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `getHistory` (IN `p_chat_history_id` INT)   BEGIN
    SELECT message_id, role, content, timestamp 
    FROM chat_message 
    WHERE chat_history_id = p_chat_history_id 
    ORDER BY timestamp ASC;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `getMonitoringSummary` (IN `p_monitoring_id` INT)   BEGIN
    SELECT 
        ms.monitoring_id,
        ms.start_time,
        ms.end_time,
        TIMESTAMPDIFF(MINUTE, ms.start_time, IFNULL(ms.end_time, NOW())) AS duration_minutes,
        ms.drowsy_events,
        ms.total_alerts,
        COUNT(fdm.face_data_id) AS total_face_readings,
        AVG(fdm.eye_aspect_ratio) AS avg_ear,
        SUM(fdm.blink_count) AS total_blinks
    FROM monitoring_session ms
    LEFT JOIN face_data_model fdm ON ms.monitoring_id = fdm.monitoring_id
    WHERE ms.monitoring_id = p_monitoring_id
    GROUP BY ms.monitoring_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `logEvent` (IN `p_monitoring_id` INT, IN `p_alert_type` VARCHAR(50))   BEGIN
    INSERT INTO alert_service (monitoring_id, alert_type, cooldown_time)
    VALUES (p_monitoring_id, p_alert_type, 0);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `onDrowsinessDetected` (IN `p_monitoring_id` INT)   BEGIN
    UPDATE monitoring_session 
    SET drowsy_events = drowsy_events + 1, total_alerts = total_alerts + 1 
    WHERE monitoring_id = p_monitoring_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `pauseTimer` (IN `p_session_id` INT, IN `p_remaining` INT)   BEGIN
    INSERT INTO timer_log (session_id, action, remaining_seconds)
    VALUES (p_session_id, 'pause', p_remaining);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `penalizeDrowsiness` (IN `p_user_id` INT, IN `p_drowsy_count` INT)   BEGIN
    UPDATE user_statistics 
    SET total_drowsy_events = total_drowsy_events + p_drowsy_count,
        avg_focus_score = GREATEST(avg_focus_score - (p_drowsy_count * 2.0), 0)
    WHERE user_id = p_user_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `resetFaceData` (IN `p_monitoring_id` INT)   BEGIN
    DELETE FROM face_data_model 
    WHERE monitoring_id = p_monitoring_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `saveChatHistory` (IN `p_user_id` INT, IN `p_session_id` VARCHAR(100))   BEGIN
    INSERT INTO chat_history (user_id, session_id)
    VALUES (p_user_id, p_session_id);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `saveMonitoringLog` (IN `p_session_id` INT)   BEGIN
    INSERT INTO monitoring_session (session_id, start_time)
    VALUES (p_session_id, NOW());
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `saveSession` (IN `p_user_id` INT, IN `p_duration` INT, IN `p_method_type` VARCHAR(50), IN `p_monitoring_enabled` BOOLEAN)   BEGIN
    INSERT INTO session_data (user_id, duration, method_type, monitoring_enabled)
    VALUES (p_user_id, p_duration, p_method_type, p_monitoring_enabled);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sendMessage` (IN `p_chat_history_id` INT, IN `p_role` VARCHAR(20), IN `p_content` TEXT)   BEGIN
    INSERT INTO chat_message (chat_history_id, role, content)
    VALUES (p_chat_history_id, p_role, p_content);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `showPopup` (IN `p_monitoring_id` INT, IN `p_cooldown` INT)   BEGIN
    INSERT INTO alert_service (monitoring_id, alert_type, cooldown_time)
    VALUES (p_monitoring_id, 'popup', p_cooldown);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `startFeynmanSession` (IN `p_user_id` INT, IN `p_duration` INT, IN `p_monitoring_enabled` BOOLEAN)   BEGIN
    INSERT INTO session_data (user_id, duration, method_type, chat_session_id, drowsy_count, monitoring_enabled)
    VALUES (p_user_id, p_duration, 'Feynman', CONCAT('CHAT-', LPAD(FLOOR(RAND() * 10000), 4, '0')), 0, p_monitoring_enabled);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `startMonitoring` (IN `p_session_id` INT)   BEGIN
    INSERT INTO monitoring_session (session_id, start_time, drowsy_events, total_alerts, is_active)
    VALUES (p_session_id, NOW(), 0, 0, TRUE);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `startTimer` (IN `p_session_id` INT, IN `p_duration_seconds` INT)   BEGIN
    INSERT INTO timer_log (session_id, action, remaining_seconds)
    VALUES (p_session_id, 'start', p_duration_seconds);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `stopMonitoring` (IN `p_monitoring_id` INT)   BEGIN
    UPDATE monitoring_session 
    SET end_time = NOW(), is_active = FALSE 
    WHERE monitoring_id = p_monitoring_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `stopTimer` (IN `p_session_id` INT)   BEGIN
    INSERT INTO timer_log (session_id, action, remaining_seconds)
    VALUES (p_session_id, 'stop', 0);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `triggerSound` (IN `p_monitoring_id` INT, IN `p_cooldown` INT)   BEGIN
    INSERT INTO alert_service (monitoring_id, alert_type, cooldown_time)
    VALUES (p_monitoring_id, 'sound', p_cooldown);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `triggerVibration` (IN `p_monitoring_id` INT, IN `p_cooldown` INT)   BEGIN
    INSERT INTO alert_service (monitoring_id, alert_type, cooldown_time)
    VALUES (p_monitoring_id, 'vibration', p_cooldown);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `updateStreak` (IN `p_user_id` INT)   BEGIN
    UPDATE user_statistics 
    SET current_streak = current_streak + 1 
    WHERE user_id = p_user_id;
END$$

--
-- Fungsi
--
CREATE DEFINER=`root`@`localhost` FUNCTION `calculateFocusBonus` (`p_duration` INT, `p_drowsy_count` INT) RETURNS FLOAT DETERMINISTIC BEGIN
    DECLARE focus_ratio FLOAT;
    IF p_duration = 0 THEN
        RETURN 0.0;
    END IF;
    SET focus_ratio = 1.0 - (p_drowsy_count / p_duration);
    RETURN ROUND(focus_ratio * 50, 2);
END$$

CREATE DEFINER=`root`@`localhost` FUNCTION `calculateXP` (`p_duration` INT, `p_drowsy_count` INT) RETURNS INT(11) DETERMINISTIC BEGIN
    DECLARE base_xp INT;
    DECLARE penalty INT;
    SET base_xp = p_duration * 5;
    SET penalty = p_drowsy_count * 10;
    RETURN GREATEST(base_xp - penalty, 0);
END$$

CREATE DEFINER=`root`@`localhost` FUNCTION `isSleepy` (`p_ear` FLOAT, `p_threshold` FLOAT) RETURNS TINYINT(1) DETERMINISTIC BEGIN
    IF p_ear < p_threshold THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` FUNCTION `validateDuration` (`p_duration` INT) RETURNS TINYINT(1) DETERMINISTIC BEGIN
    IF p_duration > 0 AND p_duration <= 180 THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Struktur dari tabel `ai_service`
--

CREATE TABLE `ai_service` (
  `service_id` int(11) NOT NULL,
  `api_key` varchar(255) NOT NULL COMMENT 'API Key untuk layanan AI',
  `model_name` varchar(100) NOT NULL COMMENT 'Nama model AI yang digunakan',
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `ai_service`
--

INSERT INTO `ai_service` (`service_id`, `api_key`, `model_name`, `is_active`, `created_at`) VALUES
(1, 'sk-abc123def456ghi789', 'gpt-4o', 1, '2026-04-15 21:39:53'),
(2, 'sk-xyz987uvw654rst321', 'gpt-3.5-turbo', 0, '2026-04-15 21:39:53'),
(3, 'sk-mno456pqr123stu789', 'gemini-pro', 1, '2026-04-15 21:39:53'),
(4, 'sk-jkl321wxy654abc987', 'claude-3-opus', 0, '2026-04-15 21:39:53'),
(5, 'sk-ghi789def456mno123', 'gpt-4o-mini', 1, '2026-04-15 21:39:53');

-- --------------------------------------------------------

--
-- Struktur dari tabel `alert_service`
--

CREATE TABLE `alert_service` (
  `alert_id` int(11) NOT NULL,
  `monitoring_id` int(11) NOT NULL,
  `alert_type` varchar(50) NOT NULL COMMENT 'Tipe alert: sound, vibration, popup',
  `cooldown_time` int(11) NOT NULL DEFAULT 30 COMMENT 'Waktu cooldown antar alert (detik)',
  `triggered_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `alert_service`
--

INSERT INTO `alert_service` (`alert_id`, `monitoring_id`, `alert_type`, `cooldown_time`, `triggered_at`) VALUES
(1, 1, 'sound', 30, '2026-04-15 08:20:00'),
(2, 1, 'popup', 30, '2026-04-15 08:35:00'),
(3, 3, 'vibration', 20, '2026-04-15 10:10:00'),
(4, 3, 'sound', 20, '2026-04-15 10:18:00'),
(5, 5, 'popup', 25, '2026-04-15 14:12:00');

-- --------------------------------------------------------

--
-- Struktur dari tabel `camera_ui`
--

CREATE TABLE `camera_ui` (
  `camera_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `is_active` tinyint(1) DEFAULT 0 COMMENT 'Status kamera aktif/tidak',
  `last_status_check` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `camera_ui`
--

INSERT INTO `camera_ui` (`camera_id`, `user_id`, `is_active`, `last_status_check`) VALUES
(1, 1, 1, '2026-04-15 08:00:00'),
(2, 2, 1, '2026-04-15 09:30:00'),
(3, 3, 0, '2026-04-15 10:30:00'),
(4, 4, 1, '2026-04-15 11:00:00'),
(5, 5, 0, '2026-04-15 14:25:00');

-- --------------------------------------------------------

--
-- Struktur dari tabel `chat_history`
--

CREATE TABLE `chat_history` (
  `chat_history_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `session_id` varchar(100) NOT NULL COMMENT 'ID sesi chat',
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `chat_history`
--

INSERT INTO `chat_history` (`chat_history_id`, `user_id`, `session_id`, `timestamp`) VALUES
(1, 1, 'CHAT-001', '2026-04-15 08:05:00'),
(2, 2, 'CHAT-002', '2026-04-15 09:35:00'),
(3, 3, 'CHAT-003', '2026-04-15 10:05:00'),
(4, 4, 'CHAT-004', '2026-04-15 11:10:00'),
(5, 5, 'CHAT-005', '2026-04-15 14:05:00');

-- --------------------------------------------------------

--
-- Struktur dari tabel `chat_message`
--

CREATE TABLE `chat_message` (
  `message_id` int(11) NOT NULL,
  `chat_history_id` int(11) NOT NULL,
  `role` varchar(20) NOT NULL COMMENT 'Peran: user, assistant, system',
  `content` text NOT NULL COMMENT 'Isi pesan',
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `chat_message`
--

INSERT INTO `chat_message` (`message_id`, `chat_history_id`, `role`, `content`, `timestamp`) VALUES
(1, 1, 'user', 'Jelaskan konsep fotosintesis menggunakan metode Feynman', '2026-04-15 08:05:30'),
(2, 1, 'assistant', 'Fotosintesis adalah proses dimana tumbuhan mengubah cahaya matahari menjadi energi...', '2026-04-15 08:05:35'),
(3, 2, 'user', 'Apa itu machine learning?', '2026-04-15 09:35:10'),
(4, 3, 'user', 'Bantu saya memahami konsep rekursif', '2026-04-15 10:05:20'),
(5, 4, 'system', 'Sesi deep work dimulai. Fokus pada materi Struktur Data.', '2026-04-15 11:10:05');

-- --------------------------------------------------------

--
-- Struktur dari tabel `drowsiness_detector`
--

CREATE TABLE `drowsiness_detector` (
  `detector_id` int(11) NOT NULL,
  `monitoring_id` int(11) NOT NULL,
  `threshold` float NOT NULL DEFAULT 0.25 COMMENT 'Threshold EAR untuk deteksi kantuk',
  `sensitivity` int(11) NOT NULL DEFAULT 3 COMMENT 'Sensitivitas deteksi (1-5)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `drowsiness_detector`
--

INSERT INTO `drowsiness_detector` (`detector_id`, `monitoring_id`, `threshold`, `sensitivity`) VALUES
(1, 1, 0.25, 3),
(2, 2, 0.25, 3),
(3, 3, 0.2, 4),
(4, 4, 0.25, 2),
(5, 5, 0.22, 5);

-- --------------------------------------------------------

--
-- Struktur dari tabel `face_data_model`
--

CREATE TABLE `face_data_model` (
  `face_data_id` int(11) NOT NULL,
  `monitoring_id` int(11) NOT NULL,
  `eye_aspect_ratio` float NOT NULL COMMENT 'Rasio aspek mata (EAR)',
  `blink_count` int(11) DEFAULT 0 COMMENT 'Jumlah kedipan mata',
  `head_pose` varchar(50) DEFAULT 'forward' COMMENT 'Posisi kepala (forward, left, right, down, up)',
  `confidence` float DEFAULT 0 COMMENT 'Tingkat kepercayaan deteksi',
  `recorded_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `face_data_model`
--

--INSERT INTO `face_data_model` (`face_data_id`, `monitoring_id`, `eye_aspect_ratio`, `blink_count`, `head_pose`, `confidence`, `recorded_at`) VALUES
--(1, 1, 0.28, 15, 'forward', 0.95, '2026-04-15 08:10:00'),
--(2, 2, 0.32, 22, 'forward', 0.98, '2026-04-15 09:45:00'),
--(3, 3, 0.18, 8, 'down', 0.87, '2026-04-15 10:15:00'),
--(4, 4, 0.3, 20, 'forward', 0.96, '2026-04-15 11:30:00'),
--(5, 5, 0.21, 10, 'left', 0.89, '2026-04-15 14:15:00');

-- --------------------------------------------------------

--
-- Struktur dari tabel `gamification_log`
--

CREATE TABLE `gamification_log` (
  `log_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `session_id` int(11) DEFAULT NULL,
  `xp_earned` int(11) DEFAULT 0 COMMENT 'XP yang didapat',
  `focus_bonus` float DEFAULT 0 COMMENT 'Bonus fokus',
  `drowsy_penalty` float DEFAULT 0 COMMENT 'Penalti kantuk',
  `streak_updated` tinyint(1) DEFAULT 0,
  `calculated_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `gamification_log`
--

INSERT INTO `gamification_log` (`log_id`, `user_id`, `session_id`, `xp_earned`, `focus_bonus`, `drowsy_penalty`, `streak_updated`, `calculated_at`) VALUES
(1, 1, 1, 120, 15, 10, 1, '2026-04-15 21:39:53'),
(2, 2, 2, 200, 25, 0, 1, '2026-04-15 21:39:53'),
(3, 3, 3, 50, 5, 30, 0, '2026-04-15 21:39:53'),
(4, 4, 4, 350, 40, 2, 1, '2026-04-15 21:39:53'),
(5, 5, 5, 80, 10, 18, 1, '2026-04-15 21:39:53');

-- --------------------------------------------------------

--
-- Struktur dari tabel `monitoring_session`
--

CREATE TABLE `monitoring_session` (
  `monitoring_id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime DEFAULT NULL,
  `drowsy_events` int(11) DEFAULT 0 COMMENT 'Jumlah event kantuk',
  `total_alerts` int(11) DEFAULT 0 COMMENT 'Total alert yang dikirim',
  `is_active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `monitoring_session`
--

INSERT INTO `monitoring_session` (`monitoring_id`, `session_id`, `start_time`, `end_time`, `drowsy_events`, `total_alerts`, `is_active`) VALUES
(1, 1, '2026-04-15 08:00:00', '2026-04-15 08:45:00', 2, 3, 0),
(2, 2, '2026-04-15 09:30:00', '2026-04-15 10:30:00', 0, 0, 0),
(3, 3, '2026-04-15 10:00:00', '2026-04-15 10:30:00', 5, 7, 0),
(4, 4, '2026-04-15 11:00:00', '2026-04-15 12:30:00', 1, 1, 0),
(5, 5, '2026-04-15 14:00:00', NULL, 3, 4, 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `session_data`
--

CREATE TABLE `session_data` (
  `session_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `duration` int(11) NOT NULL COMMENT 'Durasi sesi dalam menit',
  `method_type` varchar(50) NOT NULL COMMENT 'Tipe metode belajar (Feynman, Pomodoro, dll)',
  `timestamp` datetime DEFAULT current_timestamp(),
  `chat_session_id` varchar(100) DEFAULT NULL COMMENT 'ID sesi chatbot terkait',
  `drowsy_count` int(11) DEFAULT 0 COMMENT 'Jumlah kantuk selama sesi',
  `monitoring_enabled` tinyint(1) DEFAULT 0 COMMENT 'Apakah monitoring aktif'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `session_data`
--

INSERT INTO `session_data` (`session_id`, `user_id`, `duration`, `method_type`, `timestamp`, `chat_session_id`, `drowsy_count`, `monitoring_enabled`) VALUES
(1, 1, 45, 'Feynman', '2026-04-15 08:00:00', 'CHAT-001', 2, 1),
(2, 2, 60, 'Pomodoro', '2026-04-15 09:30:00', 'CHAT-002', 0, 1),
(3, 3, 30, 'Feynman', '2026-04-15 10:00:00', 'CHAT-003', 5, 1),
(4, 4, 90, 'Deep Work', '2026-04-15 11:00:00', 'CHAT-004', 1, 1),
(5, 5, 25, 'Pomodoro', '2026-04-15 14:00:00', 'CHAT-005', 3, 0);

-- --------------------------------------------------------

--
-- Struktur dari tabel `timer_log`
--

CREATE TABLE `timer_log` (
  `timer_id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `action` varchar(20) NOT NULL COMMENT 'start, pause, stop',
  `action_time` datetime DEFAULT current_timestamp(),
  `remaining_seconds` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `timer_log`
--

INSERT INTO `timer_log` (`timer_id`, `session_id`, `action`, `action_time`, `remaining_seconds`) VALUES
(1, 1, 'start', '2026-04-15 08:00:00', 2700),
(2, 1, 'stop', '2026-04-15 08:45:00', 0),
(3, 2, 'start', '2026-04-15 09:30:00', 3600),
(4, 2, 'pause', '2026-04-15 10:00:00', 1800),
(5, 3, 'start', '2026-04-15 10:00:00', 1800);

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

--INSERT INTO `users` (`user_id`, `username`, `email`, `password_hash`, `created_at`) VALUES
--(1, 'andi_pratama', 'andi.pratama@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', '2026-04-15 21:39:53'),
--(2, 'siti_nurhaliza', 'siti.nurhaliza@email.com', '56c867c56f09f4c19c8c96e50008ac79863ba3969503b1060d2609104ff9ce6d', '2026-04-15 21:39:53'),
--(3, 'budi_santoso', 'budi.santoso@email.com', '3775b9c2c0e7fd4746e070998c64104bdf5401af7e03a0d6ebb7995bc141d641', '2026-04-15 21:39:53'),
--(4, 'dewi_lestari', 'dewi.lestari@email.com', '58ffe61279708ee01a207f1f0390716169b176c45716e4467ccee93c6e6a745f', '2026-04-15 21:39:53'),
--(5, 'rizky_maulana', 'rizky.maulana@email.com', '7f0148c19de0071b6413e2dbf5ba4d5e409e9122549f9b69604322f42dc83b5b', '2026-04-15 21:39:53');

-- --------------------------------------------------------

--
-- Struktur dari tabel `user_statistics`
--

CREATE TABLE `user_statistics` (
  `stat_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `total_xp` int(11) DEFAULT 0 COMMENT 'Total Experience Points',
  `current_streak` int(11) DEFAULT 0 COMMENT 'Streak belajar berturut-turut (hari)',
  `total_drowsy_events` int(11) DEFAULT 0 COMMENT 'Total kejadian kantuk terdeteksi',
  `avg_focus_score` float DEFAULT 0 COMMENT 'Rata-rata skor fokus',
  `chat_interactions` int(11) DEFAULT 0 COMMENT 'Jumlah interaksi chatbot'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `user_statistics`
--

--INSERT INTO `user_statistics` (`stat_id`, `user_id`, `total_xp`, `current_streak`, `total_drowsy_events`, `avg_focus_score`, `chat_interactions`) VALUES
--(1, 1, 1500, 7, 12, 85.5, 34),
--(2, 2, 2300, 14, 5, 92.3, 56),
--(3, 3, 800, 3, 25, 68.7, 15),
--(4, 4, 3100, 21, 3, 95.1, 78),
--(5, 5, 1200, 5, 18, 74.2, 22);

-- --------------------------------------------------------

--
-- Stand-in struktur untuk tampilan `v_camera_status`
-- (Lihat di bawah untuk tampilan aktual)
--
CREATE TABLE `v_camera_status` (
`camera_id` int(11)
,`username` varchar(100)
,`is_active` tinyint(1)
,`last_status_check` datetime
,`monitoring_active` tinyint(1)
);

-- --------------------------------------------------------

--
-- Stand-in struktur untuk tampilan `v_feynman_sessions`
-- (Lihat di bawah untuk tampilan aktual)
--
CREATE TABLE `v_feynman_sessions` (
`session_id` int(11)
,`username` varchar(100)
,`duration` int(11)
,`timestamp` datetime
,`drowsy_count` int(11)
,`monitoring_enabled` tinyint(1)
,`chat_history_id` int(11)
,`total_messages` bigint(21)
);

-- --------------------------------------------------------

--
-- Stand-in struktur untuk tampilan `v_homepage`
-- (Lihat di bawah untuk tampilan aktual)
--
CREATE TABLE `v_homepage` (
`user_id` int(11)
,`username` varchar(100)
,`total_xp` int(11)
,`current_streak` int(11)
,`avg_focus_score` float
,`total_sessions` bigint(21)
);

-- --------------------------------------------------------

--
-- Stand-in struktur untuk tampilan `v_statistics`
-- (Lihat di bawah untuk tampilan aktual)
--
CREATE TABLE `v_statistics` (
`username` varchar(100)
,`total_xp` int(11)
,`current_streak` int(11)
,`total_drowsy_events` int(11)
,`avg_focus_score` float
,`chat_interactions` int(11)
,`total_sessions` bigint(21)
,`total_study_minutes` decimal(32,0)
,`avg_drowsy_per_session` decimal(14,4)
);

-- --------------------------------------------------------

--
-- Struktur untuk view `v_camera_status`
--
DROP TABLE IF EXISTS `v_camera_status`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_camera_status`  AS SELECT `cu`.`camera_id` AS `camera_id`, `u`.`username` AS `username`, `cu`.`is_active` AS `is_active`, `cu`.`last_status_check` AS `last_status_check`, `ms`.`is_active` AS `monitoring_active` FROM (((`camera_ui` `cu` join `users` `u` on(`cu`.`user_id` = `u`.`user_id`)) left join `session_data` `sd` on(`cu`.`user_id` = `sd`.`user_id`)) left join `monitoring_session` `ms` on(`sd`.`session_id` = `ms`.`session_id` and `ms`.`is_active` = 1)) ;

-- --------------------------------------------------------

--
-- Struktur untuk view `v_feynman_sessions`
--
DROP TABLE IF EXISTS `v_feynman_sessions`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_feynman_sessions`  AS SELECT `sd`.`session_id` AS `session_id`, `u`.`username` AS `username`, `sd`.`duration` AS `duration`, `sd`.`timestamp` AS `timestamp`, `sd`.`drowsy_count` AS `drowsy_count`, `sd`.`monitoring_enabled` AS `monitoring_enabled`, `ch`.`chat_history_id` AS `chat_history_id`, count(`cm`.`message_id`) AS `total_messages` FROM (((`session_data` `sd` join `users` `u` on(`sd`.`user_id` = `u`.`user_id`)) left join `chat_history` `ch` on(`sd`.`chat_session_id` = `ch`.`session_id`)) left join `chat_message` `cm` on(`ch`.`chat_history_id` = `cm`.`chat_history_id`)) WHERE `sd`.`method_type` = 'Feynman' GROUP BY `sd`.`session_id` ;

-- --------------------------------------------------------

--
-- Struktur untuk view `v_homepage`
--
DROP TABLE IF EXISTS `v_homepage`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_homepage`  AS SELECT `u`.`user_id` AS `user_id`, `u`.`username` AS `username`, `us`.`total_xp` AS `total_xp`, `us`.`current_streak` AS `current_streak`, `us`.`avg_focus_score` AS `avg_focus_score`, (select count(0) from `session_data` `sd` where `sd`.`user_id` = `u`.`user_id`) AS `total_sessions` FROM (`users` `u` left join `user_statistics` `us` on(`u`.`user_id` = `us`.`user_id`)) ;

-- --------------------------------------------------------

--
-- Struktur untuk view `v_statistics`
--
DROP TABLE IF EXISTS `v_statistics`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_statistics`  AS SELECT `u`.`username` AS `username`, `us`.`total_xp` AS `total_xp`, `us`.`current_streak` AS `current_streak`, `us`.`total_drowsy_events` AS `total_drowsy_events`, `us`.`avg_focus_score` AS `avg_focus_score`, `us`.`chat_interactions` AS `chat_interactions`, count(distinct `sd`.`session_id`) AS `total_sessions`, sum(`sd`.`duration`) AS `total_study_minutes`, avg(`sd`.`drowsy_count`) AS `avg_drowsy_per_session` FROM ((`users` `u` left join `user_statistics` `us` on(`u`.`user_id` = `us`.`user_id`)) left join `session_data` `sd` on(`u`.`user_id` = `sd`.`user_id`)) GROUP BY `u`.`user_id` ;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `ai_service`
--
ALTER TABLE `ai_service`
  ADD PRIMARY KEY (`service_id`);

--
-- Indeks untuk tabel `alert_service`
--
ALTER TABLE `alert_service`
  ADD PRIMARY KEY (`alert_id`),
  ADD KEY `monitoring_id` (`monitoring_id`);

--
-- Indeks untuk tabel `camera_ui`
--
ALTER TABLE `camera_ui`
  ADD PRIMARY KEY (`camera_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `chat_history`
--
ALTER TABLE `chat_history`
  ADD PRIMARY KEY (`chat_history_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `chat_message`
--
ALTER TABLE `chat_message`
  ADD PRIMARY KEY (`message_id`),
  ADD KEY `chat_history_id` (`chat_history_id`);

--
-- Indeks untuk tabel `drowsiness_detector`
--
ALTER TABLE `drowsiness_detector`
  ADD PRIMARY KEY (`detector_id`),
  ADD KEY `monitoring_id` (`monitoring_id`);

--
-- Indeks untuk tabel `face_data_model`
--
ALTER TABLE `face_data_model`
  ADD PRIMARY KEY (`face_data_id`),
  ADD KEY `monitoring_id` (`monitoring_id`);

--
-- Indeks untuk tabel `gamification_log`
--
ALTER TABLE `gamification_log`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `session_id` (`session_id`);

--
-- Indeks untuk tabel `monitoring_session`
--
ALTER TABLE `monitoring_session`
  ADD PRIMARY KEY (`monitoring_id`),
  ADD KEY `session_id` (`session_id`);

--
-- Indeks untuk tabel `session_data`
--
ALTER TABLE `session_data`
  ADD PRIMARY KEY (`session_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `timer_log`
--
ALTER TABLE `timer_log`
  ADD PRIMARY KEY (`timer_id`),
  ADD KEY `session_id` (`session_id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indeks untuk tabel `user_statistics`
--
ALTER TABLE `user_statistics`
  ADD PRIMARY KEY (`stat_id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `ai_service`
--
ALTER TABLE `ai_service`
  MODIFY `service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `alert_service`
--
ALTER TABLE `alert_service`
  MODIFY `alert_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `camera_ui`
--
ALTER TABLE `camera_ui`
  MODIFY `camera_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `chat_history`
--
ALTER TABLE `chat_history`
  MODIFY `chat_history_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `chat_message`
--
ALTER TABLE `chat_message`
  MODIFY `message_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `drowsiness_detector`
--
ALTER TABLE `drowsiness_detector`
  MODIFY `detector_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `face_data_model`
--
ALTER TABLE `face_data_model`
  MODIFY `face_data_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `gamification_log`
--
ALTER TABLE `gamification_log`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `monitoring_session`
--
ALTER TABLE `monitoring_session`
  MODIFY `monitoring_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `session_data`
--
ALTER TABLE `session_data`
  MODIFY `session_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `timer_log`
--
ALTER TABLE `timer_log`
  MODIFY `timer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `user_statistics`
--
ALTER TABLE `user_statistics`
  MODIFY `stat_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `alert_service`
--
ALTER TABLE `alert_service`
  ADD CONSTRAINT `alert_service_ibfk_1` FOREIGN KEY (`monitoring_id`) REFERENCES `monitoring_session` (`monitoring_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `camera_ui`
--
ALTER TABLE `camera_ui`
  ADD CONSTRAINT `camera_ui_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `chat_history`
--
ALTER TABLE `chat_history`
  ADD CONSTRAINT `chat_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `chat_message`
--
ALTER TABLE `chat_message`
  ADD CONSTRAINT `chat_message_ibfk_1` FOREIGN KEY (`chat_history_id`) REFERENCES `chat_history` (`chat_history_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `drowsiness_detector`
--
ALTER TABLE `drowsiness_detector`
  ADD CONSTRAINT `drowsiness_detector_ibfk_1` FOREIGN KEY (`monitoring_id`) REFERENCES `monitoring_session` (`monitoring_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `face_data_model`
--
ALTER TABLE `face_data_model`
  ADD CONSTRAINT `face_data_model_ibfk_1` FOREIGN KEY (`monitoring_id`) REFERENCES `monitoring_session` (`monitoring_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `gamification_log`
--
ALTER TABLE `gamification_log`
  ADD CONSTRAINT `gamification_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `gamification_log_ibfk_2` FOREIGN KEY (`session_id`) REFERENCES `session_data` (`session_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `monitoring_session`
--
ALTER TABLE `monitoring_session`
  ADD CONSTRAINT `monitoring_session_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `session_data` (`session_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `session_data`
--
ALTER TABLE `session_data`
  ADD CONSTRAINT `session_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `timer_log`
--
ALTER TABLE `timer_log`
  ADD CONSTRAINT `timer_log_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `session_data` (`session_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `user_statistics`
--
ALTER TABLE `user_statistics`
  ADD CONSTRAINT `user_statistics_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
