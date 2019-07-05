	$.fn.addplot=function(){
		$('#pnl-form').attr('style','');
		$('#pnl-form #id').val('0');
		$('#pnl-form #plotname').val(null);
		$('#pnl-form #address').val(null);
		$('#pnl-form #londegree').val(null);
		$('#pnl-form #lonminute').val(null);
		$('#pnl-form #lonsecond').val(null);
		$('#pnl-form #latdegree').val(null);
		$('#pnl-form #latminute').val(null);
		$('#pnl-form #latsecond').val(null);
		$('#pnl-form #altitude').val(null);
		$('#pnl-form #imgurl').val(null);
		$('#pnl-form #plotname').removeAttr('readonly');
		$('#pnl-form .panel-heading').text('添加样地');
	}
	$.fn.editplot=function(){
		var row=$(this).parent().parent();
		var id=row.find('#plotid').text();
		var plotname=row.find('#plotname').text();
		var address=row.find('#address').text();
		var londegree=row.find('#londegree').text();
		var lonminute=row.find('#lonminute').text();
		var lonsecond=row.find('#lonsecond').text();
		var latdegree=row.find('#latdegree').text();
		var latminute=row.find('#latminute').text();
		var latsecond=row.find('#latsecond').text();
		var altitude=row.find('#altitude').text();
		var imgurl=row.find('#imgurl').attr('href');
		$('#pnl-form #id').val(id);
		$('#pnl-form #plotname').val(plotname);
		$('#pnl-form #address').val(address);
		$('#pnl-form #londegree').val(londegree);
		$('#pnl-form #lonminute').val(lonminute);
		$('#pnl-form #lonsecond').val(lonsecond);
		$('#pnl-form #latdegree').val(latdegree);
		$('#pnl-form #latminute').val(latminute);
		$('#pnl-form #latsecond').val(latsecond);
		$('#pnl-form #altitude').val(altitude);
		$('#pnl-form #imgurl').val(imgurl);
		$('#pnl-form #plotname').attr('readonly','readonly');
		$('#pnl-form .panel-heading').text('编辑样地');
		$('#pnl-form').attr('style','');
	}
	$.fn.delplot=function(){
		$('.modal-body #del-message').text('确认删除监测样地 "'+$(this).attr('data-whatever')+'" 及其所有数据？');
		var row=$(this).parent().parent();
		var id=row.find('#plotid').text();
		var plotname=row.find('#plotname').text();
		$('.modal-body #del-id').text(id);
		$('.modal-body #del-name').text(plotname);
	}

	$.fn.showimg=function(){
		var row=$(this).parent().parent();
		var imgurl=row.find('#imgurl').attr('data-whatever')
		$('#imgModal #showimg').attr('src', imgurl);
	}
	
	$.fn.imgUpload=function(){
		$.ajaxFileUpload({
			url:'imgupload',
			secureuri:false,
			fileElementId:'file1',
			dataType:'json',
			success:function(data,status)
			{
				$("#img1").attr("src",data.imgurl);
				$("#pnl-form #imgurl").val(data.imgurl);
			},
			error:function(data,status,e)
			{
				alert(e);
			}
		});
		return false;
	}
	
	$.fn.checkerror=function(){
		$(this).attr('style','');
		if($(this).find('#id').val()=='0'){
			$(this).find('.panel-heading').text('添加样地');
		}else{
			$(this).find('.panel-heading').text('编辑样地');
			$(this).find('#plotname').attr('readonly','readonly');
		}
	}
	$(document).ready(function(){
		$('#menu-forest').attr('class','dropdown active');
		$('.error-info').parent().parent().parent().parent().checkerror();
		$('#pnl-form #imgurl').attr('style','display:none;');
		$('#btn-add').click(function(){
			$('#btn-add').addplot();
		});
		$('.del').click(function(){
			$(this).delplot();
		});
		$('.edit').click(function(){
			$(this).editplot();
		});
		$('#btn-cancel').click(function(){
			$('#pnl-form').attr('style','display:none;');
		});
		$('#plots #imgurl').click(function(){
			$(this).showimg();
		});
		$('#del-confirm').click(function(){
			var plotid=$('.modal-body #del-id').text();
			var plotname=$('.modal-body #del-name').text();
			$.post('delplot',{
				id:plotid,
				name:plotname
			},
			function(result){
				if(result=='fail')
				{
				}
				else
				{
					$('#plots').text("");
					$('#plots').append(result);
					$('#btn-add').click(function(){
						$('#btn-add').addplot();
					});
					$('.del').click(function(){
						$(this).delplot();
					});
					$('.edit').click(function(){
						$(this).editplot();
					});
					$('#plots #imgurl').click(function(){
						$(this).showimg();
					});
				}
			});	
		});
		$('#btn-upload').click(function(){
			$(this).imgUpload();
		});
	});
