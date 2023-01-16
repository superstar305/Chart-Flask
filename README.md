# Initialize
python -m venv venv
venv/scripts/activate
pip install -r requirement.txt
pip freeze > requirement.txt

# Run
Flask Run

#  First, Database Migration
Flask db init
Flask db migrate
Flask db upgrade
# If there is a migrations folder, only
Flask db upgrade

# Second, Add programmatically testing data to database
python seed.py