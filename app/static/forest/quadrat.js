$.fn.additem=function(){
	$('#pnl-form').attr('style','');
	$('#pnl-form #number').val(null);
	$('#pnl-form #plot').val('-1');
}

$.fn.delitem=function(){
	var row=$(this).parent().parent();
	var plot=row.find('#plot').text();
	var number=row.find('#number').text();
	$('.modal-body #del-message').text('确认删除样地 <'+plot+'> 的'+number+'号样方及其所有数据？');
	$('.modal-body #del-id').text($(this).attr('data-whatever'));
}

$(document).ready(function(){
	$('.error-info').parent().parent().parent().parent().attr('style','');
	$('#btn-add').click(function(){
		$('#btn-add').additem();
	});
	$('.del').click(function(){
		$(this).delitem();
	});
	$('#btn-cancel').click(function(){
		$('#pnl-form').attr('style','display:none;');
	});
	$('#del-confirm').click(function(){
		var id=$('.modal-body #del-id').text();
		$.post('delquadrat',{
			id:id
		},
		function(result){
			if(result=='fail')
			{
			}
			else
			{
				$('#quadrats').text("");
				$('#quadrats').append(result);
				$('#btn-add').click(function(){
					$('#btn-add').additem();
				});
				$('.del').click(function(){
					$(this).delitem();
				});
			}
		});	
	});
});
