# Python Application

This is a Python-based FastAPI application that interacts with OpenAI's API for a drive-thru ordering system. The application processes user inputs to extract order details, maintains in-memory storage of orders, and provides an API for order management.

---

## Features
- Process drive-thru orders through OpenAI API integration.
- Place, cancel, and summarize orders.
- REST API built using FastAPI.

---

## Prerequisites
Before you begin, ensure you have the following installed on your system:

- Python 3.9 or later
- pip (Python package manager)
- Virtualenv (optional but recommended)

---

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
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
pip install -r requirements.txt
```

### Step 4: Set Up OpenAI API Key
The application requires an OpenAI API key. Create a `.env` file in the project root and add the following:
```env
OPENAI_API_KEY=your-openai-api-key
```

Replace `your-openai-api-key` with your actual API key.

---

## Running the Application

### Start the FastAPI Server
Run the following command to start the FastAPI server:
```bash
uvicorn app.api:app --reload
```

The application will be accessible at `http://127.0.0.1:8000`.

### Endpoints
- `POST /parse_request` - Place or cancel an order.
- `GET /get_summary` - Retrieve the summary of all orders.

---

## Running Tests

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

## Deployment
You can deploy this application using any WSGI-compatible server like Gunicorn or a cloud platform like AWS, GCP, or Azure.

Example for Gunicorn:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.api:app
```

---

## License
[MIT License](LICENSE)

---

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

---

## Contact
For issues or feature requests, please open an issue in this repository.

---

## Acknowledgments
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
