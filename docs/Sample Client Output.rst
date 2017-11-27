Sample Client Output
====================

{ "optimization_problem" : 
{"function" : "Ackley" , "dim" : 10} , 

"experimental_design" : 
{ "function" : "SymmetricLatinHypercube" , "dim" : 10, "npts" : 21 } , 

"surrogate_model" : { "function" : "RBFInterpolant" , "maxp" : 500 , "tail" : "LinearTail" , "kernel" : "CubicKernel" } , 

"adaptive_sampling" : { "function" : "CandidateDYCORS" , "numcand" : 100 , "weights" : -1 } , 

"controller" : { "function" : "SerialController" } , 

"strategy" : { "function" : "SyncStrategyNoConstraints" , "nsamples" : 1 , "proj_fun" : "projection" } }';
