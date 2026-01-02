# Personality API

This project provides a REST API powered by FastAPI and a simple frontend to interact with it. The API generates responses based on a given question, simulating different "personalities."

## Prerequisites

Before you begin, make sure you have the following installed:

* **Python 3.7+:**  Ensure you have a compatible Python version installed. You can download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).
* **pip:**  The Python package installer. It usually comes with Python.
* **uvicorn:** An ASGI server for running FastAPI applications.

## Installation

1. **Create a Project Directory:**
   ```bash
   mkdir personality_api
   cd personality_api
   ```

2. **Create a Virtual Environment (Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies:**
   ```bash
   pip install fastapi uvicorn requests
   ```

4. **Create `main.py`:** Create a file named `main.py` and paste the FastAPI application code into it (as provided in the previous responses).

5. **Create `index.html`:** Create a file named `index.html` and paste the frontend HTML code into it (as provided in the previous responses).  Place it in the root of your project directory.

## Running the Application

1. **Start the Uvicorn Server:**
   ```bash
   uvicorn main:app --reload
   ```
   The `--reload` flag enables automatic code reloading during development, so you don't have to restart the server every time you make changes.

2. **Access the Frontend:**
   Open your web browser and go to `http://localhost:8000/`.  You should see the frontend, which will automatically redirect you to the API endpoint.

## API Endpoints

* **`/` (Root):** Serves the frontend HTML.  This is the main entry point for the application.
* **`/all_personalities`:**  Handles the API request.
   * **Method:** `GET`
   * **Query Parameter:** `question` (required).  The question to pass to the API.
   * **Example Request:**  `http://localhost:8000/all_personalities?question=What%20is%20your%20name`
   * **Response:** Returns a JSON object containing the personalities and combined response.

## Frontend Usage

1. **Enter a Question:** Type your question into the input field on the frontend.
2. **Click "Get Responses":**  This sends a GET request to the `/all_personalities` endpoint with your question.
3. **View the Results:** The API response (a JSON object) is displayed in the browser.

## Project Structure

```
personality_api/
├── main.py       # FastAPI application code
├── templates/index.html    # Frontend HTML file
├── venv/         # Virtual environment (not checked into version control)
└── README.md     # This file
```

## Contributing

1. **Fork the repository.**
2. **Create a new branch:** `git checkout -b feature/your-feature`
3. **Make your changes.**
4. **Commit your changes:** `git commit -m "Add your changes"`
5. **Push to your fork:** `git push`
6. **Create a pull request.**

