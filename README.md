### This is a prototype command line model for our software engineering project.

### Make sure you have the mysql local server before running the project
### Commands given here are for linux os but the procedure is same for other OS.
## Make the virtual environment: 
```
virtualenv environment
```
## Activate the environment:
```
source environment/bin/activate
```
## Install dependencies:
```
pip install -r req.txt
```
## go to code directory: 
```
cd code
```
## To create sample database run database.py:
```
python3 database.py
```
## run any one of the three files to interact with the system:
> run admin.py: (for school administration)
```
python3 admin.py
```
> run teacher.py: (for teachers)
```
python3 teacher.py
```
> run student.py: (for students)
```
python3 student.py
```
