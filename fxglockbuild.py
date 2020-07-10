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

def preflight_groups_locked(ip_addr, sid):
    print("in groups_locked", end="<br>")
    if((apifunctions.object_is_locked(ip_addr, "Local-Preload-Assist", sid)) or (apifunctions.object_is_locked(ip_addr, "Local-ISS-Admin-Server", sid)) or (apifunctions.object_is_locked(ip_addr, "SSPC-Autodim", sid)) or (apifunctions.object_is_locked(ip_addr, "SSPC-SICK", sid)) or (apifunctions.object_is_locked(ip_addr, "SPIDR_Hubs", sid)) or (apifunctions.object_is_locked(ip_addr, "FXG-SGS", sid))): 
        print("a high level group is LOCKED", end="<br>")
        return(True)
    else:
        print("Main groups are unlocked", end="<br>")
        return(False)
    """
    Local-PreLoad-Assist
    Local-ISS-Admin-Server
    SSPC-SICK
    SPIDR_Hubs
    SSPC-Autodim
    FXG-SGS
    """
#end of preflight_group_locked()

def preflight_objects_valid(sgshost, sickhost, autodim, spidr, admin_ipaddr, preload_ipaddr1, preload_ipaddr2):
    print("in objects_valid", end="<br>")

    if((preflight_host_group_valid(sgshost) == True) and (preflight_host_group_valid(sickhost) == True) and (preflight_host_group_valid(autodim) == True) and (preflight_host_group_valid(spidr) == True) and (preflight_host_valid(admin_ipaddr) == True) and (preflight_host_valid(preload_ipaddr1) == True) and (preflight_host_valid(preload_ipaddr2) == True)):
        return(True)
    else:
        return(False)
#end of preflight_objects_valid

def preflight_host_group_valid(grp):
    print("in host group valid", end="<br>")

    for host in grp:
        if(preflight_host_valid(host) == False):
            return(False)
    
    return(True)
#end of preflight_host_group_valid

def preflight_host_valid(address):
    print("in host_valid", end="<br>")

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

def build_group_and_hosts(maingrp, localgroup, hostlist, prefix, ip_addr, sid):
    print("in build_group_and_host()", end="<br>")

    debug = 1

    ## create a group ##
    apifunctions.add_a_group(ip_addr, localgroup, sid)
    apifunctions.add_group_to_group(ip_addr, localgroup, maingrp, sid)

    ## add localgroup to maingrp

    for x in hostlist:
        if(debug == 1):
            print("<br>^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^<br>")
            print(x, end="<br>")
            print(prefix, end="<br>")
            print(localgroup, end="<br>")
            print("<br>^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^<br>")

        apifunctions.add_a_host_with_group(ip_addr, prefix+x, x, localgroup, sid)
        ## add host and add to local group
#end of build_group_and_hosts

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
    print("Content-type:text/html\r\n\r\n")
    print("<html>")
    print("<head>")
    print("<title>Lock Down Build</title>")
    print("</head>")
    print("<body>")


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
    
    #login to MDS
    sid = apifunctions.login(userid, passwd, ip_addr, ip_cma)

    if(debug == 1):
        print("session id : " + sid, end="<br>")

    

    if((preflight_objects_valid(sgshost, sickhost, autodim, spidr, admin_ipaddr, preload_ipaddr1, preload_ipaddr2) == True) and (preflight_groups_locked(ip_addr, sid) == False)):
        print("Pre-Flight Checks Complete", end="<br>")
        ### create objects and groups
        build_group_and_hosts("FXG-SGS", site_name+"-"+site_num+"-SGS", sgshost, "sgs-", ip_addr, sid)
        build_group_and_hosts("SPIDR_Hubs", "SPIDR_Hubs-"+site_name+"-"+site_num, spidr, "spidr-", ip_addr, sid)
        build_group_and_hosts("SSPC-SICK", "SSPC-SICK-"+site_name+"-"+site_num, sickhost, "sick-", ip_addr, sid)
        build_group_and_hosts("SSPC-Autodim", "SSPC-Autodim-"+site_name+"-"+site_num, autodim, "autodim-", ip_addr, sid)
        
        apifunctions.add_a_host_with_group(ip_addr, admin_name, admin_ipaddr, "Local-ISS-Admin-Server", sid)
        apifunctions.add_a_host_with_group(ip_addr, preload_name1, preload_ipaddr1, "Local-Preload-Assist", sid)
        apifunctions.add_a_host_with_group(ip_addr, preload_name2, preload_ipaddr2, "Local-Preload-Assist", sid)

        ### create rules ... yea ... crazy huh

        ### Section Header : SGS
        add_sgs_rule1 = {
            "layer" : "HubLab Network",
            "position" : {
                "bottom" : "SGS"
            },
            "name" : "SGSCatch1" + site_name,
            "destination" : site_name+"-"+site_num+"-SGS",
            "action" : "Accept",
            "track" : "Log",
            "install-on" : "fw-fxg-hubs"
        }

        add_sgs_rule2 = {
            "layer" : "HubLab Network",
            "position" : {
                "bottom" : "SGS"
            },
            "name" : "SGSCatch2" + site_name,
            "source" : site_name+"-"+site_num+"-SGS",
            "action" : "Accept",
            "track" : "Log",
            "install-on" : "fw-fxg-hubs"
        }

        sgs_rule1_result = apifunctions.api_call(ip_addr, "add-access-rule", add_sgs_rule1, sid)
        sgs_rule2_result = apifunctions.api_call(ip_addr, "add-access-rule", add_sgs_rule2, sid)

        ### Section Header : ISS
        add_iss_rule1 = {
            "layer" : "HubLab Network",
            "position" : {
                "bottom" : "ISS"
            },
            "name" : "ISSCatch1" + site_name,
            "destination" : site_name+"-"+site_num+"-ISS",
            "action" : "Accept",
            "track" : "Log",
            "install-on" : "fw-fxg-hubs"
        }

        add_iss_rule2 = {
            "layer" : "HubLab Network",
            "position" : {
                "bottom" : "ISS"
            },
            "name" : "ISSCatch2" + site_name,
            "source" : site_name+"-"+site_num+"-ISS",
            "action" : "Accept",
            "track" : "Log",
            "install-on" : "fw-fxg-hubs"
        }

        iss_rule1_result = apifunctions.api_call(ip_addr, "add-access-rule", add_iss_rule1, sid)
        iss_rule2_result = apifunctions.api_call(ip_addr, "add-access-rule", add_iss_rule2, sid)

        if(debug == 1):
            print("<br>Rule Add Debug<br>")
            print(json.dumps(sgs_rule1_result), end="<br>")
            print(json.dumps(sgs_rule2_result), end="<br>")
            print(json.dumps(iss_rule1_result), end="<br>")
            print(json.dumps(iss_rule2_result), end="<br>")

    else:
        print("<h1>STOP postoji pogreška</h1>", end="<br>")

    ### Logout Info
    print("Start of Publish ... zzzzzz", end="<br>")
    time.sleep(5)
    publish_result = apifunctions.api_call(ip_addr, "publish", {}, sid)
    print("Publish Result : " + json.dumps(publish_result), end="<br>")

    time.sleep(20)

    logout_result = apifunctions.api_call(ip_addr, "logout", {}, sid)
    print(logout_result, end="<br>")

    print("------- end of program -------", end="<br>")
    print("<br><br>")
    print("</body>")
    print("</html>")
#end of main

if __name__ == "__main__":
    main()
#end of program