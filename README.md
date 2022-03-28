# djambikProject
Django Hackathon

Whenever you are starting a new web development project, it’s a good idea to first set up your development environment. Create a new directory for your project to live in, and cd into it:

$ mkdir djumbikProject
$ cd djumbikProject

Once your inside the main directory, it’s a good idea to create a virtual environment to manage dependencies. There are many different ways to set up virtual environments, but here you’re going to use venv:

$ python3 -m venv venv

This command will create a folder venv in your working directory. Inside this directory, you’ll find several files including a copy of the Python standard library. Later, when you install new dependencies, they will also be stored in this directory. Next, you need to activate the virtual environment by running the following command:

$ source venv/bin/activate

Now that you’ve created a virtual environment, it’s time to install Django. You can do this using pip:

(venv) $ pip install Django

Create a Django Project
As you saw in the previous section, a Django web application is made up of a project and its constituent apps. Making sure you’re in the rp_portfolio directory, and you’ve activated your virtual environment, run the following command to create the project:

$ django-admin startproject djumbikProject

Once your file structure is set up, you can now start the server and check that your set up was successful. In the console, run the following command:

$ python manage.py runserver

Then, in your browser go to localhost:8000, and you should see the following:
![image](https://user-images.githubusercontent.com/88595595/160432396-8d450dd4-96f7-4913-a31e-6ec3a759b798.png)
