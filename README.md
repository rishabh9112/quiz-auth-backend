# Quiz Auth Backend (Dev Mode - No SMTP)

## Setup

python -m venv venv
Activate venv
pip install -r requirements.txt
uvicorn app.main:app --reload

Password reset tokens will be printed in terminal.
