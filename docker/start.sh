python setup.py sdist
pip install dist/fiware-facts-2.6.0.tar.gz
cd /
sleep 15
while ! nc -z redis 6379; do sleep 8; done
while ! nc -z rabbit 5672; do sleep 8; done
gunicorn facts.server:app -b 0.0.0.0:5000
