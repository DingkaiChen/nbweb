$.fn.editplot=function(){
	var row=$(this).parent().parent();
	var id=row.find('#indicatorid').text();
	var indicatorname=row.find('#indicatorname').text();
	var symbol=row.find('#symbol').text();
	var unit=row.find('#unit').text();
	var indicatortype=row.find('#indicatortype').text();
	$('#editModal').find('#action').val('1');
	$('#editModal').find('#id').val(id);
	$('#editModal').find('#edit-name').text(indicatorname);
	$('#editModal').find('#indicatortype').val(indicatortype);
	$('#editModal').find('#symbol').val(symbol);
	$('#editModal').find('#unit').val(unit);
	$('#editModal').find('#submit').val('确定');
	$('#editModal').find('.modal-header').text('编辑样地');
}

$.fn.delplot=function(){
	var row=$(this).parent().parent();
	var id=row.find('#indicatorid').text();
	var indicatorname=row.find('#indicatorname').text();
	$('#delModal').find('#action').val('2');
	$('#delModal').find('#id').val(id);
	$('#delModal').find('#del-message').text('确认删除土壤监测指标项 <'+indicatorname+'> 吗？');
	$('#delModal').find('#submit').val('确定');
}

$(document).ready(function(){
	$('#menu-soil').attr('class','dropdown active');
	$('.del').click(function(){
		$(this).delplot();
	});
	$('.edit').click(function(){
		$(this).editplot();
	});
});
