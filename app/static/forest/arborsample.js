$.fn.additem=function(){
	var timestamp=$.trim($('#dropdownMenu1').text());
	$('#pnl-form').attr('style','');
	$('#pnl-form #id').val('0');
	$('#pnl-form #timestamp').val(timestamp);
	$('#pnl-form #arbor').val('-1');
	$('#pnl-form #canopyside1').val(null);
	$('#pnl-form #canopyside2').val(null);
	$('#pnl-form #height').val(null);
	$('#pnl-form #diameter').val(null);
	$('#pnl-form #note').val(null);
	$('#pnl-form .panel-heading').text('添加数据');
	$('#pnl-form #timestamp').removeAttr('readonly');
	$('#pnl-form #arbor').removeAttr('readonly');
}

$.fn.edititem=function(){
	$('#pnl-form').attr('style','');
	var row=$(this).parent().parent();
	var arborid=row.find('#arborid').text();
	var timestamp=$.trim($('#dropdownMenu1').text());
	var canopyside1=row.find('#canopyside1').text();
	var canopyside2=row.find('#canopyside2').text();
	var diameter=row.find('#diameter').text();
	var height=row.find('#height').text();
	var note=row.find('#note').text();
	$('#pnl-form #id').val('1');
	$('#pnl-form #timestamp').val(timestamp);
	$('#pnl-form #arbor').val(arborid);
	$('#pnl-form #canopyside1').val(canopyside1);
	$('#pnl-form #canopyside2').val(canopyside2);
	$('#pnl-form #diameter').val(diameter);
	$('#pnl-form #height').val(height);
	$('#pnl-form #note').val(note);
	$('#pnl-form .panel-heading').text('编辑数据');
	$('#pnl-form #timestamp').attr('readonly','readonly');
	$('#pnl-form #arbor').attr('readonly','readonly');
}

$.fn.delitem=function(){
	$('.modal-body #del-message').text('确认删除当前调研时间段树木 <编号：'+$(this).attr('data-whatever')+'> 数据？');
	var row=$(this).parent().parent();
	var del_id=row.find('#id').text();
	$('.modal-body #del-id').text(del_id);
}

$.fn.checkerror=function(){
	$(this).attr('style','');
	if($(this).find('#id').val()=='0'){
		$(this).find('.panel-heading').text('添加数据');
	}else{
		$(this).find('.panel-heading').text('编辑数据');
		$('#pnl-form #timestamp').attr('readonly','readonly');
		$('#pnl-form #arbor').attr('readonly','readonly');
	}
}

$(document).ready(function(){
	$('.error-info').parent().parent().parent().parent().checkerror();
	$('#btn-add').click(function(){
		$('#btn-add').additem();
	});
	$('.del').click(function(){
		$(this).delitem();
	});
	$('.edit').click(function(){
		$(this).edititem();
	});
	$('#btn-cancel').click(function(){
		$('#pnl-form').attr('style','display:none;');
	});
	$('#del-confirm').click(function(){
		var delid=$('.modal-body #del-id').text();
		$.post('delarborsample',{
			id:delid
		},
		function(result){
			if(result=='fail')
			{
			}
			else
			{
				$('#arborsamples').text("");
				$('#arborsamples').append(result);
				$('#btn-add').click(function(){
					$('#btn-add').additem();
				});
				$('.del').click(function(){
					$(this).delitem();
				});
				$('.edit').click(function(){
					$(this).edititem();
				});
			}
		});	
	});
});
