SET-UP BACKEND / API SERVICES
- Open a terminal
- Navigate into quitlong-app
- Execute the command: pip install virtualenv (To install virtualenv)
- Execute the command: virtualenv auth (To create virtualenv named auth)
- Open the virtual env by executing this in command: source auth/bin/activate
- Install requirements: pip install -r requirements.txt
- Execute export FLASK_APP=project
- Execute flask run

CURRENT CREDS
- email: admin@yopmail.com
- password: P@ssw0rd

- email: joanna@yopmail.com
- password: P@ssw0rd

- email: marie@yopmail.com
- password: P@ssw0rd

RUN THE REACT APP
- Open a terminal
- Navigate to react-frontend
- Execute npm install
- Execute npm start

ACCESS THE WEB
- Open browser and paste http://localhost:3000/login

SOME NOTES
I. If you want fresh database, kindly delete the db.sqlite inside the instance then set new credentials.
II. If you want to top up an account, make sure you have admin@yopmail.com account registered and use the endpoint top-up
III. Sample postman collected can find in the main directory