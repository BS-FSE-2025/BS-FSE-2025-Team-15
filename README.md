# RealPharmaPrices

## Overview

RealPharmaPrices is a web-based system designed to help patients find affordable medications close to their homes. By enabling price comparison and displaying pharmacy proximity, RealPharmaPrices empowers users to make informed decisions, ensuring accessibility and cost savings for essential medications. The platform supports three key roles: Guests, Pharmacy Managers, and Admins, each contributing to a seamless and efficient user experience.

## Problem Statement

Patients often face challenges in finding medications at fair prices and convenient locations. The lack of accessible, centralized information about drug prices and availability makes it difficult to compare options, leading to unnecessary expenses or inaccessible medications. RealPharmaPrices addresses this problem by offering a platform that not only provides pricing information but also considers pharmacy proximity, improving convenience and affordability.

## Key Features

### 1. Guest

- Search for medicines based on fair pricing, availability, and proximity.
- Compare options to find the most affordable and nearby pharmacies.

### 2. Pharmacy Manager

- Display medicine prices, stock availability, and location details.
- Reach more patients by providing accurate and up-to-date information.

### 3. Admin (ADMIN)

- Manage the system's infrastructure and supervise pharmacy activities.
- Update medication prices based on Ministry of Health regulations.
- Ensure the system remains accurate, reliable, and compliant with regulations.

## Development Environment and Tools

### Web Work Environment:

- **Backend:** Python-Django

  - Django is a secure and flexible framework based on Python, offering powerful capabilities for efficient backend development.

- **Database:** SQLite

  - SQLite is a lightweight, fast, and flexible database, suitable for small to medium-sized systems. For larger projects, server-based databases like PostgreSQL or MySQL may be considered.

- **Frontend:** HTML and CSS

  - HTML is used to structure the web pages, while CSS is employed to style and enhance the visual appeal and user experience of the platform.

## Installation Guide

### Pre-Install Required Packages

1. Install Django:
   ```bash
   pip install django
   ```

### Steps

If you download the system for the first time:

1. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

2. Apply migrations:

   ```bash
   python manage.py migrate
   ```

3. Run the server:

   ```bash
   python manage.py runserver
   ```

### In Case of Issues with Migrations

If you face migration issues (e.g., due to installing the system more than once or working with a non-clean database), follow these steps:

1. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

2. Reset migrations for specific apps (example shown for `members` and `app`):

   ```bash
   python manage.py migrate members zero --fake
   python manage.py migrate app zero --fake
   ```

3. Reapply migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the server:

   ```bash
   python manage.py runserver
   ```

## General Guidelines and Notes

- Ensure that all dependencies are installed as per the `requirements.txt` file.
- If changes occur in requirements or configurations, update the documentation accordingly.
- Keep the database connection settings updated, especially if switching from SQLite to a server-based database like PostgreSQL or MySQL.
- Regularly check for updates to the Django framework and other dependencies to maintain security and stability.

## Contributing

We welcome contributions to improve RealPharmaPrices. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes and push to your fork.
4. Create a pull request with a detailed description of your changes.



## Contact

Thank you for using RealPharmaPrices. Together, we can make medications more affordable and accessible!

