-- $ sqlite3 ./var/wordleGame.db < ./share/wordleschema.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS user;
CREATE TABLE user (
    userid INTEGER primary key,  
    username VARCHAR,
    userpassword VARCHAR    
    );

INSERT INTO user(username, userpassword) VALUES('Arati', "abcd123");
INSERT INTO user(username, userpassword) VALUES('Dillon', "wxyz123");
INSERT INTO user(username, userpassword) VALUES('Ayush', "pqrs123");
INSERT INTO user(username, userpassword) VALUES('Nikhil', "ABCDEFG");
COMMIT;