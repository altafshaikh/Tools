# X Scrappy

## The Subdomain Finder

X Scrappy is a python based tool. which is used to find and collect sub-domains for a given domain from various websites.

## Supported Services:
The tool is collecting data from the following services:
* [CRT.sh](https://crt.sh/)
* [Censys](https://censys.io/)
* [HackerTarget](https://hackertarget.com/)
* [ThreatCrowd](https://www.threatcrowd.org/)

## Features
 * Find Subdomains from various services
 * Filter Out Duplicates sub-domains
 * Stores all the unique subdomains into a file inside the folder with the name of the domain.

## Demo
[![Tool Working Demo](https://img.youtube.com/vi/4thNDNLRat0/0.jpg)](https://www.youtube.com/watch?v=4thNDNLRat0)

## Dependencies
`python3`

## Requirements

|Package|Version|
|---|---|
|requests|2.22.0|
|beautifulsoup4|4.8.2|
|censys|0.0.8|
|shodan|1.11.1|
|termcolor|1.1.0|

## Installation

1. Normal installation:
```
$ git clone https://github.com/altaf99/Tools.git
$ python3 -m pip install -r requirements.txt
```

2. Preferably install in a virtualenv:
```
Clone the repo into your machine
$ git clone https://github.com/altaf99/Tools.git

Create a virtual environment,
$ virtualenv -p /usr/bin/python3.8 myvenv

Now, at last, we just need to activate it, using the command
$ source myvenv/bin/activate

Now you are in a Python virtual environment

You can deactivate using
$ deactivate

and now install all the requirements
$ python3 -m pip install -r requirements.txt

```

## Setup
the tool requires an API key for Censys,
visit [Censys API](https://censys.io/api) and Sign Up to get the below API credentials.
```
CENSYS_API_ID
CENSYS_API_SECRET
```
## Setting environment variable :
use the below command to set the environment variable, assign the value to the variables with your credentials, and enter the command in the terminal.
```
export CENSYS_API_ID="YOUR_ID"
export CENSYS_API_SECRET="YOUR_SECRET"
```

## Usage:
```
python3 x_scrappy.py domain
```

## Example:
```
python3 x_scrappy.py google.com
```
## Credits:

### Developed by
[Altaf Shaikh](https://github.com/altafshaikh)<br>
[Email](mailto:iamaltafshaikh@gmail.com)

### Special Thanks
The tool is made as a part of the STTP Program by [We Are plymouths](https://github.com/wap-plymouths)<br>
Thank You So much for conduction such a wonderful 21 days program :100: 



Also thanks to [Harsh Bothra](https://github.com/harsh-bothra) sir for helping me to build the tool :)


