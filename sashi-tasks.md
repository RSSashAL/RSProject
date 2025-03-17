# Data engineering and data architecture test problem
## Identify and programmatically pull data from an API that provides the following types of data (multiple APIs is fine):
- images
- json
- csv
## The data pulling script should include the following aspects:
- Written in Python
- Containerized with Docker
- Uses the Python requests library
## Create an architecture to store this data using the following criteria:
- All data elements need to be stored in or referenced by a node in Arango
    - This may mean that the postgres id or the file path information is stored in a node representing that data. It is up to you to decide how you want to store and access that data.
- All code needs to be executed via a Docker container. You may use a local installation for a database.
- Use the python-arango package for accessing arango from python
- Code should be written in functions/classes and use pep8 standards.

## Create a diagram illustrating your chosen architecture. Include documentation to explain your choices.