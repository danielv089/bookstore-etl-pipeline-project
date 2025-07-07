## Changelog

- **v2.0 – Python, PostgreSQL  & Docker Compose Integration**
   - Changed backend database to PostgreSQL instead of SQLite
   - Added Docker Compose file for multi-container development and deployment of the ETL image and PostgreSQL containers
   - Implemented persistent data volumes for PostgreSQL container
   - Configured environmental variables in the Docker Compose file and the ETL pipeline
   - Importing data by using PostgreSQL’s COPY command for bulk CSV imports

- **v1.5 – Python, SQLite and Docker**
   - Pytest added 
   - Dockerbuild image added

- **v1.4 – Python and SQLite**
   - Refactored the ETL pipeline to be fully modularized with separate modules for extract, transform, normalize, and load functions 
   - Added error handling with try/except blocks across all stages
   - Added sleep parameter to limit the number of pages scraped not to overload server
   - Added main script (main.py) to orchestrate the entire pipeline
   - Reorganized project folder structure
   - Improved code readability, maintainability, and modularity

- **v1.2 – Python and SQLite**
  - Replaced custom logger with Python's logging module
  - Corrected genre classification

- **v1.1 – Python and SQLite**
  - Changed `for` loop to `while` loop  
  - Minor code refactoring

- **v1.0 – Python and SQLite**
