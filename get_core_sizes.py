import sys,getopt
import json
import subprocess

def main(argv):

   solr_host=""

   try:
      opts, args = getopt.getopt(argv,"s:h")
   except getopt.GetoptError:
      print 'get_core_sizes.py -s <solr host>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'get_core_sizes.py -s <solr host>' 
         sys.exit()
      elif opt in ("-s", "--solr-host"):
         solr_host = arg

   cmd = "/usr/bin/curl --negotiate -u : 'https://"+solr_host+":8985/solr/admin/collections?action=CLUSTERSTATUS&wt=json'"
   proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
   output=proc.stdout.read()
   data=json.loads(output)
   cluster=data.get('cluster')
   collections=data.get('cluster').get('collections')
   for collection in collections:
      print collection

   sizes = ""
   for collection in collections:
     shards=collections[collection].get("shards")
     for shard in shards:
        replicas=shards[shard].get("replicas")
        for replica in replicas:
           baseurl=replicas[replica].get("base_url")
           core=replicas[replica].get("core")
           state=replicas[replica].get("state")
           if state == "active":
              cmd="curl --negotiate -u : '"+baseurl+"/"+"admin/cores?action=STATUS&wt=json&core="+core+"'"
              proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=None)
              output=proc.stdout.read()
              data=json.loads(output)
              status=data.get("status")
              for metric in status:
                 size = status[metric].get("index").get("size")
                 sizes = sizes +"\nCore: "+core+" URL: "+baseurl+" Size: "+size 

   print sizes

if __name__ == "__main__":
   main(sys.argv[1:])
