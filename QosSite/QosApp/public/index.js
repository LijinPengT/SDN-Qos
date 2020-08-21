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
    
});




