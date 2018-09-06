tsm_pricing script
==================

Vey basic script to grab the average and realm pricing data for a list of items.

Usage
-----

api_key.txt
^^^^^^^^^^^

You must copy your tsm api key into the api_key.txt file.  Only one api key can be used at a time so this file
must contain only ONE api key.  The api key must be on the first line of the text file.

The api_key.txt file must be in the same directory as the tsm_pricing.py script file.


itme_list.txt
^^^^^^^^^^^^^

This file contains the item name and the item id (get this from wow head) in the key:value pair format.
For example (without the list formatting):

| Primal Fire:21884
| Primal shadow:22456
| Primal Water:21885

Only one item name and item id is allowed on each line and each pair must be on a single line, with no line
empty lines in between.  



Required Libraries
------------------

requests

pip install requests