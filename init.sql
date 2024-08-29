use `edge_home_db`;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE user_face_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    face_data BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);


CREATE TABLE user_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255),
    log TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_email) REFERENCES user(email) ON DELETE CASCADE
);

CREATE TABLE device (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(255) UNIQUE NOT NULL,
    device_name VARCHAR(255) NOT NULL,
    place VARCHAR(255) NOT NULL,
    state BOOLEAN DEFAULT FALSE,
    device_type VARCHAR(100),
    device_metadata JSON
);


CREATE TABLE control_device_permission (
    id INT AUTO_INCREMENT PRIMARY KEY,
    master_device_id VARCHAR(255),
    slave_device_id VARCHAR(255),
    FOREIGN KEY (master_device_id) REFERENCES device(device_id) ON DELETE CASCADE,
    FOREIGN KEY (slave_device_id) REFERENCES device(device_id) ON DELETE CASCADE
);


CREATE TABLE device_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(255),
    log TEXT NOT NULL,
    action VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES device(device_id) ON DELETE CASCADE
);

CREATE TABLE permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    device_id VARCHAR(255),
    access_level ENUM('read', 'write', 'admin') DEFAULT 'read',
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (device_id) REFERENCES device(device_id) ON DELETE CASCADE
);

CREATE TABLE device_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_type VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(100)
);

-- Inserting default device types
INSERT INTO device_types (device_type, display_name) VALUES ('LIGHT', 'Light');
INSERT INTO device_types (device_type, display_name) VALUES ('FAN', 'Fan');
INSERT INTO device_types (device_type, display_name) VALUES ('AC', 'Air Conditioner');
INSERT INTO device_types (device_type, display_name) VALUES ('TV', 'Television');
INSERT INTO device_types (device_type, display_name) VALUES ('DOOR_LOCK', 'Door Lock');
INSERT INTO device_types (device_type, display_name) VALUES ('SWITCH', 'Switch');
INSERT INTO device_types (device_type, display_name) VALUES ('SAFETY', 'Safety Device');
