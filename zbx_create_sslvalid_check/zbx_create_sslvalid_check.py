#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
__author__ = 'vladimirg'
__version__ = '3.0'

import argparse
import os
from zabbix_api import ZabbixAPI

#Define zabbix config file

zbx_conf_file =os.path.dirname(os.path.realpath(__file__)) + '/../conf/zabbix.conf'

# Get zabbix server connect credentials
for tmp_line in open(zbx_conf_file):
    if "server" in tmp_line: zbx_server = str(tmp_line.split("=")[1]).rstrip()
    if "user" in tmp_line: zbx_user = str(tmp_line.split("=")[1]).rstrip()
    if "pass" in tmp_line: zbx_pass = str(tmp_line.split("=")[1]).rstrip()

# Connect to server
zapi = ZabbixAPI(zbx_server)
zapi.login(zbx_user,zbx_pass)


parser = argparse.ArgumentParser(description='Arguments to add domain expier check')
parser.add_argument('--prname', action='store', required=True, default='None',  dest='Projectname', help='Projec name in zabbix')
parser.add_argument('--domain', dest='domainName', action='store',required=True, default=None,  help='Domain name to monitor')
parser.add_argument('--delay', dest='delay', action='store',required=True, default='1d',  help='Execution intervalof the checks. Accepts seconds, time unit with suffix. Example 5s, 1m, 1d and etc ')

args =  parser.parse_args()


pr_name = args.Projectname
domainName =  args.domainName
delay =  args.delay

zbx_host_get = zapi.host.get(
    {
        # "output": "extend",
        "filter":
            {
                "host": "content_check." + pr_name
            }
    }

)

if not zbx_host_get:
        print ("Special host dose not exist")
        exit (0)
else:
        zbx_interface = zapi.hostinterface.get ({"hostids":zbx_host_get[0]['hostid']})


zbx_item = zapi.item.get (
     {
            "output": "extend",
            "hostids": zbx_host_get[0]['hostid'],
            "filter":
                {
                    "name": "ssl expiration " + domainName
                }
        }

)


if not zbx_item:
    zbx_item = zapi.item.create(
        {
            "name": "ssl expiration " + domainName,
            "key_": "ssl_exp[" + domainName + "]",
            "hostid": zbx_host_get[0]['hostid'],
            "interfaceid":zbx_interface[0]['interfaceid'],
            "type": 0,
            "value_type": 3,
            "delay": delay

        }
    )
    print ("Items create: [OK]")

    if zbx_item:
        zab_trigger = zapi.trigger.create (
            {
                "description": "SSL certificate for " + domainName + " expires in 20 days",
                "expression":"{content_check." + pr_name + ":ssl_exp[" + domainName + "].last()}=20",
                "comments":"",
                "url": "https://" + domainName,
                "priority":"3"
            }
        )
        zab_trigger = zapi.trigger.create (
            {
                "description": "SSL certificate for " + domainName + " expires in 5 days",
                "expression":"{content_check." + pr_name + ":ssl_exp[" + domainName + "].last()}=5",
                "comments":"",
                "url": "https://" + domainName,
                "priority":"4"
            }
        )
        zab_trigger = zapi.trigger.create (
            {
                "description": "SSL certificate for " + domainName + " expires in 3 days",
                "expression":"{content_check." + pr_name + ":ssl_exp[" + domainName + "].last()}=3",
                "comments":"",
                "url": "https://" + domainName,
                "priority":"5"
            }
        )
        print ("Trigger create: [OK]")
else:
    print ("Already exist!")
