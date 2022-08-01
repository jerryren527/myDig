# myDig - DNS Lookup
_myDig_ is a DNS resolver inspired by the `dig` Linux command. 


## Introduction
This program takes as input a domain name and resolves the query to the complete IP address or CNAME by contacting the root server, the top-level domain, all the way until the authoritative name server. It is developed in Python using the `dnspython` library, the `dns.message.make_query` API, and the `dns.query.udp` API.

## Setup
Clone this repository to your local computer. Download the `dnspython` package with a package manager, like `pip`.
```
$ cd ./myDig
$ pip3 install dnspython
```

## Running the Project
To run `mydig.py`, provide two command line arguments:

1. a domain name (e.g., google.com)
2. a root server IP address (e.g. Google's public DNS 8.8.8.8, or 8.8.4.4)

This program will print to the console a Question section and Answer section. The Question section contains the name of the server that was queried (google.com), and the class and type of the query ("IN" stands for internet; "A" stands for address). The Answer section contains the IP address associated with the domain name, the query time allotted, and the date and time which the query occurred.
```
$ python3 mydig.py google.com 72.229.5.209
QUESTION SECTION:
google.com        IN A
ANSWER SECTION:
google.com  20 IN A 142.250.80.78
Query time: 41.42 ms
WHEN: 2022-07-31 22:48:44.270095
```