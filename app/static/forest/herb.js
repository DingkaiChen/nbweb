$.fn.addsample=function(){
	$('#addsampleModal').find('.modal-title').text('添加样方数据');
	$('#addsampleModal').find('#id').val("0");
	$('#addsampleModal').find('#greenstructure').val('');
	$('#addsampleModal').find('#herbcoverage').val('');
	$('#addsampleModal').find('#arborstructure').val('');
	$('#addsampleModal').find('#sampletype').val('');
}

$.fn.editsample=function(){
	$('#addsampleModal').find('.modal-title').text('编辑样方数据');
	var id=$.trim($('#herbsample').find('#id').text());
	var greenstructure=$.trim($('#herbsample').find('#greenstructure').text());
	var herbcoverage=$.trim($('#herbsample').find('#herbcoverage').text());
	var arborstructure=$.trim($('#herbsample').find('#arborstructure').text());
	var sampletype=$.trim($('#herbsample').find('#sampletype').text());
	$('#addsampleModal').find('#id').val(id);
	$('#addsampleModal').find('#greenstructure').val(greenstructure);
	$('#addsampleModal').find('#herbcoverage').val(herbcoverage);
	$('#addsampleModal').find('#arborstructure').val(arborstructure);
	$('#addsampleModal').find('#sampletype').val(sampletype);
}	

$.fn.addherb=function(){
	$('#addherbModal').find('.modal-title').text('添加草本植被调查数据');
	$('#addherbModal').find('#id').val("0");
	var herbsample_id=$(this).attr('data-whatever');
	$('#addherbModal').find('#herbsample_id').val(herbsample_id);
	$('#addherbModal').find('#herbtype').val("-1");
	$('#addherbModal').find('#quantity').val("");
	$('#addherbModal').find('#height').val("");
	$('#addherbModal').find('#coverage').val("");
	$('#addherbModal').find('#state').val("");
	$('#addherbModal').find('#phenology').val("");
	$('#addherbModal').find('#herbtype').removeAttr('disabled');
}

$.fn.editherb=function(){
	$('#addherbModal').find('.modal-title').text('编辑草本植被调查数据');
	var row=$(this).parent().parent();
	var id=$.trim(row.find('#id').text());
	var herbtype=$.trim(row.find('#herbtype').text());
	var quantity=$.trim(row.find('#quantity').text());
	var height=$.trim(row.find('#height').text());
	var coverage=$.trim(row.find('#coverage').text());
	var state=$.trim(row.find('#state').text());
	var phenology=$.trim(row.find('#phenology').text());
	$('#addherbModal').find('#id').val(id);
	$('#addherbModal').find('#herbtype').val(herbtype);
	$('#addherbModal').find('#quantity').val(quantity);
	$('#addherbModal').find('#height').val(height);
	$('#addherbModal').find('#coverage').val(coverage);
	$('#addherbModal').find('#state').val(state);
	$('#addherbModal').find('#phenology').val(phenology);
	$('#addherbModal').find('#herbtype').attr('disabled','disabled');
}

$.fn.delherb=function(){
	var row=$(this).parent().parent();
	var del_id=row.find('#id').text();
	$('#delModal').find('#del-id').text(del_id);
	var del_url=$(this).attr('data-url');
	$('#delModal').find('#del-confirm').attr('data-url',del_url);
}

$.fn.changetab=function(){
	var quadrat_id=$(this).parent().find('.inactive-quadrat').text();
	var time=$.trim($('#timeMenu').text());
	$.get("changetab?quadratid="+quadrat_id+"&time="+time,function(result){
		if(result=='fail')
		{
		}
		else
		{
			$('#quadratsamples').text("");
			$('#quadratsamples').append(result);
			$('.inactive').click(function(){
				$(this).changetab();
			});
			$('#addquadratsample').click(function(){
				$(this).addsample();
			});
			$('#editquadratsample').click(function(){
				$(this).editsample();
			});
			$('#herbs').find('.add').click(function(){
				$(this).addherb();
			});
			$('#herbs').find('.edit').click(function(){
				$(this).editherb();
			});
			$('#herbs').find('.del').click(function(){
				$(this).delherb();
				$('#delModal').find('#del-message').text('确认删除草本植被 <'+$(this).attr('data-whatever')+'> 的数据？');
			});
			$('#delquadrat').click(function(){
				$(this).delherb();
				$('#delModal').find('#del-message').text('确认删除所选样方 <编号：'+$(this).attr('data-whatever')+'> 在当前调查时间的数据？');
			});
		}
	});
}

