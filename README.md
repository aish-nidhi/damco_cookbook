Steps to run the project:-
1. git clone <git-url>
2. Enter the cloned repository
3. create a virtual environment for running the project using virtualenv .venv
4. In case of error, please install virtualenv package of python using pip install virtualenv
5. After the virtual environment is created, activate it using virtualenv <env-name>
6. Run command pip install -r requirements.txt
7. Migrate the tables by running the command python manage.py migrate
8. Run the following command with excel filepath and and email recipient parameter to import recipes to database :-
    python manage.py migrate_excel_data -f <filepath> -- email <recipient-mail>