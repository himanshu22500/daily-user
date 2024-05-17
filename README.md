# Daily User Backend

This is a Django-based backend project for managing daily users. The project is structured around a single app, `user_core`, which handles the core functionality.

## Installation

1. **Clone the repository**: Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/himanshu22500/daily-user
```

2. **Navigate to the project directory**: Change your current directory to the project directory.

```bash
cd daily-user
```

3. **Create a virtual environment**: Before installing the project dependencies, it's a good practice to create a virtual environment. This isolates your project and avoids conflicts with other projects. You can create a virtual environment using the following command:

```bash
python3 -m venv venv
```

4. **Activate the virtual environment**: You can activate the virtual environment using the following command:

```bash
source venv/bin/activate
```

5**Install the requirements**: This project uses pip for package management. You can install all the required packages using the following command:

```bash
pip install -r requirements.txt
```

6**Run migrations**: Django uses migrations to propagate changes made to models (adding a field, deleting a model, etc.) into the database schema. Run the following command to apply migrations:

```bash
python manage.py migrate
```

7**Create a superuser**: To access the admin panel, you need to create a superuser. Run the following command and enter the required details:

```bash
python manage.py createsuperuser
```

8**Run the server**: Finally, you can run the Django development server using the following command:

```bash
python manage.py runserver
```

Now, you can access the project at `http://127.0.0.1:8000/` and the admin panel at `http://127.0.0.1:8000/admin`.
`
