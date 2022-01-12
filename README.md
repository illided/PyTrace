# PyTrace

Simple python utility to trace pathway taken by a 
packet on an IP network from source to destination 

To run it, firstly install all necessary dependencies:
```
pip install -r requirements.txt
```

Then run following command 
(you may need to run this as administrator).
```
python main.py --address [address or domain to trace]
```

Output (with mocked addresses):
```
0.0.0.0 Time: 11.54 ms
1.1.1.1 Time: 8.97 ms
1.2.3.4 Time: 4.98 ms
2.3.4.5 Time: 32.03 ms
No reply
8.9.10.11 Time: 31.54 ms Destination reached
```

You can also specify more parameters, for example number of requests 
for each hop or timeout for each request.

Run following to explore more parameters:
```
python main.py -h
```