$.fn.submitsample=function(){
	var quadrat_id=$('#active-quadrat').text();
	var time=$.trim($('#timeMenu').text());
	var sample_id=$.trim($('#addsampleModal').find('#id').val());
	var greenstructure=$.trim($('#addquadratform').find('#greenstructure').val());
	var herbcoverage=$.trim($('#addquadratform').find('#herbcoverage').val());
	var arborstructure=$.trim($('#addquadratform').find('#arborstructure').val());
	var sampletype=$.trim($('#addquadratform').find('#sampletype').val());
	$.post('editquadratsample',{
		sample_id:sample_id,
		quadrat_id:quadrat_id,
		time:time,
		greenstructure:greenstructure,
		herbcoverage:herbcoverage,
		arborstructure:arborstructure,
		sampletype:sampletype
	},
	function(result){
		if(result.indexOf('fail')>=0)
		{
			var arr=result.split('@');
			alert(arr[1]);
		}
		else
		{
			$('#herbsample').text("");
			$('#herbsample').append(result);
			$('#addquadratsample').click(function(){
				$(this).addsample();
			});
			$('#editquadratsample').click(function(){
				$(this).editsample();
			});
			$('#herbs').find('.add').click(function(){
				$(this).addherb();
			});
			$('#herbs').find('.edit').click(function(){
				$(this).editherb();
			});
			$('#herbs').find('.del').click(function(){
				$(this).delherb();
				$('#delModal').find('#del-message').text('确认删除草本植被 <'+$(this).attr('data-whatever')+'> 的数据？');
			});
			$('#delquadrat').click(function(){
				$(this).delherb();
				$('#delModal').find('#del-message').text('确认删除所选样方 <编号：'+$(this).attr('data-whatever')+'> 在当前调查时间的数据？');
			});
		}
	});
}

$.fn.submitherb=function(){
	var herbid=$('#addherbModal').find('#id').val();
	var herbtype=$('#addherbModal').find('#herbtype').val();
	var herbsample_id=$.trim($('#addherbModal').find('#herbsample_id').val());
	var quantity=$.trim($('#addherbModal').find('#quantity').val());
	var height=$.trim($('#addherbModal').find('#height').val());
	var coverage=$.trim($('#addherbModal').find('#coverage').val());
	var state=$.trim($('#addherbModal').find('#state').val());
	var phenology=$.trim($('#addherbModal').find('#phenology').val());
	$.post('editherbsample',{
		id:herbid,
		herbtype:herbtype,
		herbsample_id:herbsample_id,
		quantity:quantity,
		height:height,
		coverage:coverage,
		state:state,
		phenology:phenology
	},
	function(result){
		if(result.indexOf('fail')>=0)
		{
			var arr=result.split('@');
			alert(arr[1]);
		}
		else
		{
			$('#herbs').text("");
			$('#herbs').append(result);
			$('#herbs').find('.add').click(function(){
				$(this).addherb();
			});
			$('#herbs').find('.edit').click(function(){
				$(this).editherb();
			});
			$('#herbs').find('.del').click(function(){
				$(this).delherb();
				$('#delModal').find('#del-message').text('确认删除草本植被 <'+$(this).attr('data-whatever')+'> 的数据？');
			});
		}
	});
}

$.fn.deleteconfirm=function(){
	var url=$(this).attr('data-url');
	var delid=$('#delModal').find('#del-id').text();
	$.post(url,{
		id:delid
	},
	function(result){
		if(result.indexOf('fail')>=0)
		{
			var arr=result.split('@');
			alert(arr[1]);
		}
		else
		{
			if(url=="delherbsample")
			{
				$('#herbs').text("");
				$('#herbs').append(result);
				$('#herbs').find('.add').click(function(){
					$(this).addherb();
				});
				$('#herbs').find('.edit').click(function(){
					$(this).editherb();
				});
				$('#herbs').find('.del').click(function(){
					$(this).delherb();
					$('#delModal').find('#del-message').text('确认删除草本植被 <'+$(this).attr('data-whatever')+'> 的数据？');
				});
			}
			else if(url=="delquadratsample")
			{
				$('#herbsample').text("");
				$('#herbsample').append(result);
				$('#addquadratsample').click(function(){
					$(this).addsample();
				});
			}
			else
			{
			}
		}
	});	
}

$(document).ready(function(){
	$('.inactive').click(function(){
		$(this).changetab();
	});
	$('#herbs').find('.add').click(function(){
		$(this).addherb();
	});
	$('#herbs').find('.edit').click(function(){
		$(this).editherb();
	});
	$('#addquadratsample').click(function(){
		$(this).addsample();
	});
	$('#editquadratsample').click(function(){
		$(this).editsample();
	});
	$('#addsampleModal').find('#add-confirm').click(function(){
		$(this).submitsample();
	});
	$('#addherbModal').find('#add-confirm').click(function(){
		$(this).submitherb();
	});
	$('#delModal').find('#del-confirm').click(function(){
		$(this).deleteconfirm();
	});
	$('#herbs').find('.del').click(function(){
		$(this).delherb();
		$('#delModal').find('#del-message').text('确认删除草本植被 <'+$(this).attr('data-whatever')+'> 的数据？');
	});
	$('#delquadrat').click(function(){
		$(this).delherb();
		$('#delModal').find('#del-message').text('确认删除所选样方 <编号：'+$(this).attr('data-whatever')+'> 在当前调查时间的数据？');
	});
});
