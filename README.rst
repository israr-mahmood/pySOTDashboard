PySOT Dashboard
===============

PySOTDashboard is web application for pySOT, a asynchronous parallel 
optimization toolbox for global deterministic optimization problems. 
The purpose of this application is to facilitate the user to be able
to run the experiment remortly and moniter the results without 
having to install any of the dependencies on their machines. 

The toolbox is hosted on GitHub: 

.. code-block:: bash

   https://github.com/peiyu313/pySOTDashboard

Dependencies
------------

Before starting you will need Python 2.7.x. You need to have numpy, scipy, git and pip
installed and we recommend installing Anaconda/Miniconda for your desired Python version.

The setup file might not include some of the optional components of pySOT, if you want any
of them then you are going to have to install them manually by following the guide here. 

Installation
------------

Currenty the only way to install the dashboard is by cloning the github repository.
Run the following commands in the terminal


|  1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/peiyu313/pySOTDashboard

|  2.2. Navigate to the repository using:

   .. code-block:: bash

      cd pySOTDashboard

|  2.3. Install (you may need to use sudo for UNIX):

   .. code-block:: bash

      python setup.py install


Usage
-----

pySOTDashboard essentially provides the same features as pySOT as a 
web application. In order to understand the working of pySOT refer to:

.. code-block:: bash

   http://pysot.readthedocs.io/

Several pySOT examples can be found at:

.. code-block:: bash

   https://github.com/dme65/pySOT/tree/master/pySOT/test

Instruction on how to use the web client can be found in the docs.

FAQ
---

| Q: How do I start the application?
| A: Run the server "pySOTDashboard/pysotdashboard.py" and then navigate to 
	127.0.0.1:5000 in your browser to access the Client.	
|
| Q: Which version of Python is supported?
| A: All modules should work with Python 2 and Python 3. Except for the 
 	module_scrapper which is using inspect module. Therefore it is expected 
 	that you have Python 2 running.

note
----

The server and the client have not been integrated so for
at this point after completing every evaluation the server calls the
'abc' event for the websockets and sends the value for the evaluation
to the client. Ideally we would want to integrate bokeh to display 
the optimization results on a graph to the user. The code for the 
graph will go in the following method.

.. code-block:: bash

   file: pySOTDashboard/controller_object.py
   code: MonitorSubClass.on_complete
