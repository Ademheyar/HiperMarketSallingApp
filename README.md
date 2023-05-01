#Selling App

This project is a Python-based selling application that includes a database called my_database. The database includes the following tables: pre_doc_table, doc_table, product, USERS, and tools. The application uses these tables to sell products and document the sales process, which are then recorded in the pre_doc_table and uploaded to the website.
Getting Started

To get started with the application, follow these steps:

    Clone the repository to your local machine
    Install Python on your machine if it is not already installed
    Install the required dependencies using pip install -r requirements.txt
    Create a config.py file that includes the necessary database credentials and configuration. An example file is included as config.example.py.
    Run the application using python app.py.

Application Structure

The application is structured as follows:

    app.py: This file contains the main application code and handles the routing and logic for the application.
    templates/: This directory contains the HTML templates for the application.
    static/: This directory contains the static files (e.g., CSS, JavaScript) for the application.
    database/: This directory contains the necessary database schema and migration files.

Database Structure

The my_database database includes the following tables:

    pre_doc_table: This table includes documentation of pre-sales processes.
    doc_table: This table includes documentation of post-sales processes.
    product: This table includes details about the products available for sale.
    USERS: This table includes user information such as usernames, passwords, and email addresses.
    tools: This table includes tools used by the application.

Contributing

If you wish to contribute to the application, please create a pull request and describe the changes you made. Any contribution is greatly appreciated.
License

This project is licensed under the MIT License - see the LICENSE file for details.
