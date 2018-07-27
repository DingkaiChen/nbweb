$.fn.editdata=function(){
	var row=$(this).parent().parent();
	var editid=row.find('#dataid').text();
	var plotname=row.find('#plotname').text();
	var timestamp=row.find('#timestamp').text();
	var no2=row.find('#no2').text().replace(/(^\s*)|(\s*$)/g,'');
	var co=row.find('#co').text().replace(/(^\s*)|(\s*$)/g,'');
	var so2=row.find('#so2').text().replace(/(^\s*)|(\s*$)/g,'');
	var o3=row.find('#o3').text().replace(/(^\s*)|(\s*$)/g,'');
	var pm10=row.find('#pm10').text().replace(/(^\s*)|(\s*$)/g,'');
	var pm25=row.find('#pm25').text().replace(/(^\s*)|(\s*$)/g,'');
	$('#editModal').find('#edit-id').text(editid);
	$('#editModal').find('#plotname').text(plotname);
	$('#editModal').find('#timestamp').text(timestamp);
	$('#editModal').find('#no2').val(no2);
	$('#editModal').find('#co').val(co);
	$('#editModal').find('#so2').val(so2);
	$('#editModal').find('#o3').val(o3);
	$('#editModal').find('#pm10').val(pm10);
	$('#editModal').find('#pm25').val(pm25);
}

$.fn.deldata=function(){
	var row=$(this).parent().parent();
	var delid=row.find('#dataid').text();
	var plotname=row.find('#plotname').text();
	var timestamp=row.find('#timestamp').text();
	$('#delModal').find('#del-id').text(delid);
	$('#delModal').find('#plotname').text(plotname);
	$('#delModal').find('#timestamp').text(timestamp);
}

$.fn.paginate=function(){
	var plotid=$('#query').find('#plotid').text();
	var timestart=$('#query').find('#timestart').text();
	var timeend=$('#query').find('#timeend').text();
	var page=$(this).attr('data-page');
	$.get('airdatas',{
		plotid:plotid,
		timestart:timestart,
		timeend:timeend,
		page:page
	},
	function(result){
		$('#datas').text('');
		$('#datas').append(result);
		$('.paginate').click(function(){
			$(this).paginate();
		});
	});
}

$(document).ready(function(){
	$('#menu-air').attr('class','dropdown active');
	$('#pnl-toggle').click(function() {
                $('#editpnl .panel-body').slideToggle("slow");
                datastatus=$(this).attr('data-status');
                if(datastatus=='open'){
                        $(this).attr('src','../static/icons/down.png');
                        $(this).attr('data-status','closed');
                }
                else{
                        $(this).attr('src','../static/icons/up.png');
                        $(this).attr('data-status','open');
                }
        });
        $('#editpnl').find('select').attr('style','width:100%;');
        $('#editpnl').find('select').find('option').attr('style','height:20px;');

	$('.del').click(function(){
		$(this).deldata();
	});
	$('.edit').click(function(){
		$(this).editdata();
	});
	$('.paginate').click(function(){
		$(this).paginate();
	});

	$('#del-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var plotid=$('#query').find('#plotid').text();
		var timestart=$('#query').find('#timestart').text();
		var timeend=$('#query').find('#timeend').text();
		var page=$('#currentpage').text();
		var delid=$('#delModal').find('#del-id').text();
		$.post('deldata',{
			plotid:plotid,
			timestart:timestart,
			timeend:timeend,
			page:page,
			delid:delid
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
				$('#datas').text("");
				$('#datas').append(result);
				$('.del').click(function(){
					$(this).deldata();
				});
				$('.edit').click(function(){
					$(this).editdata();
				});
				$('.paginate').click(function(){
					$(this).paginate();
				});
				var plotname=$('#delModal').find('#plotname').text();
				var timestamp=$('#delModal').find('#timestamp').text();
				$('#alert').text("监测点<"+plotname+"> 在"+timestamp+"的数据删除成功.");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});

	$('#edit-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var plotid=$('#query').find('#plotid').text();
		var timestart=$('#query').find('#timestart').text();
		var timeend=$('#query').find('#timeend').text();
		var page=$('#currentpage').text();
		var editid=$('#editModal').find('#edit-id').text();
		var no2=$('#editModal').find('#no2').val();
		var co=$('#editModal').find('#co').val();
		var so2=$('#editModal').find('#so2').val();
		var o3=$('#editModal').find('#o3').val();
		var pm10=$('#editModal').find('#pm10').val();
		var pm25=$('#editModal').find('#pm25').val();
		$.post('editdata',{
			plotid:plotid,
			timestart:timestart,
			timeend:timeend,
			page:page,
			editid:editid,
			no2:no2,
			co:co,
			so2:so2,
			o3:o3,
			pm10:pm10,
			pm25:pm25
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
				$('#datas').text("");
				$('#datas').append(result);
				$('.del').click(function(){
					$(this).deldata();
				});
				$('.edit').click(function(){
					$(this).editdata();
				});
				$('.paginate').click(function(){
					$(this).paginate();
				});
				var plotname=$('#editModal').find('#plotname').text();
				var timestamp=$('#editModal').find('#timestamp').text();
				$('#alert').text("监测点<"+plotname+"> 在"+timestamp+"的数据编辑成功.");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});


});

