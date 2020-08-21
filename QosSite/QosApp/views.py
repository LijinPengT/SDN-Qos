import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from .models import Table, Meter

from .odl import add_flow, flow_delete, add_meter, meter_delete

# Create your views here.

def Index(request):
    context = {}
    tables = Table.objects.all().order_by('priority')
    meters = Meter.objects.all()
    context = {
    	'table': tables,
		'meters': meters,
    }
    return render(request, 'index.html',context)

def CreateFlow(request):
    if(request.method == 'POST'):
		rec_data = json.loads(request.body)
		print(rec_data)
		flow_info = {
			'switch_id': rec_data.get('switch_id'),
			'name': rec_data.get('name'),
			'priority': rec_data.get('priority'),
		}
		match = {
			'in_port': rec_data.get('in_port'),
			'ethernet': rec_data.get('ethernet'),
			'ip_source': rec_data.get('ip_source'),
			'ip_dest': rec_data.get('ip_dest'),
			'layer4_match': rec_data.get('layer4_match'),
			'source_port': rec_data.get('source_port'),
			'dest_port': rec_data.get('dest_port'),
		}
		action = {
			'action': rec_data.get('action'),
			'meter_id': rec_data.get('meter_id'),
			'out_port': rec_data.get('out_port'),
		}
		can_add = add_flow(flow_info, match, action)
		res = {}
		print(can_add['result'])
		if(can_add['result'] == 'add success'):
			res['result']= 'success'
		else:
			res['result'] = 'failed'
		return JsonResponse(res)
    else:
		return render(request, 'index.html', {})


def CreateMeter(request):
    if(request.method == 'POST'):
		req_data = json.loads(request.body)
		print(req_data)
		meter = {
			'meter_id': req_data.get('meter_id'),
			'meter_type': req_data.get('meter_type'),
			'band_rate': req_data.get('band_rate'),
			'band_size': req_data.get('band_size'),
		}
		print(meter)
		can_add = add_meter(meter)
		print(can_add['result'])
		res = {}
		if(can_add['result'] == 'add success'):
			res['result'] = 'success'
		else:
			res['result'] = 'failed'
		return JsonResponse(res)
    else:
		return render(request, 'index.html', {})


def DelFlow(request):
    if(request.method=='POST'):
		res_data = json.loads(request.body)
		print(res_data)
		for port in res_data:
			print('delete ID: ', port)
			flow = Table.objects.filter(inport=port)
			flow.delete()
			del_res = flow_delete(port)
			if(del_res['result'] == 'success'):
				res = {'result': 'success'}
			else:
				res['result'] = 'failed'
			return JsonResponse(res)
    else:
		return render(request, 'index.html', {})

def DelMeter(request):
    if(request.method == 'POST'):
		req_data = request.body
		print(req_data)
		res_list = []
		for meter_id in req_data:
			meter = Meter.objects.filter(meter=meter_id)
			meter.delete()
			del_res = meter_delete(meter_id)
			res_list.append(del_res['result'])
		print(res_list)
		res = {'result': 'success'}
		return JsonResponse(res)
    else:
		return render(request, 'index.html', {})


