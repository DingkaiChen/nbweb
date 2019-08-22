$.fn.addurl=function(){
	$('#editModal').find('#action').val('0');
	$('#editModal').find('#id').val('0');
	$('#editModal').find('#submit').val('添加');
	$('#editModal').find('#years').removeAttr('readonly');
	$('#editModal').find('#regions').removeAttr('readonly');
	$('#editModal').find('#indicators').removeAttr('readonly');
	$('#editModal').find('.modal-header').text('添加链接');
}

$.fn.editurl=function(){
	var row=$(this).parent().parent();
	var id=row.find('#shpid').text();
	var year=row.find('#year').text();
	var region=row.find('#region').text();
	var indicator=row.find('#indicator').text();
	var shpurl=row.find('#shpurl').text();
	$('#editModal').find('#action').val('1');
	$('#editModal').find('#id').val(id);
	$('#editModal').find('#year').val(year);
	$('#editModal').find('#region').val(region);
	$('#editModal').find('#indicator').val(indicator);
	$('#editModal').find('#shp').val(shpurl);
	$('#editModal').find('#submit').val('确定');
	$('#editModal').find('#year').attr('readonly','readonly');
	$('#editModal').find('#region').attr('readonly','readonly');
	$('#editModal').find('#indicator').attr('readonly','readonly');
	$('#editModal').find('.modal-header').text('编辑链接');
}

$.fn.delurl=function(){
	var row=$(this).parent().parent();
	var id=row.find('#shpid').text();
	var year=row.find('#year').text();
	var region=row.find('#region').text();
	var indicator=row.find('#indicator').text();
	$('#delModal').find('#action').val('2');
	$('#delModal').find('#id').val(id);
	$('#delModal').find('#del-message').text('确认删除 '+region+' '+year+'年 <'+indicator+'> 指标的图层链接吗？');
	$('#delModal').find('#submit').val('确定');
}

$(document).ready(function(){
	$('#menu-shp').attr('class','dropdown active');
	$('#btn-add').click(function(){
		$('#btn-add').addurl();
	});
	$('.del').click(function(){
		$(this).delurl();
	});
	$('.edit').click(function(){
		$(this).editurl();
	});
});
