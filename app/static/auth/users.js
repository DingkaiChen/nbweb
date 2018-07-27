$.fn.editdata=function(){
	var row=$(this).parent().parent();
	var userid=row.find('#userid').text();
	var username=row.find('#username').text();
	var name=row.find('#name').text();
	var roleid=row.find('#roleid').text();
	$('#editUserModal').find('#id').val(userid);
	$('#editUserModal').find('#username').text(username);
	$('#editUserModal').find('#name').text(name);
	$('#editUserModal').find('#role').val(roleid);
}

$.fn.deldata=function(){
	var row=$(this).parent().parent();
	var userid=row.find('#userid').text();
	var username=row.find('#username').text();
	var name=row.find('#name').text();
	$('#delUserModal').find('#id').val(userid);
	$('#delUserModal').find('#username').text(username);
	$('#delUserModal').find('#name').text(name);
}

$(document).ready(function(){
	$('#menu-user').attr('class','dropdown active');
	$('#editUserModal').find('#action').val('1');
	$('#delUserModal').find('#action').val('2');
	$('.edit').click(function(){
		$(this).editdata();
	});
	$('.del').click(function(){
		$(this).deldata();
	});
});
