# etiketle

![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)
![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
  - [Running the Server](#running-the-server)
- [Usage](#usage)
  - [Admin Panel](#admin-panel)
  - [Annotating Posts](#annotating-posts)
- [Setting Up Users](#setting-up-users)
- [Testing](#testing)
- [Type Checking](#type-checking)
- [Documentation](#documentation)
- [Deployment](#deployment)
  - [Heroku](#heroku)
- [Contributing](#contributing)
- [License](#license)

## Introduction

**etiketle** is a robust annotation tool designed to facilitate the labeling of Reddit posts. It allows multiple users to annotate the same dataset concurrently, providing a seamless experience for collaborative labeling projects. Users can assign multiple labels to each post, add notes, and indicate their confidence levels in their annotations.

## Features

- **Multi-Choice Annotation:** Assign multiple labels to a single Reddit post.
- **Notes and Confidence Levels:** Add detailed notes and specify confidence levels for each annotation.
- **Collaborative Labeling:** Multiple users can annotate the same dataset, enhancing collaboration.
- **Dataset Management:** Upload Reddit datasets in CSV format and manage annotations efficiently.
- **User Roles:** Differentiate between normal users and superusers for varied access levels.
- **Export Functionality:** Export annotations in JSON format and posts in CSV format for external use.
- **Admin Interface:** Utilize Django's admin panel to manage teams, projects, and annotation configurations.
- **Type Checking and Testing:** Ensure code quality with `mypy`, `pytest`, and coverage reports.
- **Documentation:** Comprehensive documentation built with Sphinx for easy reference.

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL
- [Homebrew](https://brew.sh/) (for macOS users)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/aladagemre/etiketle.git
   cd etiketle
   ```

2. **Install PostgreSQL:**

   ```bash
   brew install postgresql
   ```

3. **Set Up Virtual Environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements/local.txt
   ```

### Database Setup

1. **Start PostgreSQL Service:**

   ```bash
   brew services start postgresql
   ```

2. **Create Database and User:**

   ```bash
   psql postgres
   ```

   Inside the PostgreSQL shell, run:

   ```sql
   CREATE DATABASE etiketle;
   CREATE USER etiketle WITH PASSWORD 'etiketle';
   ALTER ROLE etiketle SET client_encoding TO 'utf8';
   ALTER ROLE etiketle SET default_transaction_isolation TO 'read committed';
   ALTER ROLE etiketle SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE etiketle TO etiketle;
   ALTER USER etiketle CREATEDB;
   \q
   ```

3. **Apply Migrations:**

   ```bash
   python manage.py migrate
   ```

4. **Create Superuser:**

   ```bash
   python manage.py createsuperuser
   ```

### Running the Server

Start the development server with:

```bash
python manage.py runserver
```

Navigate to [http://localhost:8000/admin/](https://localhost:8000/admin/) to access the admin panel.

## Usage

### Admin Panel

1. **Login:**

   Access the admin panel at [http://localhost:8000/admin/](https://localhost:8000/admin/) and login with the superuser credentials you created.

2. **Setup:**

   - **Create a Team:** Define a new team to organize your projects.
   - **Create a Project:** Link the project to a team.
   - **Add Users:** Assign users to the project as needed.
   - **Configure Annotations:** Set up the annotation configurations and define annotation options.
   - **Upload Datasets:** Create a new dataset by uploading a CSV file containing Reddit posts.

### Annotating Posts

1. **Navigate to Posts:**

   Go to the dataset's detail page and click on "Display Posts" to view all Reddit posts in the dataset.

2. **Annotate:**

   Click on a post to open the annotation form. Assign labels, add notes, and specify your confidence level.

3. **Save Annotation:**

   Submit the form to save your annotation. You can navigate to the next or previous post using the provided buttons.

## Setting Up Users

- **Normal User Account:**

  - Go to the Sign Up page and fill out the registration form.
  - Verify your email address by copying the verification link from the console.
  - Your email will be verified, and the account will be ready for use.

- **Superuser Account:**

  - Use the command:

    ```bash
    python manage.py createsuperuser
    ```

  - For convenience, you can keep your normal user logged in on one browser and your superuser on another to observe different user views.

## Testing

### Running Tests

Execute the test suite with:

```bash
pytest
```

### Type Checking

Ensure type consistency using `mypy`:

```bash
mypy
```


### Test Coverage

Generate a test coverage report:

```bash
coverage run -m pytest
coverage html
open htmlcov/index.html
```


## Documentation

Documentation is built with Sphinx. To build and serve the docs locally, navigate to the `docs` directory and run:

```bash
make html
```

Open `_build/html/index.html` in your browser to view the documentation.



For more details, refer to the [Documentation](docs/howto.rst).

## Deployment

### Heroku

Follow the [Cookiecutter Django Heroku documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html) for deploying this application to Heroku.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature/YourFeature
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add some feature"
   ```

4. Push to the branch:

   ```bash
   git push origin feature/YourFeature
   ```

5. Open a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).
