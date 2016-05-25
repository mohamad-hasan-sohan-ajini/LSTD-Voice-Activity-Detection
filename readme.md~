LSTD Voice Activity Detection:
===========================
Implementation of [LSTD](http://www.sciencedirect.com/science/article/pii/S0167639303001201) Voice Activity Detection, plus appropiate sound wave plots.


prerequests:
-----------
In order to run examples, you need to install following python libraries:

numpy and scipy
matplotlib
[pyaudio](http://people.csail.mit.edu/hubert/pyaudio/)

testing:
-------
first you need to run a process in order to record sound from you PC/laptop microphoe:

```python wire_callback.py```

after that, you must run the test script to see the result:

```python test.py```

* For best result, please be quite for 3 seconds after running test script.
In this period, the VAD algorithm will detect background noise in order to rubustness in noisy environments.
After that, the sound wave plots will be depicted and the VAD system is ready for testing. 
The short time window (lower plot) will be red for Voice parts and blue for silent parts.
