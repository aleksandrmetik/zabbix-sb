#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
__preauthor__ = 'vladimirg'
__preversion__ = '1.2'

__author__ = 'aleksandrmetik'
__version__ = '2.0'

from zabbix_api import ZabbixAPI
import os
import argparse
import datetime

#Define zabbix config file

zbx_conf_file =os.path.dirname(os.path.realpath(__file__)) + '/../conf/zabbix.conf'

# Get zabbix server connect credentials
for tmp_line in open(zbx_conf_file):
    if "server" in tmp_line: zbx_server = str(tmp_line.split("=")[1]).rstrip()
    if "user" in tmp_line: zbx_user = str(tmp_line.split("=")[1]).rstrip()
    if "pass" in tmp_line: zbx_pass = str(tmp_line.split("=")[1]).rstrip()

# Connect to zabbix server
zapi = ZabbixAPI(zbx_server)
zapi.login(zbx_user,zbx_pass)

parser = argparse.ArgumentParser(description='Arguments to web test in zabbix')
parser.add_argument('--url', required=True, action='store', default=None, dest='url', help='Site url. Example: http://test.com')
parser.add_argument('--pattern', required=True, action='store', default=None, dest='pattern', help='Required pattern on site ')
parser.add_argument('-p','--prname',action='store', required=True, default='None', dest='Pr_Name', help='Project namein zabbix ' )
parser.add_argument('--desc', required=True, action='store', default=None, dest='desc', help='Desc about this web test')
parser.add_argument('--delay', required=True, action='store', default=None, dest='delay', help='Delay of checks, examples 20s, 1m, 5m and etc')
parser.add_argument('--httpcode', required=True, action='store', default=200, dest='httpcode', help='Expected http code')
parser.add_argument('--followredirect', required=True, action='store', default=1, dest='followredirect', help='Is folowing redirects? 1 or 0')
parser.add_argument('--timeout', required=True, action='store', default=30, dest='timeout', help='Timeout, default is 30 sec')


args =  parser.parse_args()

url = args.url
pattern = args.pattern
desc = args.desc
pr_name = args.Pr_Name
name = url[:40]
delay = args.delay
httpcode = args.httpcode
followredirect = args.followredirect
timeout= args.timeout

zbx_host_get = zapi.host.get(
    {
        # "output": "extend",
        "search":
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


if zbx_host_get:

        result = zapi.httptest.get({
                                "filter": { "name":["check content " +  name]},
                                "output": "extend",
                                "hostid": zbx_host_get[0]['hostid']

                            }
                        )


        if result:
                print("Web test  already exist!")
                exit (0)




result = zapi.httptest.create({
                                "name": "check content " +  name,
                                "hostid": zbx_host_get[0]['hostid'],
                                "variables":'',
                               # "headers":'',
                                "delay": delay,
                                "steps": [
                                    {
                                        "name": "Base",
                                        "url": url,
                                        "status_codes": httpcode,
					"follow_redirects" : followredirect,
                                     #   "headers":'',
                                      #   "posts":'',
                                      #  "variables":'',
                                        "timeout": timeout,
                                       "required": pattern,
                                        "no": 1
                                    }
                                ]
                            }
                        )

result = zapi.trigger.create (
    {
        "description":"Attention! Check content " + name +" failed!",
        "expression":"{content_check." + pr_name + ":web.test.fail[check content " + name + "].count(#3,0,\"ne\")}=3 and {content_check." + pr_name + ":web.test.error[check content " + name + "].str(000000000000)}=0",
        "priority": 5,
        "comments" : desc,
        "url": url


    }

)

print ("Web check successful create: [Ok]")

