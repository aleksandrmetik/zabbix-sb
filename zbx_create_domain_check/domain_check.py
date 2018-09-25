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

#Connect to server

zapi = ZabbixAPI(zbx_server)
zapi.login(zbx_user,zbx_pass)

parser = argparse.ArgumentParser(description='Arguments to add domain expier check')
parser.add_argument('-p','--prname',action='store', required=True, default='None', dest='Pr_Name', help='Project name in zabbix ' )
parser.add_argument('-d', '--domain', dest='domainName', action='store',required=True, default=None,  help='Domain name to monitor')
args =  parser.parse_args()



domainName =  args.domainName
pr_name = args.Pr_Name





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
                    "name": "domain expiration " + domainName
                }
        }

)


if not zbx_item:
    zbx_item = zapi.item.create(
        {
            "name": "domain expiration " + domainName,
            "key_": "domain_exp[" + domainName + "]",
            "hostid": zbx_host_get[0]['hostid'],
            "interfaceid":zbx_interface[0]['interfaceid'],
            "type": 0,
            "value_type": 3,
            "delay": 30

        }
    )
    print ("Items create: [OK]")

    if zbx_item:
        zab_trigger = zapi.trigger.create (
            {
                "description": "domain expiration " + domainName,
                "expression":"{content_check." + pr_name + ":domain_exp[" + domainName + "].last()}=20 or {content_check." + pr_name + ":domain_exp["+ domainName + "].last()}=3",
                "url": "http://" + domainName,
		"comments":"",
                "priority":"4"
            }
        )
        print ("Trigger create: [OK]")
else:
    print ("Already exist!")

