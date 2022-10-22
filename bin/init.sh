#!/bin/sh

sqlite3 ./var/wordleGame.db< ./share/wordleschema.sql
python3 ./bin/copydata.py
