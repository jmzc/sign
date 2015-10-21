#!/usr/bin/python

import sys, getopt, time
from urlparse import urlparse, parse_qs
from hashlib import sha1
from hmac import new as hmac
from urllib import urlencode


##########################################
# Prints usage help and exits with -2 code error
#
#
##########################################

def _usage(name):
        print name + ' -s <secret> -u <url> -i <encoding>'
	print '-s <secret> : Required. Shared secret'
	print '-u <url>: Required. URL to encoding' 
	print '-i <encoding>: Optional. Input character encoding. Default UTF-8'
        sys.exit(2)


def _encode(query):
        return urlencode(dict(item.split("=") for item in query.split("&")))

##########################################
# Returns a query string signed by secret
# query application/x-www-form-urlencoded
#
#########################
def _sign(secret,query):
        try:
		parameters = parse_qs(query,False,True)
                keys = sorted(parameters)
                result = ()
                for key in keys:
                        result = result + ((key, parameters[key][0]),)
                url = urlencode(result)
                print "Signing->" + secret + url + '&'
                mac = hmac(secret, secret + url + '&', sha1).digest().encode('base64')[:-1]

                return mac; 


        except ValueError:
                return 'Error'

##########################################
#
# Main
#
##########################################

def main(name,argv):

        secret 	 = '';
       	url 	 = '';
	encoding = 'UTF-8';

        try:
                opts, args = getopt.getopt(argv,"hs:u:i:")
        except getopt.GetoptError:
                _usage(name)
        for opt, arg in opts:
                if opt == '-h':
                        _usage(name);
                elif opt in ("-s"):
                         secret = arg
                elif opt in ("-u"):
                        url = arg
		elif opt in ("-i"):
		     	encoding = arg
        if secret == '' or url == '':
                _usage(name);
        else:
                 o = urlparse(unicode(url,encoding).encode('UTF-8'))
                 print _sign(secret,_encode(o.query))

#if the python interpreter is running that module (the source file) as the main program,
#it sets the special __name__ variable to have a value "__main__".
#If this file is being imported from another module, __name__ will be set to the module's name.
if __name__ == "__main__":
   main(sys.argv[0],sys.argv[1:])

