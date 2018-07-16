$.fn.addplot=function(){
	$('#editModal').find('#action').val('0');
	$('#editModal').find('#id').val('0');
	$('#editModal').find('#submit').val('添加');
	$('#editModal').find('#plotname').removeAttr('readonly');
	$('#editModal').find('.modal-header').text('添加样地');
}

$.fn.editplot=function(){
	var row=$(this).parent().parent();
	var id=row.find('#plotid').text();
	var plotname=row.find('#plotname').text();
	var region=row.find('#region').text();
	var frequency=row.find('#frequency').text();
	var londegree=row.find('#londegree').text();
	var lonminute=row.find('#lonminute').text();
	var lonsecond=row.find('#lonsecond').text();
	var latdegree=row.find('#latdegree').text();
	var latminute=row.find('#latminute').text();
	var latsecond=row.find('#latsecond').text();
	var altitude=row.find('#altitude').text();
	$('#editModal').find('#action').val('1');
	$('#editModal').find('#id').val(id);
	$('#editModal').find('#plotname').val(plotname);
	$('#editModal').find('#region').val(region);
	$('#editModal').find('#frequency').val(frequency);
	$('#editModal').find('#londegree').val(londegree);
	$('#editModal').find('#lonminute').val(lonminute);
	$('#editModal').find('#lonsecond').val(lonsecond);
	$('#editModal').find('#latdegree').val(latdegree);
	$('#editModal').find('#latminute').val(latminute);
	$('#editModal').find('#latsecond').val(latsecond);
	$('#editModal').find('#altitude').val(altitude);
	$('#editModal').find('#submit').val('确定');
	$('#editModal').find('#plotname').attr('readonly','readonly');
	$('#editModal').find('.modal-header').text('编辑样地');
}

$.fn.delplot=function(){
	var row=$(this).parent().parent();
	var id=row.find('#plotid').text();
	var plotname=row.find('#plotname').text();
	$('#delModal').find('#action').val('2');
	$('#delModal').find('#id').val(id);
	$('#delModal').find('#del-message').text('确认删除土壤样地 <'+plotname+'> 吗？');
	$('#delModal').find('#submit').val('确定');
}

$(document).ready(function(){
	$('#editModal').find('#plotname').addClass('form-validator-empty');
	$('#editModal').find('#frequency').addClass('form-validator-empty form-validator-integer');
	$('#editModal').find('#londegree').addClass('form-validator-empty form-validator-integer');
	$('#editModal').find('#lonminute').addClass('form-validator-empty form-validator-integer');
	$('#editModal').find('#lonsecond').addClass('form-validator-empty form-validator-float');
	$('#editModal').find('#latdegree').addClass('form-validator-empty form-validator-integer');
	$('#editModal').find('#latminute').addClass('form-validator-empty form-validator-integer');
	$('#editModal').find('#latsecond').addClass('form-validator-empty form-validator-flaot');
	$('#editModal').find('#altitude').addClass('form-validator-empty form-validator-integer');
	$('#btn-add').click(function(){
		$('#btn-add').addplot();
	});
	$('#btn-upload').click(function(){
		$('#uploadform').attr('style','');
		$('#action').val('3');
	});
	$('#upload-cancel').click(function(){
		$('#uploadform').attr('style','display:none;');
	});
	$('.del').click(function(){
		$(this).delplot();
	});
	$('.edit').click(function(){
		$(this).editplot();
	});
});
