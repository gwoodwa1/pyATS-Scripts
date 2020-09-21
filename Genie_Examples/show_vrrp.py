from ttp import ttp
import pprint
from genie.conf import Genie
from genie.testbed import load


ttp_template = """
<template name="vrrp" results="per_template">

<group name="{{ interface }}.Group-{{ VRRP_Group }}">
{{ interface }} - Group {{ VRRP_Group | DIGIT }}
  State is {{ VRRP_State | contains("Master") | let("VRRP Master for this Group") }}
  State is {{ VRRP_State | contains("Init") | let("VRRP Slave for this Group") }}
  Virtual IP address is {{ VRRP_Virtual_IP | IP }}
  Virtual MAC address is {{ VRRP_MAC | MAC }}
  Advertisement interval is {{ adv_interval }} sec
  Preemption {{ VRRP_Preempt }}
  Priority is {{ VRRP_Priority }}
  VRRS Group name {{ Group_Name }}
    Track object {{ track_obj }} state {{ track_obj_status }} decrement {{ track_obj_decrement }}
  Authentication text {{ Auth_Text }}
  Master Router is {{ Master_IP }} (local), priority is {{ priority }}
  Master Router is {{ Master_IP }}, priority is {{ priority }}
  Master Advertisement interval is {{ master_int }} sec
  Master Down interval is {{ master_down }} sec
</group>
</template>
"""

# Create a testbed object for the network
testbed = Genie.init("./testbed_iosxe.yml")




for device in testbed.devices:
    # Connect to the device
    testbed.devices[device].connect()
    # Run the "show vrrp" command on the device
    output = testbed.devices[device].execute('show vrrp')
    output = output.replace('\r\n','\n')
    parser = ttp(template=ttp_template)
    parser.add_input(output, template_name="vrrp")
    parser.parse()
    res = parser.result(structure="dictionary")
    pprint.pprint(res, width=100)
