# Readme

This Python script scrapes reddit userpage using selenium and saves json files in D:/GIT/temp/

Currently get_comment is the only implemented. Will output url, title, myComment, context, post. To D:/GIT/temp/{username}get_comment.json

submitted, upvoted, downvoted can also be implemented. 

to launch create a .env in same directory with file schema below.
launch python ./main.py

```.env
webusername=username
webpassword=passwrord
```