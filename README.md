## Instructions to run Scraper
1. Create a virtual environment and activate it.
2. Change directory to project root directory.
3. Run 'pip install -r requirements.txt' to install all required libraries.
4. Download chromedriver that matches your chrome browser and rename it to 'chromedriver'
5. Copy and paste chromedriver into /src/chromedriver/ directory.
6. Create db tables and populate them them by running 'python src/scripts/break_the_db.py' command.
7. Now you would have some scraper configurators created in ScrapConfigurator table in db. You can add a few more if needed.
8. Run 'python src/app.py' to scrape and store data against all configurators created in db. 
