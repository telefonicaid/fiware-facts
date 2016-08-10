FROM ubuntu
RUN apt-get update
RUN apt-get -y install  python-dev \
   libpq-dev libmysqlclient-dev libpq-dev \
   git wget curl libffi-dev zip python-mysqldb \
   supervisor python-clips build-essential gcc
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py 
RUN git clone https://github.com/telefonicaid/fiware-facts /opt/fiware-facts
WORKDIR /opt/fiware-facts
RUN mkdir /var/log/fiware-facts 
RUN chmod 777 /var/log/fiware-facts
RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt
COPY sonar-project.properties sonar-project.properties
COPY config.py facts/config.py
COPY fiware-facts.cfg /etc/fiware.d/fiware-facts.cfg
RUN mkdir coverage
RUN mkdir test_results 
CMD sleep 15; export PYTHONPATH=$PWD; nosetests --with-coverage --cover-package=./ --cover-xml --cover-xml-file=coverage/coverage.xml --with-xunit --xunit-file=test_results/TEST-nosetests.xml --exe
