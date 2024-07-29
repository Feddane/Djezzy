
## Project Title
Djezzy is a web application developed with HTML, CSS, JavaScript, and Flask. It offers a user-friendly interface with distinct roles and functionalities for administrators, users, and supervisors. The application is in **French**.





## Features

- Role-based access control (Admin, User, Supervisor)
- Reclamation and history management for each role
- Admin capabilities to create and delete users, supervisors, and other admins
- Statistic page for the supervisors


## Installation

1- Clone the repository
```bash
  git clone git@github.com:Feddane/Djezzy.git
```

2- Navigate to the project directory
```bash
  cd Djezzy
```

3- Install the required dependencies
``` bash
    pip install -r requirements.txt
```

4- Modify the config.py file
``` bash
    class Config:
        SECRET_KEY = "your-secret-key"
        SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/database_name'
        SQLALCHEMY_TRACK_MODIFICATIONS = False

```

5- Run the application
``` bash
    python run.py
```
## Usage
After installation, open your web browser and go to http://127.0.0.1:5000/. You will be presented with a homepage offering three roles: Admin, User, and Supervisor. Select a role to proceed.



## Demo

You can view the live demo of the Djezzy application [here](https://djezzy.onrender.com)


## Feedback

If you have any feedback, please reach me out on my [LinkedIn](https://www.linkedin.com/in/cha%C3%AFma-feddane-27a003224/) account.

