# get_core_sizes.py

This python script will retrieve the active shards (core).
Usage:

python get_core_sizes.py -s <solr host>

Note: This script uses the subprocess module to make the curl command. Originally I wanted to use the request module to make REST calls, but it doesn't support kerberos. There is the requests_kerberos module, but I didn't want to force another dependency, or make the script more complicated.
 

