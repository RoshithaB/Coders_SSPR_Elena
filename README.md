# cs520_EleNa

Elevation-based Navigation (EleNa) is an application that helps users determine the path to travel based on their choice.  The users will be allowed to choose from the following options:
->  Route with maximum elevation gain 
->  Route with minimum elevation gain
The user can also decide the maximum percentage of the shortest route that they would like to take. 
For example, the user can set the maximum length of the path to be 150% of the shortest path.


Steps to run:

# Linux
sudo apt-get install python3-venv    # If needed

pip install -r requirements

From src directory

./src/run.sh

# macOS
pip install -r requirements

From src directory

./src/run.sh

# Windows
pip install -r requirements.txt

set FLASK_ENV=development

set FLASK_APP=src/webapp.py

flask run 

preferable Jinja2 version: 2.11.3

# To run the test suites
## In one terminal
from src directory
./src/run.sh

## From another terminal
Migrate to src/test directory
Run the commands listed below
1. python UITestSuite.py
2. python AlgoTestSuite.py
3. python MVCTestSuite.py

