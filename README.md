* Create a new python virtual environment
* Install Bower, Grunt

````
npm install -g grunt-cli bower
````
* Install npm packages

````
npm install
````
* Run command ````make all```` and it will create a superuser with password "test123".
* Start a local server with command:

````
DJANGO_SETTINGS_MODULE='expense_track.settings_dev' python manage.py runserver_plus --insecure
````
