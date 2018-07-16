$.fn.accept=function(){
	var row=$(this).parent().parent();
	var id=row.find('#registerid').text();
	var name=row.find('#username').text();
	$('#acceptModal').find('#accept-id').text(id);
	$('#acceptModal').find('#accept-username').text(name);
	$('#acceptModal').find('#accept-message').text('确认通过新注册用户 <'+name+'> 的审核？');
}

$.fn.reject=function(){
	var row=$(this).parent().parent();
	var id=row.find('#registerid').text();
	var name=row.find('#username').text();
	$('#rejectModal').find('#reject-id').text(id);
	$('#rejectModal').find('#reject-username').text(name);
	$('#rejectModal').find('#reject-message').text('拒绝新注册用户 <'+name+'> 的申请？');
}

$(document).ready(function(){
	$('#newusers').find('.accept').click(function(){
		$(this).accept();
	});
	$('#newusers').find('.reject').click(function(){
		$(this).reject();
	});

	$('#accept-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var id=$('#acceptModal').find('#accept-id').text();
		var name=$('#acceptModal').find('#accept-username').text();
		$.post('acceptnewuser',{
			id:id
		},
		function(result){
			if(result=='fail')
			{
				$('#alert').text('审核通过操作失败！');
				$('#alert').attr('class','alert alert-warning');
				$('#alert').attr('style','');
			}
			else
			{
				$('#newusers').text("");
				$('#newusers').append(result);
				$('#alert').text('用户 <'+name+'> 注册申请已审核通过，系统将自动发送邮件通知该用户。');
				$('#alert').attr('class','alert alert-success');
				$('#alert').attr('style','');
				$('#newusers').find('.accept').click(function(){
					$(this).accept();
				});
				$('#newusers').find('.reject').click(function(){
					$(this).reject();
				});
			}
		});
	});

	$('#reject-confirm').click(function(){
		$('.alert-info').attr('style','display:none;');
		var id=$('#rejectModal').find('#reject-id').text();
		var name=$('#rejectModal').find('#reject-username').text();
		$.post('rejectnewuser',{
			id:id
		},
		function(result){
			if(result=='fail')
			{
				$('#alert').text('拒绝通过的操作失败！');
				$('#alert').text('class','alert alert-warning');
				$('#alert').text('style','');
			}
			else
			{
				$('#newusers').text("");
				$('#newusers').append(result);
				$('#alert').text('用户 <'+name+'> 的注册申请已被拒绝，系统将自动发送邮件通知该用户.');
				$('#alert').text('class','alert alert-success');
				$('#alert').text('style','');
				$('#newusers').find('.accept').click(function(){
					$(this).accept();
				});
				$('#newusers').find('.reject').click(function(){
					$(this).reject();
				});
			}
		});
	});

});	
