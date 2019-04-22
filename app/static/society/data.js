$.fn.editdata=function(){
	var row=$(this).parent().parent();
	var rowid=row.find('#rowid').text();
	var indicatorid=row.find('#indicatorid').text();
	var indicatorname=row.find('#indicatorname').text();
	//var year=row.find('#year').text();
	var selectedyear=$('#edit-year option').first().val();
	var value=row.find('#'+selectedyear).text().replace(/(^\s*)|(\s*$)/g,'');
	$('#editdataModal').find('#row-id').text(rowid);
	$('#editdataModal').find('#edit-indicator').text(indicatorname);
	$('#editdataModal').find('#edit-indicator-id').text(indicatorid);
	//$('#editdataModal').find('#edit-year').text(year);
	$('#editdataModal').find('#edit-year').val(selectedyear);
	$('#editdataModal').find('#edit-value').val(value);
}

$.fn.deldata=function(){
	var row=$(this).parent().parent();
	var indicatorid=row.find('#indicatorid').text();
	var indicatorname=row.find('#indicatorname').text();
	//var year=row.find('#year').text();
	$('#delModal').find('#del-indicator').text(indicatorname);
	$('#delModal').find('#del-indicator-id').text(indicatorid);
	//$('#delModal').find('#del-year').text(year);
}

$.fn.changeyear=function(){
	var rowid=$(this).parent().parent().find('#row-id').text();
	var selectedyear=$('#editdataModal').find('#edit-year').val();
	var str1='#'+rowid;
	var str2='#'+selectedyear;
	var value=$(str1).find(str2).text().replace(/(^\s*)|(\s*$)/g,'');
	$('#editdataModal').find('#edit-value').val(value);
}

$(document).ready(function(){
	$('#menu-society').attr('class','dropdown active');
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
	$('#edit-year').change(function(){
		$(this).changeyear();
	});

	$('#del-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var indicatorid=$('#delModal').find('#del-indicator-id').text();
		//var year=$('#delModal').find('#del-year').text();
		var year=$('#delModal').find('#del-year').val();
		var indicators=[];
		var years=[];
		$('#query #years span').each(function(){
			years.push($(this).text());
		});
		$('#query #indicators span').each(function(){
			indicators.push($(this).text());
		});
		var yearsjson=JSON.stringify(years);
		var indicatorsjson=JSON.stringify(indicators)
		$.post('deldata',{
			year:year,
			indicatorid:indicatorid,
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
				var indicatorname=$('#delModal').find('#del-indicator').text();
				var year=$('#delModal').find('#del-year').find("[value='"+year+"']").text();
				$('#alert').text("指标 <"+indicatorname+"> "+year+" 年度数据删除成功.");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});

	$('#edit-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var indicatorid=$('#editdataModal').find('#edit-indicator-id').text();
		var year=$('#editdataModal').find('#edit-year').val();
		var value=$('#editdataModal').find('#edit-value').val();
		var indicators=[];
		var years=[];
		$('#query #years span').each(function(){
			years.push($(this).text());
		});
		$('#query #indicators span').each(function(){
			indicators.push($(this).text());
		});
		var yearsjson=JSON.stringify(years);
		var indicatorsjson=JSON.stringify(indicators)
		$.post('editdata',{
			year:year,
			indicatorid:indicatorid,
			value:value,
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
				var indicatorname=$('#editdataModal').find('#edit-indicator').text();
				var year=$('#editdataModal').find('#edit-year').find("[value='"+year+"']").text();
				$('#alert').text("指标 <"+indicatorname+"> "+year+" 年度数据编辑成功.");	
				$('#alert').attr('class','alert alert-info');
				$('#alert').attr('style','');
			}
		});
	});
});
