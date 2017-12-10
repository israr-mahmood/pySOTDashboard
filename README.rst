pySOT Dashboard
---------------

pySOTDashboard is web application for pySOT, a asynchronous parallel 
optimization toolbox for global deterministic optimization problems. 
The purpose of this application is to facilitate the user to be able
to run the experiment remortly and moniter the results without 
having to install any of the dependencies on their machines. 

The toolbox is hosted on GitHub: https://github.com/peiyu313/pySOTDashboard

Installation
------------

Run python setup.py install

Examples
--------

pySOTDashboard essentially provides the same features as pySOT as a 
web application. In order to understand the working of pySOT refer to:
http://pysot.readthedocs.io/

Several pySOT examples can be found at:
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
  module_scrapper which is using inspect module. Therefore it is expected that
	you have Python 2 running.
