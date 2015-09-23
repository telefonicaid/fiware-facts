========================================
FIWARE | FACTS | Acceptance test project
========================================

This project contains the Facts' (PolicyManager) acceptance tests (component, integration and E2E testing).
All test cases have been defined using Gherkin that it is a Business Readable, Domain Specific Language that lets you
describe software’s behaviour without detailing how that behaviour is implemented.
Gherkin has the purpose of serving documentation of test cases.


Test case implementation has been performed using `Python`_ and the BDD framework
`Behave`_.

Acceptance Project Structure
============================
 ::

    ├───acceptance
    │   ├───commons
    │   ├───features
    │   │   ├───component
    │   │   │   ├───steps
    │   │   │   │   ├───context_update.py
    │   │   │   │   └───...
    │   │   │   ├───environment.py
    │   │   │   ├───context_update.feature
    │   │   │   └───...
    │   │   └───...
    │   ├───fiwarecloto_client
    │   ├───fiwarefacts_client
    │   └───settings
    │       └───settings.json
    │


FIWARE Facts Automation Framework
=================================

Features:

- BDD features
- Behave support.
- Settings using json files.
- Test report using xUnit output and Behave output.
- Assertions using Hamcrest (declaratively define "match" rules).
- Fiware-Facts Client.
- Fiware-Facts Cloto.
- Logging.

Domain specific language implemented for building features: `Fiware-Facts Acceptance DSL <doc/dsl.rst>`_


Acceptance test execution
=========================

Execute the following command in the acceptance test project directory:

::

  $> cd $FACTS_HOME/tests/acceptance
  $> behave features/component --tags ~@skip

With this command, you will execute:

- Test Cases with the environment configuration defined in `settings/settings.json`.
- all *.features implemented for *component* testing.
- Skipping all Scenarios tagged with *skip*.

For more options, execute::

  $> behave --help


Prerequisites
-------------

- `Python`_ or newer (2.x).
- `pip`_.
- `Virtualenv`_.
- `Fiware-Facts`_.

Test case execution using virtualenv
------------------------------------

1. Create a virtual environment somewhere::

      $> virtualenv $WORKON_HOME/venv

#. Activate the virtual environment::

      $> source $WORKON_HOME/venv/bin/activate)

#. Go to `$FACTS_HOME/tests/acceptance` folder in the project.
#. Install the requirements for the acceptance tests in the virtual environment::

      $> pip install -r requirements.txt --allow-all-external)

Test case execution using Vagrant (optional)
--------------------------------------------

Instead of using virtualenv, you can use the provided Vagrantfile to deploy a local VM
using `Vagrant`_, that will provide all environment configurations
for launching test cases.

1. Download and install `Vagrant`_.
#. Go to `FACTS_HOME/tests/acceptance` folder in the project.
#. Execute *vagrant up* to launch a VM based on the Vagrantfile provided.
#. After Vagrant provision, your VM is properly configured to launch acceptance tests.
   You have to access to the VM using *vagrant ssh* and change to */vagrant* directory that will have
   mounted your workspace *(test/acceptance)*.

If you need more information about how to use Vagrant, you can see `Vagrant Getting Started`_.

Settings
========

Project properties
------------------

Before executing the acceptance tests, you need configure the properties in the file `settings/settings.json` for each
service properly::

    {
        "environment": {
            "name": "qa"
        },
        "facts_service": {
            "protocol": "http",
            "host": "1.2.3.4",
            "port": "5000",
            "resource": "/v1.0",
            "os_tenant_id": "00000000000000000000000000000000",
            "facts_grace_period": 10
        },
        "cloto_service": {
            "protocol": "http",
            "host": "1.2.3.4",
            "port": "8000",
            "resource": "/v1.0",
            "os_username": "myusername",
            "os_password": "mypassword",
            "os_tenant_id": "00000000000000000000000000000000",
            "os_auth_url": "http://my-keystone:4731/v2.0"
        },
        "rabbitmq_service": {
            "host": "130.206.81.209",
            "port": "5672",
            "user": "qa",
            "password": "testing",
            "facts_messages": {
              "exchange_name": "facts",
              "exchange_type": "direct",
              "queue": "facts"
            },
            "facts_window_size":{
              "exchange_name": "windowsizes",
              "routing_key": "windowsizes"
            }
        }
    }


RabbitMQ configuration for testing
----------------------------------

The FACTS' component test cases are executed integrated with RabbitMQ.
Then, before executing test cases, you should configure RabbitMQ to accept connections
from a new remote user::

    root@ubuntu1404:/etc/init.d# rabbitmqctl add_user {rabbitmq_username} {rabbitmq_password}
    root@ubuntu1404:/etc/init.d# rabbitmqctl set_permissions -p / {rabbitmq_username} ".*" ".*" ".*"
    root@ubuntu1404:/etc/init.d# rabbitmqctl set_user_tags {rabbitmq_username} administrator


That user credentials should be configured in the project properties (`rabbitmq_service` property)
to be used by test cases. The rest of RabbitMQ configuration should be configured
according to FACTS' configuration.


API endpoint
------------

- **protocol**: `http` or `https`
- **host**: Host name or IP
- **port**: API port
- **resource**: Base API URI

OpenStack credentials
---------------------

- **os_keystone_url**: Keystone URL.
- **os_tenant_id**: Tenant ID.
- **os_tenant_name**: Tenant Name.
- **os_user_domain_name**: Domain Name for the user (Keystone v3).
- **os_user**: Username.
- **os_password**: User password.

.. REFERENCES

.. _Python: http://www.python.org/
.. _Behave: http://pythonhosted.org/behave/
.. _pip: https://pypi.python.org/pypi/pip
.. _Virtualenv: https://pypi.python.org/pypi/virtualenv
.. _Fiware-Facts: https://github.com/telefonicaid/fiware-facts
.. _Vagrant: https://www.vagrantup.com/
.. _Vagrant Getting Started: https://docs.vagrantup.com/v2/getting-started/index.html
