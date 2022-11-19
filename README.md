# CPSC449Project2 - Group 20

### Group Members:
##### Arati Maurya
##### Aaditya Chaudhari
##### Anvit Rajesh Patil
##### Wesley Zoroya

---
## **Setting up NginxConfig**
#### Add Nginx config file "project2NginxConfig"  at path `/etc/nginx/sites-enabled`

## **Initializing Database & Start Service:**

##### `./bin/init.sh`
##### `foreman start -m user=1,game=3`

---

## **Testing the APIs**
### Note: In order to run the API, you will ocasionally have to to supply specific variables. Any time this is required, please replace the < variable > with the correct information.


### **User API**
#### `http://127.0.0.1:5000/docs`

#### User API get, will display the index page for user API.
#### `http GET  http://users.local.gd/` 

#### Registers a new user.
#### `http POST http://users.local.gd/user/registration username=<username> userpassword=<password>` 


### **Game API**
#### `http://127.0.0.1:5100/docs`

#### Game API get, will display the index page for game API.
#### `http --auth user:password http://games.local.gd/` 

#### Starts a new game for a player.
#### `http --auth user:password POST http://games.local.gd/newgame`

#### Allows the player to enter a 5 letter word to guess given a game ID.
#### `http --auth user:password http://games.local.gd/guess game_id=<game_ID> guess_word=<guess>`

#### Prints all in progress games for the player.
#### `http --auth user:password http://games.local.gd/inprogressgame/`

#### Prints the status of a game given a game ID.
#### `http --auth user:password http://games.local.gd/gamestatus/<game_ID>`

 

