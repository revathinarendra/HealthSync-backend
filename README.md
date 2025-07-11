DRY PROJECT
Description
    About The Project
    This project includes a DRY (Don't Repeat Yourself) implementation for user authentication and profile management. It features:

        - A custom Account model with email-based login and password authentication.
        - Role-based user management with user, admin, and superadmin roles.
        - A linked UserProfile model for storing additional user information.
        - account activation functionalities.
        - A clean, reusable structure to ensure maintainability and scalability.

Setup Instructions:

1. .Clone the repository git clone https://github.com/revathinarendra/dry



2. Navigrate to the working directory  cd dry



3. Open the project from the code editor code . or atom .



4. Create virtual environment python -m venv env


5. Activate the virtual environment source env/Scripts/activate


6. Install required packages to run the project pip install -r requirements.txt


7. .Rename .env-sample to .env


8. Fill up the environment variables: Generate your own Secret key using this tool https://djecrety.ir/, copy and paste the secret key in the SECRET_KEY field.
     Your configuration should look something like this:

        - SECRET_KEY=47d)n05#ei0rg4#)*@fuhc%$5+0n(t%jgxg$)!1pkegsi*l4c%


        - DEBUG=True


        - #if you are using supabase database setting 


        - SUPABASE_URL=

        - SUPABASE_ANON_KEY=


        - SUPBASE_DB_NAME= 

        - SUPBASE_DB_USER=


        - SUPBASE_DB_PASSWORD= 


        - SUPBASE_DB_HOST=  


        - SUPBASE_DB_PORT =


9. .Create database tables
        python manage.py migrate

10. Create a super user    
        python manage.py createsuperuser
        
        GitBash users may have to run this to create a super user - winpty python manage.py createsuperuser

11..Run server

        python manage.py runserver

12. Login to admin panel - (http://127.0.0.1:8000/admin/)



13. Then we can we api endpoints for User creation , login, userprofile for additional setup

## Live Demo

Check out the live demo of DRY [here]https://dry-weld.vercel.app/

Support

💙 If you like this project, give it a ⭐ and share it with friends!

Contact Me
