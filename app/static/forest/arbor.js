$.fn.addarbor=function(){
	$('#pnl-form').attr('style','');
	$('#pnl-form #id').val('0');
	$('#pnl-form #number').val(null);
	$('#pnl-form #chnname').val('-1');
	$('#pnl-form .panel-heading').text('添加树种');
}

$.fn.editarbor=function(){
	$('#pnl-form').attr('style','');
	var row=$(this).parent().parent();
	var number=row.find('#number').text();
	var chnname=row.find('#typeid').text();
	$('#pnl-form #id').val('1');
	$('#pnl-form #number').val(number);
	$('#pnl-form #chnname').val(chnname);
	$('#pnl-form .panel-heading').text('编辑树种数据');
}

$.fn.delarbor=function(){
	$('.modal-body #del-message').text('确认删除树木 <编号：'+$(this).attr('data-whatever')+'> 及其所有数据？');
	var row=$(this).parent().parent();
	var number=row.find('#number').text();
	$('.modal-body #del-number').text(number);
}

$.fn.checkerror=function(){
	$(this).attr('style','');
	if($(this).find('#id').val()=='0'){
		$(this).find('.panel-heading').text('添加树种');
	}else{
		$(this).find('.panel-heading').text('编辑树种数据');
	}
}
	
$(document).ready(function(){
	$('#menu-forest').attr('class','dropdown active');
	$('.error-info').parent().parent().parent().parent().checkerror();
	$('#btn-add').click(function(){
		$('#btn-add').addarbor();
	});
	$('.del').click(function(){
		$(this).delarbor();
	});
	$('.edit').click(function(){
		$(this).editarbor();
	});
	$('#btn-cancel').click(function(){
		$('#pnl-form').attr('style','display:none;');
	});
	$('#del-confirm').click(function(){
		var number=$('.modal-body #del-number').text();
		var plotid=$('.modal-body #del-plotid').text();
		$.post('delarbor',{
			number:number,
			plotid:plotid
		},
		function(result){
			if(result=='fail')
			{
			}
			else
			{
				$('#arbors').text("");
				$('#arbors').append(result);
				$('#btn-add').click(function(){
					$('#btn-add').addarbor();
				});
				$('.del').click(function(){
					$(this).delarbor();
				});
				$('.edit').click(function(){
					$(this).editarbor();
				});
			}
		});	
	});
});
