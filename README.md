# RealEstateScrapingAPI
The following program is a scraper for real estate listing.

<h3>Running on windows</h3>
1. Download python 11 Installer from this [link](https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe)

2. Open the Installer and checkmark the `Add python.exe to PATH` [!!IMPORTANT!! Make Sure you checkmark add python.exe to PATH, we need python in PATH env]  

3. proceed and install the python 11

4. Open terminal like Powershell Or even VS code terminal would work too.

5. Navigate to cloned repo folder. `RealEstateScrapingAPI` (if you open the repo on VS code then your terminal would already be in the folder)

6. `cd` in to `ZameenScrapingAPI` with `cd .\ZameenScrapingAPI\`

7. type `pip install pipenv` and press enter, wait for Package to be installed.

8. type `pipenv install --dev` and press enter, wait for the packages to be installed.

9. type `pipenv install -r .\requirements.txt` and press enter, wait for packages to be installed.

10. Enter into virtual enviroment by typing `pipenv shell` and enter to enter the development enviroment.

11. Start the flask server by typing `flask --app .\index.py run` and press enter.

12. Navigate to `http:localhost:5000` and thats `https://scraper.macubesoftservices.com/` running on your local windows machine.
