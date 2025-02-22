
## Project Title
Djezzy is a web application developed with HTML, CSS, JavaScript, and Flask. It offers a user-friendly interface with distinct roles and functionalities for administrators, users, and supervisors. The application is in **French**.





## Features

- Role-based access control (Admin, User, Supervisor)
- Reclamation and history management for each role
- Admin capabilities to create and delete users, supervisors, and other admins
- Statistic page for the supervisors



## Installation

### Prerequisites

- Install [Docker](https://docs.docker.com/get-docker/)
- Install [Docker Compose](https://docs.docker.com/compose/install/)

### Steps

   1. Clone the repository:

       ```bash
       git clone git@github.com:Feddane/Djezzy.git
       ```

   2. Navigate to the project directory:
   
       ```bash 
       cd Djezzy
       ```

   3. Create a `.env` file (if not already present) and configure it:  

       ```bash
       cp .env.example .env
       ```

       Or manually set environment variables inside `.env`:  

       ```dotenv
       POSTGRES_USER=your_username
       POSTGRES_PASSWORD=your_password
       POSTGRES_DB=your_db
       SECRET_KEY=your-secret-key
       DATABASE_URL=postgresql://your_username:your_password@db/your_db
       ```

   4. Start the application with Docker:
   
       ```bash 
       docker-compose up -d --build
       ```

## Usage
After installation, open your web browser and go to http://127.0.0.1:5000/. You will be presented with a homepage offering three roles: Admin, User, and Supervisor. Select a role to proceed.



## Demo

You can view the live demo of the Djezzy application [here](https://djezzy.onrender.com)


## Feedback

If you have any feedback, please reach me out on my [LinkedIn](https://www.linkedin.com/in/cha%C3%AFma-feddane-27a003224/) account.

