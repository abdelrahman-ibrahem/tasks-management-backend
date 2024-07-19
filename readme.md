# Task Management Backend Application

This Task Management Backend Application is built using FastAPI, providing APIs for task management and user authentication. The application uses an SQLite database.

## Packages Used

- `fastapi`
- `sqlalchemy`
- `passlib[bcrypt]`
- `python-multipart`

## Endpoints

### Task Endpoints

- **Get All Tasks**
  - **Endpoint**: `GET /tasks`
  
- **Get Task by ID**
  - **Endpoint**: `GET /tasks/{task_id}`
  
- **Create Task**
  - **Endpoint**: `POST /tasks`
  
- **Update Task**
  - **Endpoint**: `PUT /tasks/{task_id}`
  
- **Delete Task**
  - **Endpoint**: `DELETE /tasks/{task_id}`

### Authentication Endpoints

- **Register**
  - **Endpoint**: `POST /auth/register`
  
- **Login**
  - **Endpoint**: `POST /auth/login`
  
- **Get Profile**
  - **Endpoint**: `GET /auth/profile`

## Database

- **SQLite**

## Running the Application

1. Install dependencies:
   ```bash
   pip install fastapi sqlalchemy passlib[bcrypt] python-multipart
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

This will start the application on `http://127.0.0.1:8000`.