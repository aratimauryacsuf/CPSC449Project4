PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS User;
CREATE TABLE User(user_id int primary key, username varchar, password varchar);

DROP TABLE IF EXISTS Game;
CREATE TABLE Game(game_id int primary key, user_id int, secretword text, guess_num int);

DROP TABLE IF EXISTS In_Progress;
CREATE TABLE In_Progress(user_id int, game_id int);

DROP TABLE IF EXISTS Completed;
CREATE TABLE Completed(user_id int, game_id int, guess_num int); 

DROP TABLE IF EXISTS Guesses;
CREATE TABLE Guesses(game_id int, guess_num int, guess_word text);

INSERT INTO User VALUES (1, "Arati", "pass123");
INSERT INTO User VALUES (2, "Ayush", "pass456");
INSERT INTO User VALUES (3, "Dillon", "pass789");

INSERT INTO Game VALUES (1, 1, "rares", 2);
INSERT INTO Game VALUES (2, 1, "quits", 1);
INSERT INTO Game VALUES (3, 1, "rusky", 3);
INSERT INTO Game VALUES (4, 2, "skews", 1);
INSERT INTO Game VALUES (5, 2, "laval", 2);
INSERT INTO Game VALUES (6, 2, "ambos", 2);
INSERT INTO Game VALUES (7, 3, "midis", 2);
INSERT INTO Game VALUES (8, 3, "scuff", 1);
INSERT INTO Game VALUES (9, 3, "yoofs", 3);

INSERT INTO In_Progress VALUES (1, 1);
INSERT INTO In_Progress VALUES (1, 2);
INSERT INTO In_Progress VALUES (1, 3);
INSERT INTO In_Progress VALUES (2, 4);
INSERT INTO In_Progress VALUES (2, 5);
INSERT INTO In_Progress VALUES (2, 6);
INSERT INTO In_Progress VALUES (3, 7);
INSERT INTO In_Progress VALUES (3, 8);
INSERT INTO In_Progress VALUES (3, 9);

INSERT INTO Completed VALUES (1, 10, 3);
INSERT INTO Completed VALUES (2, 11, 2);
INSERT INTO Completed VALUES (3, 12, 4);

INSERT INTO Guesses VALUES (1, 1, "vagus");
INSERT INTO Guesses VALUES (1, 2, "upsee");
INSERT INTO Guesses VALUES (2, 1, "ukase");
INSERT INTO Guesses VALUES (3, 1, "villi");
INSERT INTO Guesses VALUES (3, 2, "whyda");
INSERT INTO Guesses VALUES (3, 3, "voids");
INSERT INTO Guesses VALUES (4, 1, "wasts");
INSERT INTO Guesses VALUES (5, 1, "gonef");
INSERT INTO Guesses VALUES (5, 2, "giron");
INSERT INTO Guesses VALUES (6, 1, "grrls");
INSERT INTO Guesses VALUES (6, 2, "gurry");
INSERT INTO Guesses VALUES (7, 1, "hecht");
INSERT INTO Guesses VALUES (7, 2, "hyson");
INSERT INTO Guesses VALUES (8, 1, "hyphy");
INSERT INTO Guesses VALUES (9, 1, "firie");
INSERT INTO Guesses VALUES (9, 2, "ollie");
INSERT INTO Guesses VALUES (9, 3, "ology");

COMMIT;



