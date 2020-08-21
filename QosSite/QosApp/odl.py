#coding:utf-8

import json
import base64
import httplib

from .models import Table, Meter


switch_id = 'openflow:178839866559053'

def pre_get():
    try:
        url = "/restconf/operational/network-topology:network-topology/topology/flow:1"
        auth = base64.b64encode('admin' + ':' + 'admin')
        headers = {"Authorization": "Basic " + auth, "Content-Type": "application/json"}
        conn = httplib.HTTPConnection('127.0.0.1:8181', timeout=3)
        conn.request(method="GET", url=url, headers=headers)
        response = conn.getresponse()
        ret = response.read()
        return {"status": 1, "data": ret}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": 0}


def pre_put(url, body):
    try:
        auth = base64.b64encode('admin:admin'.encode())
        headers = {"Authorization": "Basic " + auth, "Content-Type": "application/json"}
        conn = httplib.HTTPConnection('127.0.0.1:8181', timeout=3)    
        conn.request("PUT", url, body, headers)
        response = conn.getresponse()
        
        if response.status in [200,201]:
            return {'result': 'add success'}
        else:
            return {'result': 'add failure'}
   
    except Exception as e:
        import traceback
        traceback.print_exc()


def flow_delete(in_port):

    url_in = "/restconf/config/opendaylight-inventory:nodes/node/" + switch_id + "/flow-node-inventory:table/0/flow/" + in_port
    auth = base64.b64encode('admin:admin'.encode())
    headers = {"Authorization": "Basic " + auth, "Content-Type": "application/json"}

    conn = httplib.HTTPConnection('127.0.0.1:8181', timeout=3)
    try:
        conn.request("DELETE", url_in, json.dumps({}), headers)
	    return {'result': 'success'}
    except:
        import traceback
        traceback.print_exc()
	    return {'result': 'failed'}

def meter_delete(meter_id):
    url_in = "/restconf/config/opendaylight-inventory:nodes/node/" + switch_id + "/meter/" + meter_id
    auth = base64.b64encode('admin:admin'.encode())
    headers = {'Authorization': "Basic " + auth, "Content-Type": "application/json"}
    conn = httplib.HTTPConnection('127.0.0.1:8181', timeout=3)
    try:
        conn.request('DELETE', url_in, json.dumps({}), headers)
        return {'result': 'success'}
    except:
        import traceback
        traceback.print_exc()
        return {'result': 'failed'}

def add_flow(flow_info, match, action):
    name = flow_info['name']
    priority = flow_info['priority']
    in_port = match['in_port']
    url = "/restconf/config/opendaylight-inventory:nodes/node/" + switch_id + "/flow-node-inventory:table/0/flow/" + in_port
    flow_set = {
        'id': in_port,
        'flow-name': name,
        'table_id': 0,
        'priority': priority,
    }

    #match
    match_set = {
        "ethernet-match": {
            "ethernet-type":{"type": match['ethernet']}
        },
        "ipv4-source": match['ip_source'],
        "ipv4-destination": match['ip_dest'],
        "ip-match": {"ip-protocol": 6},
        "tcp-destination-port": match["dest_port"],
    }

    #action
    action_set = {
       'order': '1',
        'output-action':{
            "output-node-connector": switch_id +':' + action['out_port'],
            "max-length": 65535,
    	}
    }

    instruc_set = {
        "instruction": [{
	    'order': '0',
	    'meter': {'meter-id': action['meter_id']}	
	    },{
            "order": '1',
            "apply-actions": {
                "action": [action_set]
            }
        }]
    }

    flow_set['match'] = match_set
    flow_set['instructions'] = instruc_set
    table = Table(flow=name, flow_node=switch_id, priority=priority, inport=in_port, match=match_set, instruction=instruc_set)
    body = json.dumps({"flow":flow_set})
    res = pre_put(url, body)
    if(res['result'] == 'add success'):
	    table.save()
    return res


def add_meter(meter):
    meter_id = meter['meter_id']
    meter_type = meter['meter_type']
    band_rate = meter['band_rate']
    band_size = meter['band_size']
    url = '/restconf/config/opendaylight-inventory:nodes/node/' + switch_id + '/meter/' + meter_id
    
    meter_set = {
	"meter-id": meter_id,
	"meter-band-headers": {
	    "meter-band-header": {
	    	"band-id": '0',
		"meter-band-types": {"flags": meter_type},
		"drop-burst-size": band_size,
		"drop-rate": band_rate
	    }
	},
	"meter-name": "guestMeter",
	"container-name": "guestMeterContainer",
	"flags": "meter-kbps"
    }
    meter = Meter(meter=meter_id, meterType=meter_type, bandRate=band_rate, bandSize=band_size)
    body = json.dumps({"meter": meter_set})
    res = pre_put(url, body)
    if(res['result'] == 'add success'):
	    meter.save()
    return res


if __name__ == "__main__":
    #add_flow("100")
    meter = {
	'meter_id': "5",
	'meter_type': "ofpmbt-drop",
	'band_size': "1024",
	'band_rate': "256",
    }
   # add_meter(meter)8
