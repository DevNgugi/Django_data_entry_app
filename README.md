# Django_data_entry_app
An API for posting and getting data, with an unknown  number of columns for each category.

**Requirements**

The app should:
 - accept multiple categories of data
 - enable addition of categories
 - ensure unique entries (no duplicates)
 - enable data search/filter
   
**Dependencies**

- All dependencies are listed in requirements.txt
- The major dependencies are:
    - Django
    - Django rest framework
    - pymongo (for interacting with MongoDB)
      
**How to Install**

- Download and install MongoDB Compass from https://www.mongodb.com/try/download/compass
- Clone the repository: git clone https://github.com/DevNgugi/Django_data_entry_app.git
- create a virtual environment. For help, see https://virtualenv.pypa.io/en/latest/installation.html
- Install dependencies listed in requirements.txt as so: pip install -r requirements.txt
- To ensure all dependencies have been installed type: pip list

  **Linking to the Database**
  - For this code, I have linked to the remote mongo db cluster, but you can use the local installation we did previously as follows:
      - go to settings.py and change the database host to "mongodb://localhost:27017"
      ![image](https://github.com/DevNgugi/Django_data_entry_app/assets/113933822/b1603c12-e3dd-4c3a-a7f8-fd553b6639d6)
      - change the connection_string also in api/views.py as so:
      ![image](https://github.com/DevNgugi/Django_data_entry_app/assets/113933822/95a7cb3b-7f9a-43b5-8a2e-eab42b56d01c)
  - Run Migrations: python manage.py migrate
  - This should now reflect in you mongodbcompass like so:
  - ![image](https://github.com/DevNgugi/Django_data_entry_app/assets/113933822/5ae88857-f0f4-45b6-9de9-8475a3bdedff)
  - run server : python manage.py runserver

**Usage**
The endpoints for the API are:
 - GET /api request shows all the entries in the database
 - POST /api request posts data to the database
 - /api/category:
     Supports POST only. The reponse is a filter of all documents/data that belong to a specific category
 - /api/search: Supports POST only. The response is a filter of all records that have a specific keyword

Examples:
  - Saving Data:
  -    ![image](https://github.com/DevNgugi/Django_data_entry_app/assets/113933822/16468d87-b866-4de5-beee-203f3b6b8ccb)
  -    NB: The data must have a category key, otherwise it will return an error
  -    ![image](https://github.com/DevNgugi/Django_data_entry_app/assets/113933822/7bd4bf95-d087-4802-b8e1-a59251959abd)
  -    Trying to save same data twice will also result in an error, as the records(documents) must be unique
  -    ![image](https://github.com/DevNgugi/Django_data_entry_app/assets/113933822/4e73d411-c123-4d30-be59-2f892149510b)

   - Searching by Category:
   - Pass the category value as shown below. The Json Data has to match the format or get a format error. as shown below
   - ![image](https://github.com/DevNgugi/Django_data_entry_app/assets/113933822/a317cc23-dd16-43d2-b670-d77c6761f5f7)
   - A success should return all records/documents with the said category
   - ![image](https://github.com/DevNgugi/Django_data_entry_app/assets/113933822/fea26751-1efe-4e51-a3ac-ca6e1847239c)

  - Searching by keyword
  - As in searching by category, pass the keyword, and the field that needs to match in your request as shown below
   ![image](https://github.com/DevNgugi/Django_data_entry_app/assets/113933822/c2b99f79-3724-4a3b-ae2f-350b251ce731)
  - The search patterns are implemented using regex to get substrings, and make the search case insensitive

**Testing**
- You can run tests using python manage.py test

**CI/CD**
The project uses github actions for CI. The setup can be fould at .github/workflows/django.yml, which runs the test automatically every time a push command is executed.

**Database Design**
The api uses Mongodb for two reasons:

 - We can add multiple categories, but we dont know the number of columns that each category will have. So it will be hard to create such database schema using relational databases.
 - MongoDb is document-based, which are easily convertible into python dictionaries/ json using built in JSON encoders/decoders and more flexible for multiple data types.

 

