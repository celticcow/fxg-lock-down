#!/usr/bin/python3 -W ignore::DeprecationWarning

import requests
import json
import sys
import time
import ipaddress
import apifunctions
import cgi,cgitb
import apifunctions

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    debug = 1

    #create instance for field storage
    form = cgi.FieldStorage()

    userid = form.getvalue('user')
    passwd = form.getvalue('password')

    ip_addr = "146.18.96.16"
    ip_cma  = "146.18.96.25"

    ### get form data fields
    site_name = form.getvalue('sitename')
    site_num  = form.getvalue('sitenumber')

    sgshosts_raw = form.getvalue('sgshosts')
    sickhosts_raw = form.getvalue('sickhosts')
    autodim_raw = form.getvalue('autodimhosts')
    spidr_raw = form.getvalue('spidrhosts')

    admin_name = form.getvalue('adminname')
    admin_ipaddr = form.getvalue('adminip')

    preload_name1 = form.getvalue('preloadhostname1')
    preload_name2 = form.getvalue('preloadhostname2')
    preload_ipaddr1 = form.getvalue('preloadipaddr1')
    preload_ipaddr2 = form.getvalue('preloadipaddr2')


    ## html header and config data dump
    print ("Content-type:text/html\r\n\r\n")
    print ("<html>")
    print ("<head>")
    print ("<title>Lock Down Build</title>")
    print ("</head>")
    print ("<body>")


    #### to be removed later ####
    print(userid, end="<br>")
    print(passwd, end="<br>")
    #############################

    if(debug == 1):
        ### Data Dump of form values
        print("------------------------------", end="<br>")
        print(site_name, end="<br>")
        print(site_num, end="<br>")
        print(sgshosts_raw, end="<br>")
        print(sickhosts_raw, end="<br>")
        print(autodim_raw, end="<br>")
        print(spidr_raw, end="<br>")
        print(admin_name, end="<br>")
        print(admin_ipaddr, end="<br>")
        print(preload_name1, end="<br>")
        print(preload_ipaddr1, end="<br>")
        print(preload_name2, end="<br>")
        print(preload_ipaddr2, end="<br>")
        print("------------------------------", end="<br>")

    ### Logout Info

    print("------- end of program -------")
    print("<br><br>")
    print("</body>")
    print("</html>")
#end of main

if __name__ == "__main__":
    main()
#end of program