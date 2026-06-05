-- Run inside EC2 MySQL: sudo mysql -u root

-- Create database
CREATE DATABASE iotdb;

-- Create user
CREATE USER 'admin'@'%' IDENTIFIED BY 'Admin1234!';

-- Grant permissions
GRANT ALL PRIVILEGES ON iotdb.* TO 'admin'@'%';

-- Required for AWS DMS CDC
GRANT BINLOG MONITOR ON *.* TO 'admin'@'%';

FLUSH PRIVILEGES;

-- Verify
SHOW GRANTS FOR 'admin'@'%';


-- ─────────────────────────────────────
-- Also add to: /etc/my.cnf.d/mariadb-server.cnf
-- Under [mysqld] section:
-- ─────────────────────────────────────

-- server-id=1
-- log-bin=mysql-bin
-- binlog-format=ROW
-- binlog_row_image=FULL
-- expire_logs_days=1

-- Then restart: sudo systemctl restart mariadb
