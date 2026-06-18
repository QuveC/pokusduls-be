-- ============================================================
-- MIGRATION: Tambah kolom premium ke tabel users
-- Database: study_app (MariaDB / MySQL)
-- Tanggal: 2026-06-18
-- ============================================================

ALTER TABLE users
  ADD COLUMN is_premium           TINYINT(1)   NOT NULL DEFAULT 0      COMMENT 'Status premium user (1 = premium)',
  ADD COLUMN premium_activated_at DATETIME     NULL                    COMMENT 'Waktu admin mengaktifkan premium',
  ADD COLUMN premium_activated_by VARCHAR(100) NULL                    COMMENT 'Username admin yang mengaktifkan';

-- ============================================================
-- Untuk cek hasil migration:
--   DESCRIBE users;
--
-- Untuk aktifkan premium user secara manual (admin):
--   UPDATE users
--   SET is_premium = 1,
--       premium_activated_at = NOW(),
--       premium_activated_by = 'admin'
--   WHERE username = '<username_user>';
-- ============================================================
