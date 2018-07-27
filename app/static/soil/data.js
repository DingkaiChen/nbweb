$.fn.editdata=function(){
	var row=$(this).parent().parent();
	var rowid=row.find('#rowid').text();
	var plotid=row.find('#plotid').text();
	var plotname=row.find('#plotname').text();
	var year=row.find('#year').text();
	var selectedindicatorid=$('#edit-indicator option').first().val();
	var value=row.find('#'+selectedindicatorid).text().replace(/(^\s*)|(\s*$)/g,'');
	$('#editdataModal').find('#row-id').text(rowid);
	$('#editdataModal').find('#edit-plot').text(plotname);
	$('#editdataModal').find('#edit-plot-id').text(plotid);
	$('#editdataModal').find('#edit-year').text(year);
	$('#editdataModal').find('#edit-indicator').val(selectedindicatorid);
	$('#editdataModal').find('#edit-value').val(value);
}

$.fn.deldata=function(){
	var row=$(this).parent().parent();
	var plotid=row.find('#plotid').text();
	var plotname=row.find('#plotname').text();
	var year=row.find('#year').text();
	$('#delModal').find('#del-plot').text(plotname);
	$('#delModal').find('#del-plot-id').text(plotid);
	$('#delModal').find('#del-year').text(year);
}

$.fn.changeindicator=function(){
	var rowid=$(this).parent().parent().find('#row-id').text();
	var selectedindicatorid=$('#editdataModal').find('#edit-indicator').val();
	var str1='#'+rowid;
	var str2='#'+selectedindicatorid;
	var value=$(str1).find(str2).text().replace(/(^\s*)|(\s*$)/g,'');
	$('#editdataModal').find('#edit-value').val(value);
}

$(document).ready(function(){
	$('#menu-soil').attr('class','dropdown active');
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
	$('#edit-indicator').change(function(){
		$(this).changeindicator();
	});

	$('#del-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var plotid=$('#delModal').find('#del-plot-id').text();
		var year=$('#delModal').find('#del-year').text();
		var indicatorid=$('#delModal').find('#del-indicator').val();
		var plots=[];
		var indicators=[];
		var years=[];
		$('#query #plots span').each(function(){
			plots.push($(this).text());
		});
		$('#query #years span').each(function(){
			years.push($(this).text());
		});
		$('#query #indicators span').each(function(){
			indicators.push($(this).text());
		});
		var plotsjson=JSON.stringify(plots);
		var yearsjson=JSON.stringify(years);
		var indicatorsjson=JSON.stringify(indicators)
		$.post('deldata',{
			plotid:plotid,
			year:year,
			indicatorid:indicatorid,
			plots:plotsjson,
			years:yearsjson,
			indicators:indicatorsjson
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
				var plotname=$('#delModal').find('#del-plot').text();
				var indicator=$('#delModal').find('#del-indicator').find("[value='"+indicatorid+"']").text();
				$('#alert').text("样点<"+plotname+"> "+year+"年度 "+indicator+" 指标数据删除成功.");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});

	$('#edit-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var plotid=$('#editdataModal').find('#edit-plot-id').text();
		var year=$('#editdataModal').find('#edit-year').text();
		var indicatorid=$('#editdataModal').find('#edit-indicator').val();
		var value=$('#editdataModal').find('#edit-value').val();
		var plots=[];
		var indicators=[];
		var years=[];
		$('#query #plots span').each(function(){
			plots.push($(this).text());
		});
		$('#query #years span').each(function(){
			years.push($(this).text());
		});
		$('#query #indicators span').each(function(){
			indicators.push($(this).text());
		});
		var plotsjson=JSON.stringify(plots);
		var yearsjson=JSON.stringify(years);
		var indicatorsjson=JSON.stringify(indicators)
		$.post('editdata',{
			plotid:plotid,
			year:year,
			indicatorid:indicatorid,
			value:value,
			plots:plotsjson,
			years:yearsjson,
			indicators:indicatorsjson
		},
		function(result){
			if(result=='fail')
			{
				$('#alert').text("编辑失败！");	
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
				var plotname=$('#editdataModal').find('#edit-plot').text();
				var indicator=$('#editdataModal').find('#edit-indicator').find("[value='"+indicatorid+"']").text();
				$('#alert').text("样点<"+plotname+"> "+year+"年度 "+indicator+" 指标数据编辑成功.");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});
});
