# csv-stats

Designed a one page django website that allows user to enter a path to a CSV file and compute various statistics on it based on the CSV file's categories. Created for an honors project in CSE445 at Arizona State University.

![image](https://user-images.githubusercontent.com/72316669/140620100-4d2d7e08-0631-46da-b17d-8e31bc832b42.png)

User is able to enter link to CSV file and then click "Parse CSV" to display the categories. From there, the user selects which categories they would like to compute statistics on. When they are done selecting, a user hits the "Calculate" button. The website is also able to error check if the user tries to request in incorrect/invalid results and displays an error message at the bottom, below the reset button. In addition, the program is able to check if the url is valid and leads to a CSV file, warning the user if not. The reset button is for removing all context from the screen in the simplest manner possible

----
### How To Run
1. Nagivate to the frontend directory and run the command `python manage.py runserver`
2. In a separate terminal, navigate to the backend directory and run the command `python app.py`
3. Open browser to https://localhost:8000



### Implementation
Implemented frontend using **django** and **bootstrap css**
Implemented backend using **flask** with **pandas** and **numpy** libraries for csv processing
