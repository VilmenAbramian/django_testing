
# Django Testing  

This repository contains two Django projects: **YaNews** and **YaNote**, which represent services for publishing news and notes. By structure and functionality, they are similar to another one of my projects — **Blogicum**.  
In this case, the projects in this repository served as precoded applications for which test suites had to be written.  
- For **YaNews** — using the `pytest` library.  
- For **YaNote** — using the built-in `unittest` framework.  

---

## ⚙️ How to run tests

1. Create and activate a virtual environment; install dependencies from `requirements.txt`.  
2. Run the script `run_tests.sh` from the project’s root directory:

```sh
bash run_tests.sh
```

## 📂 Repository structure

```
 django_testing
     ├── ya_news
     │   ├── news
     │   │   ├── fixtures/
     │   │   ├── migrations/
     │   │   ├── pytest_tests/
     |   │   │   ├── __init__.py
     |   │   │   ├── conftest.py <- Fixtures module
     |   │   │   ├── consts.py <- Module with precomputed addresses and users
     |   │   │   ├── test_content.py <- Tests for page content
     |   │   │   ├── test_logic.py <- Tests for business logic
     |   │   │   └── test_routes.py <- Tests for site routes
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanews/
     │   ├── manage.py
     │   └── pytest.ini
     ├── ya_note
     │   ├── notes
     │   │   ├── migrations/
     │   │   ├── tests/
     |   │   │   ├── __init__.py
     |   │   │   ├── conf.py <- Fixtures module
     |   │   │   ├── consts.py <- Module with precomputed addresses and users
     |   │   │   ├── test_content.py <- Tests for page content
     |   │   │   ├── test_logic.py <- Tests for business logic
     |   │   │   └── test_routes.py <- Tests for site routes
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanote/
     │   ├── manage.py
     │   └── pytest.ini
     ├── .gitignore
     ├── README.md
     ├── requirements.txt
     └── structure_test.py
```

## 🧪 Test suite for YaNews (Pytest)
 
The Pytest test package includes the following modules:
-   **conftest.py** — contains fixtures for creating various users and objects (such as a set of news entries, a single news entry, a set of comments, a single comment), as well as fixtures for computing addresses to different site pages.
-   **consts.py** — collects fixtures required for parametrization into classes with sets of constants. To allow fixtures to be passed as test parameters, the lazy_fixture library is used.
-   **test_content.py** contains tests such as:
    -   No more than 10 news items on the main page.
    -   News are sorted from newest to oldest.
    -   Comments on a news detail page are sorted chronologically: older first, newer last.
    -   Anonymous users cannot see the comment submission form, while authenticated users can.
-   **test_logic.py** contains tests such as:
    -   Anonymous users cannot submit comments.
    -   Authenticated users can submit comments.
    -   Comments containing forbidden words are not published, and the form returns an error.
    -   Authenticated users can edit or delete their own comments.
    -   Authenticated users cannot edit or delete others’ comments.
-   **test_routes.py** contains tests such as:
    -   The main page is available to anonymous users.
    -   The news detail page is available to anonymous users.
    -   Comment edit and delete pages are available to the comment’s author.
    -   Anonymous users trying to access edit/delete pages are redirected to the login page.
    -   Authenticated users cannot access edit/delete pages for comments they do not own (404 error is returned).
    -   Registration, login, and logout pages are available to anonymous users.

## 🧪 Test suite for YaNote (Unittest)
The Unittest test package includes the following modules:
-   **conf.py** — contains a parent class with fixtures for creating various users and a note, as well as fixtures for computing addresses to different site pages.
-   **test_content.py** contains tests such as:
    -   A note is passed to the notes list page in the object_list of the context dictionary.
    -   Notes belonging to one user do not appear in another user’s notes list.
    -   The note creation and edit pages are passed forms.
-   **test_logic.py** contains tests such as:
    -   A logged-in user can create a note, while an anonymous user cannot.
    -   Two notes with the same slug cannot be created.
    -   If no slug is specified during creation, it is automatically generated using pytils.translit.slugify.
    -   A user can edit or delete their own notes but cannot edit or delete others’ notes.
-   **test_routes.py** contains tests such as:
    -   The main page is available to anonymous users.
    -   The news detail page is available to anonymous users.
    -   Comment edit and delete pages are available to the comment’s author.
    -   Anonymous users trying to access edit/delete pages are redirected to the login page.
    -   Authenticated users cannot access edit/delete pages for comments they do not own (404 error is returned).
    -   Registration, login, and logout pages are available to anonymous users.

## 📚 Context
This project was created as part of **Sprint 9** of the _Python Developer+_ course.

## 👤 Author
**Vilmen Abramian**
📧 vilmen.abramian@gmail.com
