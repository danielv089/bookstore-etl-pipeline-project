## Changelog

- **v1.5 – Python, SQLite and Docker**
   - Pytest added to enable testing
   - Added Docker suppor to containerize the ETL pipeline for easier deployment

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
