$.fn.adddata=function(){
	$('#addModal').find('#rivername').val('');
}

$.fn.editdata=function(){
	var row=$(this).parent().parent();
	var id=row.find('#watershedid').text();
	var rivername=row.find('#rivername').text()
	$('#editModal').find('#watershedid').text(id);
	$('#editModal').find('#rivername').val(rivername);
	$('#editModal').find('#oldname').text(rivername);
}

$.fn.deldata=function(){
	var row=$(this).parent().parent();
	var id=row.find('#watershedid').text();
	var rivername=row.find('#rivername').text()
	$('#delModal').find('#watershedid').text(id);
	$('#delModal').find('#rivername').text(rivername);
}

$(document).ready(function(){
	$('#menu-water').attr('class','dropdown active');
	$('#btn-add').click(function(){	$(this).adddata(); });
	$('.del').click(function(){ $(this).deldata(); });
	$('.edit').click(function(){ $(this).editdata(); });

	$('#add-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var rivername=$('#addModal').find('#rivername').val();
		$.post('addwatershed',{
			rivername:rivername
		},
		function(result){
			if(result=='fail1')
			{
				$('#alert').text("流域 <"+rivername+"> 已存在，添加失败！");	
				$('#alert').attr('class','alert alert-warning');
				$('#alert').attr('style','');
			}
			else if(result=='fail')
			{
				$('#alert').text("添加失败！");	
				$('#alert').attr('class','alert alert-warning');
				$('#alert').attr('style','');
			}
			else
			{
				$('#datas').text("");
				$('#datas').append(result);
				$('#btn-add').click(function(){	$(this).adddata(); });
				$('.del').click(function(){ $(this).deldata(); });
				$('.edit').click(function(){ $(this).editdata(); });
				$('#alert').text("流域 <"+rivername+"> 添加成功");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});

	$('#edit-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var watershedid=$('#editModal').find('#watershedid').text();
		var rivername=$('#editModal').find('#rivername').val();
		$.post('editwatershed',{
			watershedid:watershedid,
			rivername:rivername
		},
		function(result){
			if(result=='fail1')
			{
				$('#alert').text("流域名称 <"+rivername+"> 已存在，修改失败！");	
				$('#alert').attr('class','alert alert-warning');
				$('#alert').attr('style','');
			}
			else if(result=='fail2')
			{
				$('#alert').text("找不到指定的流域项，修改失败！");	
				$('#alert').attr('class','alert alert-warning');
				$('#alert').attr('style','');
			}
			else if(result=='fail')
			{
				$('#alert').text("修改失败！");	
				$('#alert').attr('class','alert alert-warning');
				$('#alert').attr('style','');
			}
			else
			{
				$('#datas').text("");
				$('#datas').append(result);
				$('#btn-add').click(function(){	$(this).adddata(); });
				$('.del').click(function(){ $(this).deldata(); });
				$('.edit').click(function(){ $(this).editdata(); });
				$('#alert').text("流域 <"+rivername+"> 名称修改成功");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});

	$('#del-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var watershedid=$('#delModal').find('#watershedid').text();
		$.post('delwatershed',{
			watershedid:watershedid
		},
		function(result){
			if(result=='fail1')
			{
				$('#alert').text("找不到指定的流域项，删除失败！");	
				$('#alert').attr('class','alert alert-warning');
				$('#alert').attr('style','');
			}
			else if(result=='fail')
			{
				$('#alert').text("删除失败！");	
				$('#alert').attr('class','alert alert-warning');
				$('#alert').attr('style','');
			}
			else
			{
				$('#datas').text("");
				$('#datas').append(result);
				$('#btn-add').click(function(){	$(this).adddata(); });
				$('.del').click(function(){ $(this).deldata(); });
				$('.edit').click(function(){ $(this).editdata(); });
				var rivername=$('#delModal').find('#rivername').val();
				$('#alert').text("流域 <"+rivername+"> 及其所有调查数据删除成功");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});
});
