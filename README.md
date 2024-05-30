# FastAPI Job Posting Application

This is a FastAPI application for posting and searching job listings. The application uses MongoDB for data storage and JWT (JSON Web Tokens) for authentication.

## Features

- User authentication with JWT
- CRUD operations for job postings
- Secure access to job listings for authenticated users

## Prerequisites

- Python 3.10
- MongoDB (local installation or MongoDB Atlas)
- Git (optional, for cloning the repository)

## Setup Instructions

### Clone the Repository

You can clone this repository using Git:

```bash
git clone https://github.com/your-username/fastapi-job-posting.git
cd fastapi-job-posting
```

# Create a virtual environment

python -m venv fastapi-jobs-env

# Activate the virtual environment (Windows)

fastapi-jobs-env\Scripts\activate

# Activate the virtual environment (Unix or MacOS)

source fastapi-jobs-env/bin/activate

# Install Requirements

`pip install -r requirements.txt`

# Run Application

`uvicorn app.main:app --reload`
