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

BEGIN TRANSACTION;
DROP TABLE IF EXISTS Correct_Words;
CREATE TABLE Correct_Words(
    correctwordid INTEGER primary key,
    correctword VARCHAR
);

DROP TABLE IF EXISTS Valid_Words;
CREATE TABLE Valid_Words(
    validwordid INTEGER primary key,
    validword VARCHAR
);

DROP TABLE IF EXISTS Games;
CREATE TABLE Games(
    gameid INTEGER primary key,
    userid INTEGER,
    secretword VARCHAR, 
    guesscount INTEGER,
    FOREIGN KEY(userid) REFERENCES user(userid)
);
COMMIT;