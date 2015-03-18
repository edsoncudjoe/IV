Intervideo LTO History Reporter


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


------------
Installation
------------
Can be run from the command line. Currently needs the CatDVlib.py file to 
correctly access the CatDV Server API. If this is not available, it can 
still calculate information based on '.csv' files that have been outputted 
from the CatDV desktop software.

