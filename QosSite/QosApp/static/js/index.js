// 检查action的值
function checkAction(action){
    if(action == 'drop'){
        $('#out_port').css("display", "none");
    }else {
        $('#out_port').css("display", "");
    }
}

// 给action select添加change事件
$('#action').change(function (e) { 
    e.preventDefault();
    let action = $('#action').val();
    checkAction(action);
});

// 序列化表单数据，生成json格式的数据
$('#add_flow').click(function (e) {
    e.preventDefault();
    let data = {};
    let value = $('#addFlow').serializeArray();
    $.each(value, function (index, item) {
                data[item.name] = item.value;
            });
    let json = JSON.stringify(data);
    console.log('json : ',json);
    $.ajax({
    	type: "POST",
        url: "add-flow/",
        'Content-Type': 'application/json',
        datatype: 'json',
        data: json,
        success: function(data){
            if(data.result == "success"){
                alert('AddFLow success!');
            location.reload();
            }else{
                alert('AddFlow Failed!');
            }
        }
    });    
});

var items = [];
$('#del_flow').click(function(e){
    e.preventDefault();
    items.splice(0,items.length);
    $("input[type='checkbox'][name='in_port']").each(function(){
    	if($(this).is(":checked")){
	    items.push($(this).val());
	}
    });
    console.log('items:', items);
    $.ajax({
        type: "POST",
        url: "del-flow/",
        'Content-Type': 'application/json',
        datatype: 'json',
        data: JSON.stringify(items),
        success: function(data){
            if(data.result == 'success'){
                alert('DeleteFlow success!');
            location.reload();
            }else{
                alert('DeleteFlow Failed!');
            }
        }
    });
});

// add-meter
$('#add_meter').click(function(e){
    e.preventDefault();
    let data = {}
    let value = $('#addMeter').serializeArray();
    $.each(value, function(index, item){
    	data[item.name] = item.value;
    });
    let json = JSON.stringify(data);
    console.log('JSON: ', json);
    $.ajax({
        type: "POST",
        url: "add-meter/",
        'Content-Type': 'application/json',
        datatype: 'json',
        data: json,
        success: function(data){
            if(data.result == 'success'){
                alert('AddMeter success!');
		        location.reload();
            }else{
                alert('AddMeter Failed!');
            }
        }

    });
});

//delete-meter
var meters = [];
$('#del_meter').click(function(e){
    e.preventDefault();
    meters.splice(0, meters.length);
    $("input[type='checkbox'][name='meter_id']").each(function(){
        if($(this).is(":checked")){
            meters.push($(this).val());
        }
    });
    console.log(meters);
    $.ajax({
        type: "POST",
        url: "del-meter/",
        'Content-Type': 'application/json',
        datatype: 'json',
        data: JSON.stringify(meters),
        success: function(data){
            if(data.result == 'success'){
                alert('DeleteMeter success!');
		        location.reload();
            }else{
                alert('DeleteMeter Failed!');
            }
        }
    });
});
