# taxi-prototype

INSTALL  
(should be compatible with any python 3 version)  
python3.6 -m venv .venv  
source .venv/bin/activate  
pip install -r requirements.txt  

python create_test_data.py

python run.py

http://localhost:5000/login  

login/pass:  
qwerty/qwerty  
asdfgh/asdfgh  
zxcvbn/zxcvbn  

i18n:  
pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot app  
pybabel update -i messages.pot -d app/translations  
pybabel compile -d app/translations  
