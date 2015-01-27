
About
----------------

This is a simple test suite for Table of comments. 
It emulates the standard unit test functionality of 
test class, methods and assertions.


Setup
----------------

The test suite is configured within __init__.py regarding 
which test classes to run.

Each new test class needs to be imported into __init__, 
listed within the reload_modules() function and listed within 
the run() function as a test.

Within each test class, every function starting with "test_" 
is run as a test

To run this test suite open the command palette (Ctrl + Shift + P) 
to execute the command "Table of comments: Run Tests"


Results
----------------
Each class and method is listed with a "." for the number of passed 
test assertions made and a "F" for failed assertions.