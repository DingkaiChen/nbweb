$.fn.addplot=function(){
	$('#editModal').find('#action').val('0');
	$('#editModal').find('#id').val('0');
	$('#editModal').find('#submit').val('添加');
	$('#editModal').find('#plotname').removeAttr('readonly');
	$('#editModal').find('.modal-header').text('添加监测点位');
}

$.fn.editplot=function(){
	var row=$(this).parent().parent();
	var id=row.find('#plotid').text();
	var plotname=row.find('#plotname').text();
	var landtype=row.find('#landtype').text();
	var samplefrequency=row.find('#samplefrequency').text();
	var londegree=row.find('#londegree').text();
	var lonminute=row.find('#lonminute').text();
	var lonsecond=row.find('#lonsecond').text();
	var latdegree=row.find('#latdegree').text();
	var latminute=row.find('#latminute').text();
	var latsecond=row.find('#latsecond').text();
	$('#editModal').find('#action').val('1');
	$('#editModal').find('#id').val(id);
	$('#editModal').find('#plotname').val(plotname);
	$('#editModal').find('#landtype').val(landtype);
	$('#editModal').find('#samplefrequency').val(samplefrequency);
	$('#editModal').find('#londegree').val(londegree);
	$('#editModal').find('#lonminute').val(lonminute);
	$('#editModal').find('#lonsecond').val(lonsecond);
	$('#editModal').find('#latdegree').val(latdegree);
	$('#editModal').find('#latminute').val(latminute);
	$('#editModal').find('#latsecond').val(latsecond);
	$('#editModal').find('#submit').val('确定');
	$('#editModal').find('#plotname').attr('readonly','readonly');
	$('#editModal').find('.modal-header').text('编辑监测点位');
}

$.fn.delplot=function(){
	var row=$(this).parent().parent();
	var id=row.find('#plotid').text();
	var plotname=row.find('#plotname').text();
	$('#delModal').find('#action').val('2');
	$('#delModal').find('#id').val(id);
	$('#delModal').find('#del-message').text('确认删除空气质量监测点位 <'+plotname+'> 吗？');
	$('#delModal').find('#submit').val('确定');
}

$(document).ready(function(){
	$('#menu-air').attr('class','dropdown active');
	$('#btn-add').click(function(){
		$('#btn-add').addplot();
	});
	$('.del').click(function(){
		$(this).delplot();
	});
	$('.edit').click(function(){
		$(this).editplot();
	});
});

