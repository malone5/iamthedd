
# IAMTHE DD
iamthedd, short for "I am the Designated Driver" is a story generator that depicts a night out with friends.
Users create an account that allows them to create groups of friends called "crews". When adding people to "crews" users assign
a personality trait that most applies to them when the go out drinking with friends. This "personality" will dictate how their story
is generated.

When a user wants to generate a story all they have to do is give the story a name, select a venue where the story will take place
(Bar, Club, House, ect.) and select the crew that will be involved.

The app then generates a short story for each member of the "crew" that will be told throught he perspective of the designated driver(the user).

http://malone5.pythonanywhere.com/

## Getting Started

- Clone the repo
```
$ git clone https://github.com/malone5/iamthedd.git
$ cd iamthedd
``` 
- create virtualenv and instal dependancies
```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
- Initialize database
```
$ python manage.py migrate
```
- Run dev server
```
$ python manage.py runserver
```

### Populating the database
You have your development server running. But there are no story templates! If you try to generate a story without story templates you will see that all stories are the same default template.
To help this, I create fixture data to get you going and populate the database so you don't have to start from scratch every time the database is initialized. 

Initialize simple default story templates 
 ```$ python manage.py loaddata fixture_story_templates.json```

Create an admin user ```(un:admin pw:admin)``` **development only!**
 ```$ python manage.py loaddata fixture_admin_user.json```

 
