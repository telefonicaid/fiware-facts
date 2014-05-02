# File to execute the covertura and unit test and generate the information
# to be shown in sonar
#
# __author__ = 'arobres'

virtualenv ENV
source ENV/bin/activate
mkdir /var/log/fiware-facts
chmod 777 /var/log/fiware-cloto
pip install -r requirements.txt
pip install -r requirements_dev.txt
python facts.py &
nosetests-2.6 -s -v --cover-package=facts --with-cover --cover-xml-file=target/site/cobertura/coverage.xml --cover-inclusive --cover-erase --cover-branches --cover-xml --with-xunit
kill $(lsof -t -i:5000)