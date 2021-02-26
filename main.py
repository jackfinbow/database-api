# https://repl.it/@JackFinbow/Databaseslab3#main.py

import sqlite3

attributes = ['empID', 'empTitle', 'forename', 'surname', 'email', 'salary']

# Define DBOperation class to manage all data into the database. 
# Give a name of your choice to the database

class DBOperations:
  # SQL commands

  sql_create_table_firsttime = "create table if not exists "

  # creates table EmployeeUoB with required fields and empID as primary key
  sql_create_table = "CREATE TABLE EmployeeUoB (empID INTEGER NOT NULL, empTitle VARCHAR(5), forename VARCHAR(20) NOT NULL, surname VARCHAR(20) NOT NULL, email VARCHAR(30), salary INTEGER, PRIMARY KEY (empID))"

  # inserts row of data into table
  sql_insert = "INSERT INTO EmployeeUoB (empID, empTitle, forename, surname, email, salary) VALUES {}"
  sql_select_all = "SELECT * FROM EmployeeUoB"
  sql_search = "SELECT * FROM EmployeeUoB WHERE empID = {}"
  
  # update a specified attribute value when given an employee ID
  sql_update_data = "UPDATE EmployeeUoB SET {} = '{}' WHERE empID = {}"

  # deletes row of data for given employee ID
  sql_delete_data = "DELETE FROM EmployeeUoB WHERE empID = {}"

  # drops the table EmployeeUoB. sql_create_table will have to be run if the table needs to be re-created
  sql_drop_table = "DROP TABLE EmployeeUoB"

  # function to connect to the database UoBDB.db
  def get_connection(self):
    self.conn = sqlite3.connect("UoBDB.db")
    self.cur = self.conn.cursor()

  # function asks for user to input employee ID
  # it checks the input is a valid ID and then returns all data for that employee ID
  def get_empID(self):
    employeeID = int(input("Enter Employee ID: "))
    self.cur.execute(self.sql_search.format(employeeID))
    result = self.cur.fetchone()

    # while and if statements check if that empID exists and will re-prompt user for input if it's invalid
    empIDExists = False
    while empIDExists == False:
      if type(result) != type(tuple()):
        print("No record")
        employeeID = int(input("Enter Employee ID: "))
        self.cur.execute(self.sql_search.format(employeeID))
        result = self.cur.fetchone()
      else:
        empIDExists = True
    
    return employeeID, result

  # function gets user input for atttribute and updated value
  def update_attribute(self):
    # obtain user input for attribute name to be updated
    # e.g. salary
    attribute = input("Enter attribute to be updated: ")
    global attributes

    # checks that attribute supplied exists in the table
    isAttribute = False
    while isAttribute == False:
      if attribute not in attributes:
        print("This attribute is not in table EmployeeUoB")
        attribute = input("Enter attribute to be updated: ")
      else:
        isAttribute = True
      
    # if attribute is empID or salary, checks that input is integer
    if (attribute == "empID" or attribute == "salary"):
      isInt = False
      while isInt == False:
        try:
          # obtain user input for new value
          updated_data = int(input("Enter updated data: "))
          isInt = True
        except:
          print("The entered value is not as integer")
    else:
      updated_data = input("Enter updated data: ")

    # if attribute is email, checks that it's a valid UoB email
    if attribute == "email":
      isBathEmail = False
      while isBathEmail == False:
          if "@bath.ac.uk" not in updated_data:
            print("This is not a UoB email address")
            updated_data = input("Enter updated data: ")
          else:
            isBathEmail = True

    return attribute, updated_data

  # function run when 1 selected from menu
  # creates table EmployeeUoB and prints message upon success
  # prints an error message if the table already exists
  def create_table(self):
    try:
      self.get_connection()
      # creates table
      self.cur.execute(self.sql_create_table)
      # saves changes
      self.conn.commit()
      print("Table EmployeeUoB created successfully")
    except:
      print("This table is already created")
      #print(e)
    finally:
      self.conn.close()

  # function run when 2 selected from menu
  # takes user input for values of each attribute
  def insert_data(self):
    try:
      self.get_connection()

      # creates instance of class Employee
      emp = Employee()
      emp.set_employee_id(int(input("Enter Employee ID: ")))
      emp.set_employee_title(input("Enter Employee Title: "))
      emp.set_forename(input("Enter Employee Forename: "))
      emp.set_surname(input("Enter Employee Surname: "))
      emp.set_email(input("Enter Employee Email: "))
      # error message if email is not a UoB email address
      # reprompts user for email input
      isBathEmail = False
      while isBathEmail == False:
        if "@bath.ac.uk" not in emp.email:
          print("This is not a UoB email address")
          emp.set_email(input("Enter Employee Email: "))
        else:
          isBathEmail = True
      emp.set_salary(int(input("Enter Employee Salary: ")))

      # inserts data into table
      self.cur.execute(self.sql_insert.format(tuple(emp.__str__().split("\n"))))
      self.conn.commit()
      print("Inserted data successfully")

    # prints error message
    # triggered if empID is not unique or if that or salary are not integers
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # function run when 3 selected from menu
  def select_all(self):
    try:
      self.get_connection()
      # selects all data from table
      self.cur.execute(self.sql_select_all)
      results = self.cur.fetchall()
      
      # combine attribute headings and data into single list
      attributes = [('empID', 'empTitle', 'forename', 'surname', 'email', 'salary')]
      results2 = attributes + results

      # display all rows of data in formatted columns
      # https://stackoverflow.com/questions/9989334/create-nice-column-output-in-python
      for row in results2:
        print("{: >5}{: >10}{: >11}{: >10}{: >23}{: >7}".format(*row))

    except Exception as e:
      print(e)
    finally:
      self.conn.close()
    
  # function run when 4 selected from menu
  # returns employee data for given employee ID
  def search_data(self):
    try:
      self.get_connection()

      employeeID, result = self.get_empID()

      # prints out employee information for given empID
      for index, detail in enumerate(result):
        if index == 0:
          print("Employee ID: " + str(detail))
        elif index == 1:
          print("Employee Title: " + detail)
        elif index == 2:
          print("Employee Name: " + detail)
        elif index == 3:
          print("Employee Surname: " + detail)
        elif index == 4:
          print("Employee Email: " + detail)
        else:
          print("Salary: "+ str(detail))
            
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # function run when 5 selected from menu
  # updates a specific attribute selected by user
  def update_data(self):
    try:
      self.get_connection()
      
      employeeID, result = self.get_empID()

      attribute, updated_data = self.update_attribute()

      # updates table and prints confirmation, in addition to number or rows updated
      # https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor
      numRows = self.cur.execute(self.sql_update_data.format(attribute, updated_data, employeeID)).rowcount
      self.conn.commit()
      print("Inserted data successfully")
      print (str(numRows)+ "Row(s) updated.")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

