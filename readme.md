# HR Interview Question Generator

This Django-based HR Interview Question Generator allows HR managers and interviewers to easily generate skill-based interview questions for candidates based on their resume. The system supports resume uploads, extracts skills, and provides questions tailored to the candidate's expertise level in selected skills.

## Features

- **User Authentication**: Supports login and logout functionality.
- **Resume Upload**: Accepts PDF resumes and extracts primary and secondary skills using LangChain.
- **Skill Display**: Lists top 5 primary and secondary skills for the candidate to select expertise levels.
- **Dynamic Question Generation**: Generates interview questions based on chosen skill and expertise level, including coding challenges.
- **RESTful API Endpoints**: Uses Django REST Framework to manage question generation.

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: PostgreSQL (with PGVector for vector storage)
- **Other Tools**: LangChain for skill extraction and question generation

## Getting Started

### Prerequisites

- **Python 3.8+**
- **Docker** (recommended for PostgreSQL setup with PGVector extension)
- **Node.js** (optional, for additional frontend setup if needed)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/hr-interview-question-generator.git
   cd hr-interview-question-generator
   ```

2. **Create a Virtual Environment**:
``` bash
    Copy code
    python3 -m venv venv
    source venv/bin/activate
```
3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure PostgreSQL**:
- Set up a PostgreSQL database with PGVector for vector storage.
- Update the DATABASES settings in settings.py with your PostgreSQL credentials.
5. **Run Migrations:**:
```bash
python manage.py migrate
```
6. **Start the Development Server:**:
```bash
python manage.py runserver
```
The app will be available at http://127.0.0.1:8000/.

## Usage
1. **Login**: Go to /login to access the main features of the application.
2. **Upload Resume**: Navigate to the "Upload" page, select a PDF resume, and upload it. The app will process the resume to extract skills and experience.
3. **Select Skills and Expertise Level**: After uploading, the system will display a list of primary and secondary skills. Select the expertise level (Beginner, Medium, or Expert) for each skill.
4. **Generate Questions**: Click "Get Questions" to generate skill-based interview questions, including coding challenges.
5. **Review Questions**: The questions will display on the same page in an organized table.

## API Endpoints
- **Resume Upload**: /upload_resume/ (POST) - Upload a PDF resume to extract skills.
- **Get Questions**: /get_questions/ (POST) - Fetch interview questions based on selected skill and expertise level.

## Folder Structure
```bash
hr-interview-question-generator/
├── candidates/                 # Main app for candidates
│   ├── templates/
│   │   ├── upload.html          # Template for uploading resume
│   │   ├── display_skills.html  # Template for displaying skills
│   │   └── questions.html       # Template for displaying questions
│   ├── views.py                 # Contains views for upload and question generation
│   └── urls.py                  # URL routing for the candidates app
├── manage.py                    # Django project management
└── requirements.txt             # Project dependencies
```

## Customization
- **Modify Question Generation Prompt**: In views.py, customize the LangChain prompt to adjust the style or depth of generated questions.
- **Front-End Customization**: Customize templates in templates/candidates for styling changes or layout adjustments.
- **Add More Skills**: Extend the skill extraction functionality to support additional skills.

# Contributing
Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.

## Happy coding! Let’s simplify the interview process with better question generation.

