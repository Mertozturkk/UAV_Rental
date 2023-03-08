# UAV Rental Project using Django

This is a project for UAV (Unmanned Aerial Vehicle) rental service. It allows customers to browse UAV models, make a reservation, and pay for the rental. The project is built with Django, and uses PostgreSQL as the database management system. Docker is used for containerization and deployment of the application.

## Prerequisites

Before starting the project, make sure you have the following software installed:

- Docker
- Docker Compose
- Python 3.8 or higher


## Installation

1. Clone the repository:

        
        git clone https://github.com/your-username/uav-rental-project.git
        cd uav-rental-project

2. Create a virtual environment and activate it:

        
        python3 -m venv venv
        source venv/bin/activate

3. Install the dependencies:

            
            pip install -r requirements.txt





# UAV Rental Project
This is a Django-based web application that allows users to rent unmanned aerial vehicles (UAVs) for a specified period of time. The project utilizes Docker, PostgreSQL, and Docker Compose to facilitate deployment and management.

## Installation
Clone the repository:


    git clone https://github.com/username/UAV-Rental.git
    cd UAV-Rental
## Build and start Docker containers:

    docker-compose up --build
This will create and start two Docker containers: one for the web application and one for the PostgreSQL database.

## Create the database schema:

    docker-compose exec web python manage.py migrate
This will run the Django migration scripts to create the necessary database tables.

## Create a superuser account:

    docker-compose exec web python manage.py createsuperuser
Follow the prompts to create a superuser account, which will have access to the Django admin interface.

## Load initial data (optional):

    docker-compose exec web python manage.py loaddata initial_data.json
This will load some initial data into the database, such as sample UAV models and rental rates. This step is optional, but it may be useful for testing or demonstration purposes.

## Usage
Once the application is installed and running, you can access it by opening a web browser and navigating to http://localhost:8000/. The home page will display a list of available UAV models, along with their rental rates and a link to the rental form.

To rent a UAV, click on the "Rent" button next to the desired model. This will take you to a rental form where you can specify the rental period and provide your contact information. After submitting the form, you will receive a confirmation email with further instructions.

To manage the rental process, you can log in to the Django admin interface at http://localhost:8000/admin/. From there, you can view and modify rental orders, as well as add or edit UAV models and rental rates.