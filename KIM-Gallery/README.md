# KIM Gallery

A Flask-based image gallery website that allows users to upload, browse, and manage images with features like tagging, search, and user profiles.

## Features

- User authentication (register, login, logout)
- Image upload and management
- Gallery view with grid layout
- Image details page with tags
- User profiles
- Search functionality
- Image categories/tags
- Responsive design

## Tech Stack

- Python 3.9+
- Flask web framework
- SQLAlchemy with SQLite
- Poetry for dependency management
- Bootstrap 5 for UI
- Modern CSS with transitions and animations

## Setup

1. Make sure you have Python 3.9 or higher installed
2. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Clone the repository:
   ```bash
   git clone <repository-url>
   cd KIM-Gallery
   ```

4. Install dependencies:
   ```bash
   poetry install
   ```

5. Create the database:
   ```bash
   poetry run flask db upgrade
   ```

6. Run the application:
   ```bash
   poetry run python run.py
   ```

The application will be available at `http://localhost:5000`

## Project Structure

```
KIM-Gallery/
├── kim_gallery/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── gallery/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── main/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── uploads/
│   ├── templates/
│   │   ├── auth/
│   │   ├── gallery/
│   │   ├── main/
│   │   └── base.html
│   └── models.py
├── migrations/
├── pyproject.toml
├── README.md
└── run.py
```

## Development

- The application uses Flask's blueprint structure for modularity
- SQLAlchemy models are defined in `models.py`
- Forms are created using Flask-WTF
- Templates use Jinja2 templating engine
- Static files are served from the `static` directory
- Uploaded images are stored in `static/uploads`

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
