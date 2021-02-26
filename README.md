# Database API
A Python API for interacting with a database using SQL.

The Python code imports sqlite and allows the user to interact with the database via the command line. When the code is run, the user will be prompted with 8 options:
1. Create a database for storing employee data for the University of Bath; this will create a UoBDB.db if it does not already exist.
2. Allows the user to insert new data. Code checks that employee ID is unique, that the salary is an integer and that the email contains "@bath.ac.uk".
3. Displays all data in the database.
4. Searches for an entry using the employee ID.
5. Updates a user-specified attribute for a given employee ID.
6. Deletes an entire entry corresponding to a given employee ID.
7. Deletes the database
8. Exits by stopping the code from running.
