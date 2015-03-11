Intervideo LTO History Reporter

CatDVlib.py

-----------
What is it?
-----------

LTO History Reporter
--------------------
The reporter is a program that provides information on the amount data 
that has been archived to LTO tape. The length of time can be defined by
the user. It was designed as a link between Squarebox's CatDV assest
management software and GB-Labs Space LTO archiving machine. 

The project involved finding a way to report the amount of data archived 
to LTO for separate clients. Once this information was found, the data
had to provided in a clear format.

To run this on the terminal you first need to get either a JSON or CSV 
file from GB-Labs Tape History Manager. Once you have this you can call 
the reporter along with the GB-Labs file in the terminal.

example:
	
	python ltohistory.py history.json


The Latest Version
------------------

	1.0.2 Added access to the CatDV Server API to allow remote download
		of catalog information.

		Added JSON compatibility. The reporter can now extract data from
		GB-Labs JSON file formats.

		Choice of whether to collect data fom CatDV API or from manually
		created files

	1.0.0 Initial build

CatDVlib.py
-----------
This library acts as a wrapper for CatDV's Server API. It was designed to 
quickly download information from the server and acts as a replacement to
manually exporting data from the CatDV GUI.

To use you would have to first set the URL of the location of the CatDV
server. This could possibly be 'localhost:8080' if the server is installed 
on your local machine.

Once the URL is set you can then login to the server to get access to the
stored clips and catalog information.

example:

	from CatDVlib import Cdvlib

	user = Cdvlib()

	url = user.setUrl() # Sets the location of the CatDV Server API

	# Stores the login session key once the user has logged in
	key = user.getSessionKey()   

	# Get clips of any given catalog.
	clips = user.getCatalogClips(user.catalog_names[0][1])

The Latest Version
------------------

	1.0.0 Initial Build

------------
Installation
------------

LTO History Reporter
--------------------

Can be run from the command line. Currently needs the CatDVlib.py file to 
correctly access the CatDV Server API. If this is not available, it can 
still calculate information based on '.csv' files that have been outputted 
from the CatDV desktop software.

CatDVlib.py
-----------

Needs the Requests python library to be installed. The file can be run directly
from the terminal. 


