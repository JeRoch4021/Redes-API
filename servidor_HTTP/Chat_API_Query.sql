CREATE DATABASE chatdb;
DROP DATABASE chatdb;

USE chatdb;

CREATE TABLE users
(
	id INT PRIMARY KEY,
    username VARCHAR (50)
);

CREATE TABLE messages 
(
	id INT PRIMARY KEY NOT NULL,
    user_id INT,
    message_date DATE,
    message TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (id, username) VALUES
(1, 'Ivan&20Cadena');

INSERT INTO messages (id, user_id, message_date, message) VALUES
(1, 1, '2025-04-24', 'Hola, esta es una nota');

SELECT * FROM messages;
SELECT * FROM users;

SELECT p.id, u.username, p.message_date, p.message
            FROM users as u join messages as p on u.id = p.user_id
            WHERE u.username = 'Ivan&20Cadena';