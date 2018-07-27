$.fn.editdata=function(){
	var row=$(this).parent().parent();
	var rowid=row.find('#rowid').text();
	var typeid=row.find('#typeid').text();
	var typename=row.find('#typename').text();
	var time=row.find('#time').text();
	var selectedplotid=$('#edit-plot option').first().val();
	var value=row.find('#'+selectedplotid).text().replace(/(^\s*)|(\s*$)/g,'');
	$('#editModal').find('#row-id').text(rowid);
	$('#editModal').find('#edit-type').text(typename);
	$('#editModal').find('#edit-type-id').text(typeid);
	$('#editModal').find('#edit-time').text(time);
	$('#editModal').find('#edit-plot').val(selectedplotid);
	$('#editModal').find('#edit-value').val(value);
}

$.fn.deldata=function(){
	var row=$(this).parent().parent();
	var typeid=row.find('#typeid').text();
	var typename=row.find('#typename').text();
	var time=row.find('#time').text();
	$('#delModal').find('#del-type').text(typename);
	$('#delModal').find('#del-type-id').text(typeid);
	$('#delModal').find('#del-time').text(time);
}

$.fn.changeplot=function(){
	var rowid=$(this).parent().parent().find('#row-id').text();
	var selectedplotid=$('#editModal').find('#edit-plot').val();
	var str1='#'+rowid;
	var str2='#'+selectedplotid;
	var value=$(str1).find(str2).text().replace(/(^\s*)|(\s*$)/g,'');
	$('#editModal').find('#edit-value').val(value);
}



$(document).ready(function(){
	$('#menu-air').attr('class','dropdown active');
	$('#pnl-toggle').click(function() {
                $('#editpnl .panel-body').slideToggle("slow");
                datastatus=$(this).attr('data-status');
                if(datastatus=='open'){
                        $(this).attr('src','../static/icons/down.png');
                        $(this).attr('data-status','closed');
                }
                else{
                        $(this).attr('src','../static/icons/up.png');
                        $(this).attr('data-status','open');
                }
        });
        $('#editpnl').find('select').attr('style','width:100%;');
        $('#editpnl').find('select').find('option').attr('style','height:20px;');

	$('.del').click(function(){
		$(this).deldata();
	});
	$('.edit').click(function(){
		$(this).editdata();
	});
	$('#edit-plot').change(function(){
		$(this).changeplot();
	});

	$('#del-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var typeid=$('#delModal').find('#del-type-id').text();
		var time=$('#delModal').find('#del-time').text();
		var plotid=$('#delModal').find('#del-plot').val();
		var plots=[];
		var types=[];
		var times=[];
		$('#query #plots span').each(function(){
			plots.push($(this).text());
		});
		$('#query #types span').each(function(){
			types.push($(this).text());
		});
		$('#query #times span').each(function(){
			times.push($(this).text());
		});
		var plotsjson=JSON.stringify(plots);
		var typesjson=JSON.stringify(types);
		var timesjson=JSON.stringify(times)
		$.post('delvocdata',{
			plotid:plotid,
			time:time,
			typeid:typeid,
			plots:plotsjson,
			types:typesjson,
			times:timesjson
		},
		function(result){
			if(result=='fail')
			{
				$('#alert').text("删除失败！");	
				$('#alert').attr('class','alert alert-warning');
				$('#alert').attr('style','');
			}
			else
			{
				$('#datas').text("");
				$('#datas').append(result);
				$('.del').click(function(){
					$(this).deldata();
				});
				$('.edit').click(function(){
					$(this).editdata();
				});
				var typename=$('#delModal').find('#del-type').text();
				var plotname=$('#delModal').find('#del-plot').find("[value='"+plotid+"']").text();
				$('#alert').text("监测点位点<"+plotname+"> "+time+"的 "+typename+" 指标数据删除成功.");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});

	$('#edit-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var typeid=$('#editModal').find('#edit-type-id').text();
		var time=$('#editModal').find('#edit-time').text();
		var plotid=$('#editModal').find('#edit-plot').val();
		var value=$('#editModal').find('#edit-value').val();
		var plots=[];
		var types=[];
		var times=[];
		$('#query #plots span').each(function(){
			plots.push($(this).text());
		});
		$('#query #types span').each(function(){
			types.push($(this).text());
		});
		$('#query #times span').each(function(){
			times.push($(this).text());
		});
		var plotsjson=JSON.stringify(plots);
		var typesjson=JSON.stringify(types);
		var timesjson=JSON.stringify(times)
		$.post('editvocdata',{
			plotid:plotid,
			time:time,
			typeid:typeid,
			value:value,
			plots:plotsjson,
			times:timesjson,
			types:typesjson
		},
		function(result){
			if(result=='fail')
			{
				$('#alert').text("编辑失败！");	
				$('#alert').attr('class','alert alert-warning');
				$('#alert').attr('style','');
			}
			else
			{
				$('#datas').text("");
				$('#datas').append(result);
				$('.del').click(function(){
					$(this).deldata();
				});
				$('.edit').click(function(){
					$(this).editdata();
				});
				var typename=$('#editModal').find('#edit-type').text();
				var plotname=$('#editModal').find('#edit-plot').find("[value='"+plotid+"']").text();
				$('#alert').text("监测点位 <"+plotname+"> "+time+"的 "+typename+" 指标数据编辑成功.");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});

});

