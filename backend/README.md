# Python (Fast API) Application

This is a Python-based FastAPI application that interacts with OpenAI's API for a drive-thru ordering system. The application processes user inputs to extract order details, maintains in-memory storage of orders, and provides an API for order management.

---

## Features
- Process drive-thru orders through OpenAI API integration.
- Place, cancel, and summarize orders.
- REST API built using FastAPI.

---

## Prerequisites
Before you begin, ensure you have the following installed on your system:

- Python 3.11 or later
- pip (Python package manager)
- Virtualenv (optional but recommended)

---

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/baidush/voker-assestment
cd voker-assestment
```

### Step 2: Set Up a Virtual Environment
(optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
Install the required Python packages:
```bash
cd backend
pip install --upgrade pip
pip install build
pip install .

```

### Step 4: Set Up OpenAI API Key
Rename a `.env-example` file in the project root and add the following:
```env
OPENAI_API_KEY=your-openai-api-key
```

Replace `your-openai-api-key` with your actual API key.

---

## Running the Application

### Run the FastAPI Server
```bash
uvicorn app.api:app --reload
```

The application will be accessible at `http://127.0.0.1:8000`.

### Endpoints
- `POST /parse_request` - Place or cancel an order.
- `GET /get_summary` - Retrieve the summary of all orders.

---

## Unit Tests

### Install Testing Dependencies
Ensure you have `pytest` installed:
```bash
pip install pytest
```

### Run Tests
Run the following command to execute the test suite:
```bash
pytest
```
---

## Running the Application with Docker and Docker Compose

### Build the Docker Image
Navigate to your project directory and run:
```bash
docker-compose build
```

### Run the Application
Start the application using:
```bash
docker-compose up
```

This will:
- Build the Docker image.
- Start the FastAPI application on port `8000`.

### Access the Application
Open your browser and navigate to:
```
http://localhost:8000
```

The API documentation is available at:
```
http://localhost:8000/docs
```

## License
[MIT License](LICENSE)

---

## Acknowledgments
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
