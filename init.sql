CREATE TABLE IF NOT EXISTS user_transfers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_ref VARCHAR(255) UNIQUE,
    sender_name VARCHAR(255),
    phone_number VARCHAR(20),
    phone_confidence DECIMAL(6,4),
    amount DECIMAL(10,2),
    amount_confidence DECIMAL(6,4),
    transaction_date DATETIME,
    ocr_confidence DECIMAL(6,4),
    source_filename VARCHAR(255),
    user_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bank_transfers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_date DATETIME,
    amount DECIMAL(10,2),
    ref_id VARCHAR(255) UNIQUE,
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS matched_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_transfer_id INT,
    bank_transfer_id INT,
    matched_amount DECIMAL(10,2),
    amount_confidence DECIMAL(6,4),
    matched_phone VARCHAR(20),
    phone_confidence DECIMAL(6,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_transfer_id) REFERENCES user_transfers(id),
    FOREIGN KEY (bank_transfer_id) REFERENCES bank_transfers(id)
);

CREATE TABLE IF NOT EXISTS anomaly_user_transfers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_transfer_id INT,
    amount DECIMAL(10,2),
    reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_transfer_id) REFERENCES user_transfers(id)
);

CREATE TABLE IF NOT EXISTS anomaly_bank_transfers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bank_transfer_id INT,
    amount DECIMAL(10,2),
    reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bank_transfer_id) REFERENCES bank_transfers(id)
);