$.fn.adddata=function(){
	$('#addModal').find('#plotname').val('');
}

$.fn.editdata=function(){
	var row=$(this).parent().parent();
	var id=row.find('#plotid').text();
	var plotname=row.find('#plotname').text();
	var rivername=row.find('#rivername').text()
	var londegree=row.find('#londegree').text();
	var lonminute=row.find('#lonminute').text();
	var lonsecond=row.find('#lonsecond').text();
	var latdegree=row.find('#latdegree').text();
	var latminute=row.find('#latminute').text();
	var latsecond=row.find('#latsecond').text();
	$('#editModal').find('#plotid').text(id);
	$('#editModal').find('#rivername').text(rivername);
	$('#editModal').find('#oldname').text(plotname);
	$('#editModal').find('#plotname').val(plotname);
	$('#editModal').find('#londegree').val(londegree);
	$('#editModal').find('#lonminute').val(lonminute);
	$('#editModal').find('#lonsecond').val(lonsecond);
	$('#editModal').find('#latdegree').val(latdegree);
	$('#editModal').find('#latminute').val(latminute);
	$('#editModal').find('#latsecond').val(latsecond);
}

$.fn.deldata=function(){
	var row=$(this).parent().parent();
	var id=row.find('#plotid').text();
	var plotname=row.find('#plotname').text();
	var rivername=row.find('#rivername').text()
	$('#delModal').find('#plotid').text(id);
	$('#delModal').find('#plotname').text(plotname);
	$('#delModal').find('#rivername').text(rivername);
}

$(document).ready(function(){
	$('#menu-water').attr('class','dropdown active');
	$('#btn-add').click(function(){	$(this).adddata(); });
	$('.del').click(function(){ $(this).deldata(); });
	$('.edit').click(function(){ $(this).editdata(); });

	$('#add-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var plotname=$('#addModal').find('#plotname').val();
		var watershedid=$('#addModal').find('#watershed').val();
		var londegree=$('#addModal').find('#londegree').val();
		var lonminute=$('#addModal').find('#lonminute').val();
		var lonsecond=$('#addModal').find('#lonsecond').val();
		var latdegree=$('#addModal').find('#latdegree').val();
		var latminute=$('#addModal').find('#latminute').val();
		var latsecond=$('#addModal').find('#latsecond').val();
		$.post('addplot',{
			plotname:plotname,
			watershedid:watershedid,
			londegree:londegree,
			lonminute:lonminute,
			lonsecond:lonsecond,
			latdegree:latdegree,
			latminute:latminute,
			latsecond:latsecond
		},
		function(result){
			if(result=='fail1')
			{
				$('#alert').text("监测点名称 <"+plotname+"> 已存在，添加失败！");	
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
				$('#alert').text("水质监测点位 <"+plotname+"> 添加成功");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});

	$('#edit-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var plotid=$('#editModal').find('#plotid').text();
		var plotname=$('#editModal').find('#plotname').val();
		var londegree=$('#editModal').find('#londegree').val();
		var lonminute=$('#editModal').find('#lonminute').val();
		var lonsecond=$('#editModal').find('#lonsecond').val();
		var latdegree=$('#editModal').find('#latdegree').val();
		var latminute=$('#editModal').find('#latminute').val();
		var latsecond=$('#editModal').find('#latsecond').val();
		$.post('editplot',{
			plotid:plotid,
			plotname:plotname,
			londegree:londegree,
			lonminute:lonminute,
			lonsecond:lonsecond,
			latdegree:latdegree,
			latminute:latminute,
			latsecond:latsecond
		},
		function(result){
			if(result=='fail1')
			{
				$('#alert').text("水质监测点位名称 <"+plotname+"> 已存在，修改失败！");	
				$('#alert').attr('class','alert alert-warning');
				$('#alert').attr('style','');
			}
			else if(result=='fail2')
			{
				$('#alert').text("找不到指定的水质监测点位，修改失败！");	
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
				$('#alert').text("水质监测点位 <"+plotname+"> 信息修改成功");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});

	$('#del-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var plotid=$('#delModal').find('#plotid').text();
		$.post('delplot',{
			plotid:plotid
		},
		function(result){
			if(result=='fail1')
			{
				$('#alert').text("找不到指定的水质监测点位，删除失败！");	
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
				var plotname=$('#delModal').find('#plotname').val();
				$('#alert').text("水质监测点位 <"+plotname+"> 及其所有调查数据删除成功");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});
});
