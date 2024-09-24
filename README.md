# SUN Lab Access System

## Project Overview
The SUN Lab Access System is a desktop application that tracks access to the Student Unix Network (SUN) Lab. Every time a student swipes their card, their student ID and the timestamp are recorded in the database. The system provides an admin interface for managing users, viewing access logs, and searching logs by filters.

## How to Run
To run this project, follow the steps below:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/sun_lab_access_system.git
   cd sun_lab_access_system

2. **Set Up the Database: Run the database setup script to initialize the SQLite database**:
   ```bash
   Copy code
   python3 db_setup.py

3. **Run the Admin Interface: Launch the admin panel to manage users and view logs**:
   ```bash
   Copy code
   python3 admin_gui.py

## Video Demo
Watch the [video demo here](https://drive.google.com/file/d/1kSvmlgab_1EYOZODGHkHTAmitF8GqUf4/view?usp=sharing).

# Features

## View Access Logs
Display all access logs, showing student IDs and timestamps.
## Search Logs by Filters
Filter access logs by student ID and/or date range.
## User Management
   ``bash
   Activate: Add a new user or activate a suspended user.
   ``bash
   Suspend: Suspend an active or reactivated user.
   ``bash
   Reactivate: Reactivate a suspended user.
## View User Details
View detailed user information, including their status (active, suspended, or reactivated) and last access time.
## Dashboard Summary
View a summary of the system, showing the total number of active, suspended, and reactivated users, as well as total access logs.
# Bonus Features

## View User Details with Last Access
This feature allows the admin to view user details, including their last recorded access time.
## System Activity Dashboard
The dashboard shows a quick summary of the system activity, displaying the number of users in each status (active, suspended, reactivated) and the total number of access logs.

