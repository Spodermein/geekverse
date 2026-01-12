GeekVerse

GeekVerse is a full-stack blogging platform built with React, FastAPI, and MySQL, fully containerized using Docker Compose.
It supports role-based access (Admin/User), rich post creation, comments, bookmarks, and category management.
<img width="1896" height="925" alt="image" src="https://github.com/user-attachments/assets/60ecd9d8-cc9a-4c6c-aec4-ffbceb219efa" />



Tech Stack

Frontend

- React (SPA)
- React Router
- Axios
- Bootstrap
- Drag & Drop editor (@dnd-kit)
- Served via Nginx

Backend

- FastAPI
- SQLAlchemy
- MySQL
- JWT Authentication
- Passlib (bcrypt)
- Infrastructure

Docker

- Docker Compose
- Nginx
- MySQL 8.0

Features

- JWT Authentication (Register / Login)
- Role-based access (admin, user)
- Create / Edit / Delete posts (Admin only)
- Block-based post editor (text + images)
- Comments (edit/delete own comments)
- Bookmark posts
- Predefined categories
- Fully Dockerized (one command startup)

Project Structure
geekverse/
├── backend/
│   ├── routers/
│   ├── models/
│   ├── database.py
│   ├── main.py
│   └── Dockerfile
│
├── frontend/
│   └── geekverse-frontend/
│       ├── src/
│       │   ├── pages/
│       │   ├── components/
│       │   ├── api.js
│       │   └── App.js
│       ├── nginx.conf
│       └── Dockerfile
│
├── docker-compose.yml
├── .env
└── README.md

Environment Variables

Create a .env file in the project root:

MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DB=geekverse_db
MYSQL_USER=geekuser
MYSQL_PASSWORD=geekpassword

DATABASE_URL=mysql+pymysql://geekuser:geekpassword@mysql:3306/geekverse_db
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

Running the Project (Docker)

1. Build & start everything

docker compose up --build

2. Access the app

Frontend: http://localhost:3000
Backend API: http://localhost:8000
Swagger Docs: http://localhost:8000/docs

3. Admin Accounts

New users are created with role: user
Admin access is not selectable from frontend
Promote a user to admin (manual)
UPDATE users
SET role = 'admin'
WHERE username = 'your_username';


You can run this using:

docker exec -it geekverse-mysql mysql -u geekuser -p geekverse_db


Category Seeding

Categories are predefined:

Tech
Gaming
Dinosaurs & Comics
Gym & Sports
Others

If categories are missing, run the seed script manually inside backend:

docker exec -it geekverse-backend python seed_categories.py


📄 License

This project is for educational and portfolio purposes.


