#!/usr/bin/python3

DOCUMENTATION = r'''
---

description: 
    This custom filter plugin is to construct a list of host vars from csv user data dynamically. It has 'unique_id' and 
    "hostvars' elements in it. hostvars is a dictionary that has host vars. The final output looks like:
                {
                    "unique_id": "1",
                    "hostvars": {
                        "zone": "global",
                        "path": "/demo/jw_demo_299",
                        "hard": "20000",
                        "description": "chg00299",
                        "share_name": "jw_demo_299",
                        "app_name": "demo_299",
                        "endpoint_host": "10.34.225.6"
                    }
                },
                {
                    "unique_id": "2",
                    "hostvars": {
                        "zone": "global",
                        "path": "/demo/jw_demo_300",
                        "hard": "20000",
                        "description": "chg00300",
                        "share_name": "jw_demo_300",
                        "app_name": "demo_300",
                        "endpoint_host": "10.34.225.6"
                    }
                }

author:
    - Jingwei.Zhang@dell.com
'''
EXAMPLES = r'''
- set_fact:
        test_data: "{{ csv_user_data | dynamic_hostvars }}"

'''

import logging
import json
import sys
import os

class FilterModule(object):
    # required class method 
    def filters(self):
      return {'dynamic_hostvars': self.dynamic_hostvars}

    # main method that creates dynamic hostvars list
    def dynamic_hostvars(self, csv_user_data):
        logging.basicConfig(filename=os.path.splitext(os.path.basename(__file__))[0] + '.log', level=logging.DEBUG)
        logging.debug("++++++ csv_user_data: " + json.dumps(csv_user_data, indent=2))

        dynamic_hostvars = []   # empty list 
        for i in range(len(csv_user_data)):         
            csv_user_data_item = csv_user_data[i]
            dynamic_hostvars_item = {} # dynamic hostvars item is a dict 

            # create dynamic hostvars dict
            dynamic_hostvars_item['unique_id'] = csv_user_data_item['unique_id']

            # remove host_name from csv_user_data and add to dynamic hostvars item
            csv_user_data_item.pop('unique_id')
            dynamic_hostvars_item['hostvars'] = csv_user_data_item

            # add dynamic hostvats item to list
            dynamic_hostvars.append(dynamic_hostvars_item)
        # end of for loop

        logging.debug("++++++ dynamic_hostvars: " + json.dumps(dynamic_hostvars, indent=2))

        return dynamic_hostvars
        