# function run when 6 selected from menu
# deletes row of data from the table for given empID
  def delete_data(self):
    try:
      self.get_connection()
      
      employeeID, result = self.get_empID()

      # deletes row of data corresponding to supplied empID and number of rows deleted
      print(self.sql_delete_data.format(employeeID))
      numRows = self.cur.execute(self.sql_delete_data.format(employeeID)).rowcount
      self.conn.commit()
      print (str(numRows)+ "Row(s) deleted.")

    except Exception as e:
      print(e)
    finally: 
      self.conn.close()

  # function run when 7 selected from menu
  # drops (deletes) whole table EmployeeUoB
  def drop_table(self):
    self.get_connection()
    # asks for user confirmation before dropping table
    confirm = input("Are you sure you want to drop table EmployeeUoB? y/n ")
    if confirm == "y":
      self.cur.execute(self.sql_drop_table)
      print("EmployeeUoB table successfully deleted")
    else:
      return

    
class Employee:
  def __init__(self):
    self.employeeID = 0
    self.empTitle = ''
    self.forename = ''
    self.surname = ''
    self.email = ''
    self.salary = 0.0

  def set_employee_id(self, employeeID):
    self.employeeID = employeeID

  def set_employee_title(self, empTitle):
    self.empTitle = empTitle

  def set_forename(self,forename):
   self.forename = forename
  
  def set_surname(self,surname):
    self.surname = surname

  def set_email(self,email):
    self.email = email
  
  def set_salary(self,salary):
    self.salary = salary

  def __str__(self):
    return str(self.employeeID)+"\n"+self.empTitle+"\n"+ self.forename+"\n"+self.surname+"\n"+self.email+"\n"+str(self.salary)

# The main function will parse arguments. 
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.
  
while True:
  print ("\n Menu:")
  print ("**********")
  print (" 1. Create table EmployeeUoB")
  print (" 2. Insert data into EmployeeUoB")
  print (" 3. Select all data into EmployeeUoB")
  print (" 4. Search an employee")
  print (" 5. Update data some records")
  print (" 6. Delete data some records")
  print (" 7. Drop table EmployeeUoB")
  print (" 8. Exit\n")

  __choose_menu = int(input("Enter your choice: "))
  db_ops = DBOperations()
  if __choose_menu == 1:
    db_ops.create_table()
  elif __choose_menu == 2:
    db_ops.insert_data()
  elif __choose_menu == 3:
    db_ops.select_all()
  elif __choose_menu == 4:
    db_ops.search_data()
  elif __choose_menu == 5:
    db_ops.update_data()
  elif __choose_menu == 6:
    db_ops.delete_data()
  elif __choose_menu == 7:
    db_ops.drop_table()
  elif __choose_menu == 8:
    exit(0)
  else:
    print ("Invalid Choice")