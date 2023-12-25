# SocialMedia API

This is an implementation of api for a social media application, that allows users to post, vote content. Users can post text as well as images. Relational as well as noSQL is used.

## Installation

1. Clone this repository in your local folder. 
2. Create a relational postgress database.
3. Create an account at mongodb cloud and create a cluster.
4. For the cluster create two collections, one for the post and other for users.
5. Create a python virual environment and activate the environment.
```
python -m venv venv
source venv/Scripts/Activate.ps
```
5. Install the required packages using below command.
```bash
pip install -r requirements.txt
```
6. Create a .env file for saving environment variables. The file should have following variables.

```
DATABASE_HOSTNAME = 
DATABASE_PORT = 
DATABASE_PASSWORD = 
DATABASE_NAME = 
DATABASE_USERNAME = =
SECRET_KEY = 
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 
ADMIN_PASSWORD = 
MONGODB_USERNAME = 
MONGODB_PASSWORD = 
MONGODB_CLUSTER = 
MONGODB_DB = 
MONGODB_COLLECTION_USERS = 
MONGODB_COLLECTION_POSTS = 
```

## Usage
Use POSTMON to test various api endpoints.

Use CURL for api endpoints serving images.\
Examples
```
curl -O -J -X GET -H "Authorization: Bearer <JWT_Token>" http://localhost:8000/post/image/<post>
```

## Contributing

Pull requests are welcome. Appreciate any  suggestions and improvements.

