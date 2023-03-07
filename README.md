# Corporate-Asset-Tracker
The Corporate Asset Tracker is a Django web application designed to track the assignment and return of corporate assets, such as phones, tablets, and laptops, to employees. The application is designed to be used by multiple companies, and each company can delegate devices to its employees for a specific period of time. The application also allows companies to track when a device was checked out and returned and to log the condition of each device at the time of check-in.
# Installations
1. Clone the repository:

   ```
   git clone https://github.com/Armaaan/Corporate-Asset-Tracker.git
   ```

2. Install the required packages:

   ```
   cd Corporate-Asset-Tracker 

   pip install -r requirements.txt
   ```

3. Create the database tables:

   ```
   python manage.py migrate
   ```


# Usage
1. Run the server:
   ```
   python manage.py runserver
   ```
2. Navigate to the application in your web browser at 
   ```
   http://localhost:8000/
   ```
3. Use the application to track corporate assets, including assigning devices to employees and logging their condition upon check-in and check-out.

# Testing
Run the automated tests by running the following command:
   ```
   python manage.py test
   ```

# Code Coverage Report
Run the following command:
   ```
   coverage report
   ```

# API Documentation
The Corporate Asset Tracker includes an API that allows you to programmatically interact with the application. You can access the API documentation at http://localhost:8000/swagger/

# Contributing
Contributions to the Corporate Asset Tracker are welcome. If you have a bug fix or feature request, please open an issue on GitHub. If you would like to contribute code, please fork the repository and submit a pull request.