var activeLogin = '';
var activeDone = 'today';
var orderlist = '';
var tempname = '';
var tempprice = '';
var tempid ='';
var tempqty = '';
var tempoid = '';
var rowCounter = 0;

//what is this function doing
$(document).ready(function() {
    $("#qty_no").keydown(function(event) {
    	if ( event.keyCode == 46 || event.keyCode == 8 )
			{ }
        else {         
			if (event.keyCode < 48 || event.keyCode > 57 )
				{
            	event.preventDefault(); 
              	}       
        	}

	});
	$('#qty_no').keydown(function() {
                var len = this.value.length;
                if (len >= 1)
				{
                    this.value = this.value.substring(0, 0);
                }
                $('#charLeft').text(150 - len);
            });
});


$(function() {
    $("a").click(function() {this.blur();});
	

    if (activeLogin != '') {
        active = $('#' + activeLogin.toLowerCase());
		
        $("#signup, #login").bind("click", function() { 
                                            SwapLogin($(this).html());return false; });

        $("#signup-form input:not(.submit), #login-form input:not(.submit),  #done-form textarea").focus(function() { 
                                            $(this).parent().addClass("focused") });

        $("#signup-form input:not(.submit), #login-form input:not(.submit),  #done-form textarea").blur(function() { 
                                            $(this).parent().removeClass("focused") });
    }


    $('#no-problem').bind("click", function() { $(this).parent().css('display', 'none'); });
    
    $('#done-list li:last-child').css('border-bottom', '1px solid #E5E5E5');
    $('#add-friend, #add-friend-link').click(function() { $('#add-friend-form').toggle(); });

    $('#friend-input').focus(function() { if ($(this).attr('value') == 'friend\'s username') { $(this).attr('value',''); } });

    
    $('#id_description').focus();
	
	$("#done-nav a").bind("click", function() {SwapDone($(this).attr("href"));
											return false;});


	$('#foodlist_1 img, #foodlist_2 img, #foodlist_3 img').bind("click", function() {
                                    tempoid = $(this).attr('id');
                                    var tempparent = $(this).parent();
                                    var p = tempparent.attr("class")
                                    var temp = $(this).attr('id') + 'a';
                                    var temp1 = ('#' + temp); 
                                    var temp2 = $(this).attr('id') + 'b';
                                    var temp3 = ('#' + temp2);
                                    tempname = $(temp1).text(); 
                                    tempprice = $(temp3).text();
                                    var temp7 = "#" + p;
                                    
                                    $('#menu_t').css('display','none');
                                    $('#quantity-form').css('display','');
                                    return false;});

		$("#qty_sub").bind("click",function(){
                                    tempqty = $("#qty_no").attr("value"); 
								/*	for(var j=0;j<tempqty;j++)
									{
									    orderlist = orderlist + tempoid + ','; 
								    }*/
                                    orderlist = orderlist + tempoid +'%'+tempqty+',';
									$("#orders").val(orderlist);											  
		                            if(rowCounter <= 10)
		   	                        {
                        				rowCounter = rowCounter+1;
                        				$('#' + rowCounter + '_1').text(tempname);
                        				$('#' + rowCounter + '_2').text(tempprice);
                        				$('#' + rowCounter + '_3').text(tempqty);
                        				$('#row_' + rowCounter).removeClass("hide");
		                            }
			                        else
                                    {
                        				alert("Maximum Order Limit Reached !!");
                                    }
                                	return false ;});
	
		
	$("#qty_sub").bind("click",function(){ $('#menu_t').css('display','');});
	$("#qty_sub").bind("click",function(){$('#quantity-form').css('display','none');});

	
});

$(document).ready(function(){
        rowCounter = 0;
		$('#t1 img').bind("click", function(){
		        					var img_id = $(this).attr("id").substring(3,4);
									slideRows(img_id);
                                    alert(img_id);
				    				$('#row_' + rowCounter).addClass("hide");
									rowCounter = rowCounter - 1;
									return false;});

});


						   

function SwapLogin(current) {
    activeLoginLower = activeLogin.toLowerCase();
    currentLower = current.toLowerCase();
    $('#' + activeLoginLower + '-form').css('display', 'none');
    $('#' + currentLower + '-form').css('display', 'block');
    $('#' + activeLoginLower).replaceWith('<a href="/' + activeLoginLower + '/" id="' + activeLoginLower + '" onclick="SwapLogin(\'' + activeLogin + '\'); return false;">' + activeLogin + '</a>');
    $('#' + currentLower).replaceWith('<span id="' + currentLower + '" onclick="SwapLogin(\'' + current + '\'); return false;">' + current + '</span>');
    activeLogin = current;
    return false;
}


function SwapDone(current) {
    current = current.toLowerCase();
    if (current != activeDone) {
        $('#' + current + '-nav').addClass('active');
        $('#' + activeDone + '-nav').removeClass('active');
        $('#' + current).css('display', 'block');
        $('#' + activeDone).css('display', 'none');
        $('#' + current.toLowerCase().replace(' ','')).css('display','block');
        activeDone = current;
        return false;
    } else {
        return false;
    }
}

function slideRows(number ){
	
	if(number<rowCounter)
	{
    	for(var i=number;i <= rowCounter - 1;i++)
		{		
			var j =  parseInt(i) + 1;
			
			for (var k=1;k<=3;k++)
			{
				var cell_1 = '#' + i + '_' + k;
				var cell_2 = '#' + j + '_' + k;
				
				var temp = $(cell_2).text();
				$(cell_1).text(temp);		
			}
		}
		
		return false;
	}
	else  return false;

}
