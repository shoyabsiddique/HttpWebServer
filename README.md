# Simple HTTP Server with Basic Authentication and Data Analysis

This is a Python script for a simple HTTP server that provides basic authentication, serves HTML templates, handles form submissions, and performs data analysis. The server allows users to authenticate using basic authentication and access different endpoints to view HTML pages, submit form data, and receive analyzed results.

## Features:

- **Basic Authentication**: Users are required to authenticate using their student ID as both username and password.
- **Static File Serving**: The server serves static HTML files located in the `templates` directory.
- **Form Submission**: Supports form submission with `POST` requests.
- **Data Analysis**: Analyzes user-submitted data to generate a psychological profile.
- **Third-Party API Integration**: Fetches movie recommendations and images of pets from third-party APIs.

## Requirements:

- Python 3.x
- Requests library (install via `pip install requests`)

## Usage:

1. Clone the repository or download the Python script.
2. Ensure Python 3.x is installed on your system.
3. Install the Requests library using `pip install requests`.
4. Customize the script as needed (e.g., change `STUDENT_ID`).
5. Run the script using `python <filename>.py`.
6. Access the server at `http://localhost:8080` in a web browser.

## Endpoints:

- `/`: Home page with basic authentication.
- `/form`: Form submission page for users to input their data.
- `/login`: Endpoint for authenticating users with their student ID.
- `/analysis`: Endpoint for submitting form data and generating a psychological profile.
- `/view/input`: View submitted input data in JSON format.
- `/view/profile`: View generated psychological profile in JSON format.

## Credits:

- This script utilizes third-party APIs for fetching movie recommendations and pet images.
- Third-party APIs used:
  - Dog CEO API for dog images: [https://dog.ceo/dog-api/](https://dog.ceo/dog-api/)
  - TheCatAPI for cat images: [https://thecatapi.com/](https://thecatapi.com/)
  - Random Duck for duck images: [https://random-d.uk/](https://random-d.uk/)
