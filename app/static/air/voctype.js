$.fn.editdata=function(){
	var row=$(this).parent().parent();
	var typeid=row.find('#typeid').text();
	var typename=row.find('#typename').text();
	$('#editModal').find('#typeid').text(typeid);
	$('#editModal').find('#typename').val(typename);
}

$.fn.deldata=function(){
	var row=$(this).parent().parent();
	var typeid=row.find('#typeid').text();
	var typename=row.find('#typename').text();
	$('#delModal').find('#typeid').text(typeid);
	$('#delModal').find('#typename').text(typename);
}
$(document).ready(function(){
	$('#menu-air').attr('class','dropdown active');
	$('.del').click(function(){
		$(this).deldata();
	});
	$('.edit').click(function(){
		$(this).editdata();
	});
	
	$('#del-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var typeid=$('#delModal').find('#typeid').text();
		$.post('delvoctype',{
			typeid:typeid
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
				$('#voctypes').text("");
				$('#voctypes').append(result);
				$('.del').click(function(){
					$(this).deldata();
				});
				$('.edit').click(function(){
					$(this).editdata();
				});
				var typename=$('#delModal').find('#typename').text();
				$('#alert').text("挥发性有机物指标 <"+typename+"> 及其所有数据删除成功.");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});

	$('#edit-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var typeid=$('#editModal').find('#typeid').text();
		var typename=$('#editModal').find('#typename').val();
		$.post('editvoctype',{
			typeid:typeid,
			typename:typename
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
				$('#voctypes').text("");
				$('#voctypes').append(result);
				$('.del').click(function(){
					$(this).deldata();
				});
				$('.edit').click(function(){
					$(this).editdata();
				});
				$('#alert').text("挥发性有机物指标 <"+typename+"> 名称修改成功.");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});
});
