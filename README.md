# Multi-Restaurant Management API

A Django REST Framework (DRF) project for managing multiple restaurants and their menus.
This API supports **user registration, JWT authentication, restaurant and menu management**, and **role-based access control**.

---

## Features

- User registration with profile details
- JWT-based authentication (login and refresh tokens)
- Users can create and manage multiple restaurants
- Users can create, update, and delete menus for their restaurants
- Admins can update user roles
- API documentation using **DRF Spectacular (Swagger/OpenAPI)**
- Profiling and optimization using **Django Silk**

---

## Technologies

- Python 3.x
- Django 4.x
- Django REST Framework
- Django REST Framework Simple JWT
- DRF Spectacular
- `uv` for dependency management
- Django Silk for profiling
- SQLite (default) / PostgreSQL (optional)

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/multi-restaurant-api.git
cd multi-restaurant-api
```

2. **Install `uv` (if not installed)**

```bash
pip install uv
```

3. **Install dependencies from `pyproject.toml`**

```bash
uv install
```

- This will read `pyproject.toml` and install all required packages.
- `uv.lock` ensures the exact versions are installed.

4. **Run migrations**

```bash
uv run manage.py migrate
```

5. **Create a superuser (optional for admin)**

```bash
uv run manage.py createsuperuser
```

6. **Run the development server**

```bash
uv run manage.py runserver
```

> You can now access the API locally at `http://127.0.0.1:8000/`

---

## Adding or Updating Dependencies

- To **add a new package**:

```bash
uv add <package-name>
uv install
```

- To **remove a package**:

```bash
uv remove <package-name>
uv install
```

- To **update packages**:

```bash
uv update
uv install
```

> `uv.lock` will be updated automatically to lock the versions.

---

## Authentication

- Uses **JWT tokens** via `djangorestframework-simplejwt`
- Include token in request headers for protected endpoints:

```http
Authorization: Bearer <access_token>
```

---

## Permissions

- **Authenticated users** can create and manage their own restaurants and menus
- **Admin users** can update roles of other users
- Users cannot modify restaurants or menus belonging to other users

---

## API Documentation

- **Swagger UI**:

```
http://127.0.0.1:8000/schema/swagger-ui/
```

- **Redoc**:

```
http://127.0.0.1:8000/
```

> You can restrict documentation access to admins or disable it in production.

---

## Profiling & Optimization with Django Silk

**Django Silk** allows you to profile requests, SQL queries, and view performance metrics to optimize your API.

- Visit:

```
http://127.0.0.1:8000/silk/
```

> The Silk dashboard lets you view request profiling, SQL queries, and performance metrics in real-time.

---

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/YourFeature`
3. Make your changes
4. Commit your changes: `git commit -m "Add feature"`
5. Push to the branch: `git push origin feature/YourFeature`
6. Open a Pull Request

---

## License

This project is licensed under the MIT License.
