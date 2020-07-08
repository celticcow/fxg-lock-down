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

def preflight_groups_locked(ipaddr, sid):
    print("in groups_locked", end="<br>")
    
    
    return(False) #default condition

def preflight_objects_valid(sgshost, sickhost, autodim, spidr, admin_ipaddr, preload_ipaddr1, preload_ipaddr2):
    print("in objects_valid", end="<br>")

    if((preflight_host_group_valid(sgshost) == True) and (preflight_host_group_valid(sickhost) == True) and (preflight_host_group_valid(autodim) == True) and (preflight_host_group_valid(spidr) == True) and (preflight_host_valid(admin_ipaddr) == True) and (preflight_host_valid(preload_ipaddr1) == True) and (preflight_host_valid(preload_ipaddr2) == True)):
        return(True)
    else:
        return(False)


def preflight_host_group_valid(grp):
    print("in host group valid")

    for host in grp:
        if(preflight_host_valid(host) == False):
            return(False)
    
    return(True)
#end of preflight_host_group_valid

def preflight_host_valid(address):
    print("in host_valid")

    try:
        if(ipaddress.ip_address(address)):
            print("valid IP", end="<br>")
            return(True)
        else:
            print("Invalid IP", end="<br>")
            return(False)
    except ValueError:
        print("Invalid IP", end="<br>")

        return(False)
#end of preflight_host_valid

"""
"""

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
    #print(userid, end="<br>")
    #print(passwd, end="<br>")
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

    #manipulate textarea hosts
    sgshost_stage1 = str(sgshosts_raw)
    sickhost_stage1 = str(sickhosts_raw)
    autodim_stage1 = str(autodim_raw)
    spidr_stage1 = str(spidr_raw)

    sgshost_stage2 = sgshost_stage1.split(' ')
    sickhost_stage2 = sickhost_stage1.split(' ')
    autodim_stage2 = autodim_stage1.split(' ')
    spidr_stage2 = spidr_stage1.split(' ')

    sgshost = sgshost_stage2[0].split()
    sickhost = sickhost_stage2[0].split()
    autodim = autodim_stage2[0].split()
    spidr = spidr_stage2[0].split()

    if(debug == 1):
        print("++++++++++++++++++++++++++++++", end="<br>")
        print(sgshost, end="<br>")
        print(sickhost, end="<br>")
        print(autodim, end="<br>")
        print(spidr, end="<br>")
        print("++++++++++++++++++++++++++++++", end="<br>")

    #if((preflight_host_group_valid(sgshost) == True) and (preflight_host_group_valid(sickhost) == True) and (preflight_host_group_valid(autodim) == True) and (preflight_host_group_valid(spidr) == True) and (preflight_host_valid(admin_ipaddr) == True) and (preflight_host_valid(preload_ipaddr1) == True) and (preflight_host_valid(preload_ipaddr2) == True) ):
    

    if((preflight_objects_valid(sgshost, sickhost, autodim, spidr, admin_ipaddr, preload_ipaddr1, preload_ipaddr2) == True) and (preflight_groups_locked() == False)):
        print("Pre-Flight Checks Complete", end="<br>")
    else:
        print("<h1>STOP postoji pogreška</h1>", end="<br>")

    ### Logout Info

    print("------- end of program -------")
    print("<br><br>")
    print("</body>")
    print("</html>")
#end of main

if __name__ == "__main__":
    main()
#end of program