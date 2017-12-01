Surrogate Optimization Problem
==============================
In order to start the Surrogate Optimization the client has to send four components over to the server.
1. Optimization problem
2. Surrogate model
3. Experimental design 
4. Adaptive sampling

A list of all possible object available to initialize their components is sent over to the client from the server, this list is explained in PySOT Dictionary Layout. The user will select their desired object from the list (displayed on the client's user interface) and hit the 'run' button. The client then compiles a JSON using the selected parameters and sends it over to the server over web-sockets. One sample JSON object is shown below. 

.. code-block:: json
   :linenos:
   
   '{ 
   "optimization_problem" : 
   {"function" : "Ackley" , "dim" : 10} , 
   "experimental_design" : 
   { "function" : "SymmetricLatinHypercube" , "dim" : 10, "npts" : 21 } , 
   "surrogate_model" : { "function" : "RBFInterpolant" , "maxp" : 500 , "tail" : "LinearTail" , "kernel" : "CubicKernel" } , 
   "adaptive_sampling" : { "function" : "CandidateDYCORS" , "numcand" : 100 , "weights" : -1 } , 
   "controller" : { "function" : "SerialController" } , 
   "strategy" : { "function" : "SyncStrategyNoConstraints" , "nsamples" : 1 , "proj_fun" : "projection" } 
   }';

**Explanation**
There is separate entry in the JSON for each of the four components. The key for each of the component is the component name and the value is another JSON object containing the object name and the arguments required to initialize that object. The key "function" refers to the object and the following key, value pairs are the argument name and their value. Note that 
