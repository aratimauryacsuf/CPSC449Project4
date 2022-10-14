
import json
import sqlite3

file1 = open("./share/correct.json")
correct_word = json.load(file1)


file2 = open("./share/valid.json")
valid_word = json.load(file2)


connection = sqlite3.connect('./var/wordleGame.db')
cursor = connection.cursor()


for i in range(len(correct_word)):
    index = i+1
    cursor.execute('insert into Correct_Words(correct_word_id,correct_word) values(?,?)',(index, correct_word[i]))

for j in range(len(valid_word)): 
     index = j+1
     cursor.execute('insert into Valid_Words(valid_word_id,valid_word) values(?,?)',(index, valid_word[j]))

connection.commit()

file1.close()
file2.close()




