# PROJECT PAL
# Overview
This application is designed to give users with busy schedules a way to quickly create and keep track of projects of any type and purpose allowing each project to add or remove tasks updating their progress through completion.

# Process Flow
- [ERD](https://dbdiagram.io/d/BE-Capstone-Project-Pal-65cab919ac844320aeff164e)

- [Wireframes](https://www.figma.com/file/DdCdckqyu95M7JiTiPJ0NO/BE-Capstone-%22Project-Pal%22?type=whiteboard&node-id=0-1&t=eZL4pGmqNtpXSUJh-0)

- [Project Board](https://github.com/users/DavidBPoole/projects/4/views/1)

# Target User of this application is:
- someone who needs an organized way to keep track of personal projects
- someone who needs a clean and streamlined to-do list
- someone who wants a quick and simple project management interface
- someone who may want to collaborate with other users on their projects and tasks

# Features
- Authenticated registration/sign-in
- User home page with project listings
- Project details with task view page
- CRUD on projects and tasks
- Category assignment of tasks
- Ability to CRUD endless projects authenticated and unique to the user
- Future feature to collaborate with other authenticated users on your projects
- Ability to collaborate with other authenticated users on your projects

# Relevant Links
[Project Pal - Client](https://github.com/DavidBPoole/projectpal-client)

# Contributors
[David Poole](https://github.com/DavidBPoole)

# Tech Stack
Python
Django
Figma

# Setup Instructions

1. Set up a [Firebase](https://firebase.google.com/) project w/ authentication only.
    - [Firebase Setup w/ Authentication instructional video](https://www.loom.com/share/163ffe1539bb482196efa713ed6231e9)

2. Clone Project Pal (projectpal-server) to your local drive and change to that directory:
    - `git@github.com:DavidBPoole/projectpal-server.git`
    - `cd projectpal-client`

3. From the root direction, in your command line run the following:
```markdown
    pipenv install django=='4.1.3' autopep8=='2.0.0' pylint=='2.15.5' djangorestframework=='3.14.0' django-cors-headers=='3.13.0' pylint-django=='2.5.3'
```
4. Select the Python Interpreter within your editor. Press the following commands to open the Command Palette, and select "Python: Select Interpreter:
    - ⌘SHIFTP (Mac)
    - CtrlSHIFTP (Windows)
    - You will be looking for the following format beginning with your project's name followed by a random string:
    <YOUR_FOLDER_NAME>-<RANDOM_STRING>

5. Pylin Settings for Django
  There should now be a .vscode folder in your directory. If there is not one, create it. Create/open the settings.json file and add the following lines:
  ```markdown
      {
          "python.linting.pylintArgs": [
              "--load-plugins=pylint_django",
              "--django-settings-module=projectpal.settings",
          ],
      }
  ```

6. Create Django Tables by inputting the following into your command line then pressing enter:
  ```python manage.py migrate```

7. Configuring the Django Server
  Inside the .vscode folder, create a file namded "launch.json" and paste the follwing code into that file:
      ```markdown
          {
      "version": "0.2.0",
      "configurations": [
          {
              "name": "Python: Django",
              "type": "debugpy",
              "request": "launch",
              "program": "${workspaceFolder}/manage.py",
              "args": ["runserver"],
              "django": true,
              "autoReload":{
                  "enable": true
              }
          }
      ]
    }
     ```

9. Run Server by inputting the following into your command line or simply use the run server shortcut provided via the launch.json file:
  ```python manage.py runserver```

    - Once the server is running, you may start the client side with ```npm run dev``` then open the port provided within the terminal.
