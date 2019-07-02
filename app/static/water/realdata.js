$(document).ready(function(){
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
});

