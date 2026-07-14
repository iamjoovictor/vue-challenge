-- Creates both databases on first container start.
-- MariaDB executes every file in /docker-entrypoint-initdb.d/ automatically.

CREATE DATABASE IF NOT EXISTS `vue-challenge`;
CREATE DATABASE IF NOT EXISTS `vue-challenge-test`;
