
import json
import sqlite3

file1 = open("./share/correct.json")

correct_word = json.load(file1)
length = len(correct_word)
# length += 1

file2 = open("./share/valid.json")

valid_word = json.load(file2)
length1 = len(valid_word)
# length1 += 1

connection = sqlite3.connect('./var/wordleGame.db')
cursor = connection.cursor()
# cursor.execute('Create Table if not exists Correct_Words(correctwordid int, correctword Text)')
# cursor.execute('Create Table if not exists Valid_Words (validwordid int, validword Text)')


for i in range(length):
    index = i+1
    cursor.execute('insert into Correct_Words(correct_word_id,correct_word) values(?,?)',(index, correct_word[i]))

for j in range(length1): 
     index = j+1
     cursor.execute('insert into Valid_Words(valid_word_id,valid_word) values(?,?)',(index, valid_word[j]))

connection.commit()

file1.close()
file2.close()




