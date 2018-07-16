$.fn.noEmpty=function(){
	var value=$.trim($(this).val());
	if (value=="")
	{
		$(this).addClass('form-invalid');
		$(this).siblings(".form-errorinfo").text('数据不能为空');
	}
}

$.fn.isInteger=function(){
	var value=$(this).val();
	var pattInteger=new RegExp("^\\d+$");
	if (!(pattInteger.test(value)))
	{
		$(this).addClass('form-invalid');
		$(this).parents('.form-validgroup').first().find(".form-errorinfo").text('数据必须为整形');
	}
}

$.fn.isFloat=function(){
	var value=$(this).val();
	var pattFloat=new RegExp("^-?(\\d+(\\.\\d+)?)$");
	if (!(pattFloat.test(value)))
	{	
		$(this).addClass('form-invalid');
		$(this).parents('.form-validgroup').first().find(".form-errorinfo").text('数据必须为数值');
	}
}

$(document).ready(function(){
	$(".form-clearerrorinfo").click(function(){
		$('.form-errorinfo').text('');
		$('.form-invalid').removeClass('form-invalid');
	});
	$("form").submit(function(e){
		$('.form-errorinfo').text('');
		$('.form-invalid').removeClass('form-invalid');
		$(".form-validator-empty").noEmpty();
		$(".form-validator-integer :not(.form-invalid)").isInteger();
		$(".form-validator-float :not(.form-invalid)").isFloat();
		if ($(this).find('.form-invalid').length != 0)
		{
			e.preventDefault();
			alert("Submit prevented");
		}		
	});
});
