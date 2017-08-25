# secure-chat-api

### run locally
* run a mongo database named `chatter`
* install python 3
* create virtualenv `virtualenv -p python3 venv`
* run the virtualenv `source ven/bin/activate`
* install dependencies `pip3 install -r requirements.txt`
* run the server `python3 main.py`

### deploying
* clone [ecs-deploy](https://github.com/silinternational/ecs-deploy) into a ~/src folder
* `bash deploy.sh testing | production`

### todo
* delete old user when a new user is created with the same apn token
* use session tokens
