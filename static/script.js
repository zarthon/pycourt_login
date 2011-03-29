var activeLogin = '';
var activeDone = 'today';
var orderlist = '';
var tempname = '';
var tempprice = '';
var tempid ='';
var tempqty = '';
var tempoid = '';
var rowCounter = 0;
var counter_no = '';
var total_price = '';
var total_final = 0 ;


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
                                    var c = tempoid.split("count");
                                 
                                    var count_no = c[1].split("%");
                                    counter_no = count_no[0];
                                    
                                    $('#menu_t').css('display','none');
                                    $('#quantity-form').css('display','');
                                    return false;});

		$("#qty_sub").bind("click",function(){
                                    tempqty = $("#qty_no").attr("value"); 
									
                                    orderlist = orderlist + tempoid +'%'+tempqty+',';
									$("#orders").val(orderlist);
									total_price = parseInt(tempqty) * parseInt(tempprice);
									
		                            if(rowCounter < 10)
		   	                        {
                        				rowCounter = rowCounter+1;
                        				$('#' + rowCounter + '_1').text(tempname);
                        				$('#' + rowCounter + '_2').text(tempprice);
                        				$('#' + rowCounter + '_3').text(tempqty);
                                        $('#' + rowCounter + '_5').text(counter_no);
										$('#' + rowCounter + '_4').text(total_price);
                        				$('#row_' + rowCounter).fadeIn(1000);
		                            }
									else
                                    {
                        				alert("Maximum Order Limit Reached !!");
                                    }
                                    if(rowCounter >0 )$('#add-success').slideDown(1200);
									
									total_final = 0;
                                	for(var k=1; k <= rowCounter;k++)
									{
										
										
										total_final = total_final + parseInt($('#' + k  + '_4').text());
										
									}
									$('#total_disp').text(total_final);
										
									
									return false ;});
	
		
	$("#qty_sub").bind("click",function(){ $('#menu_t').css('display','');});
	$("#qty_sub").bind("click",function(){$('#quantity-form').css('display','none');});

	
});

$(document).ready(function(){
        rowCounter = 0;
		$('#t1 img').bind("click", function(){var img_id = '';
											if(rowCounter < 10) {img_id = $(this).attr("id").substring(3,4);}
											else {
												img_id = $(this).attr("id").substring(3,5);
												if(img_id == '10'){
													}
												else img_id = 1;
												
												}
											total_final = total_final - parseInt($('#' + img_id + '_4').text());
									
									$('#total_disp').text(total_final);
									slideRows(img_id);
									
									$('#row_' + img_id).fadeOut(1000);
                                    var temp = orderlist.split(",");
                                    var tem_orderlist = '';
									
                                    for(var j=0;j<temp.length-1;j++){
                                        if(j != parseInt(img_id)-1){
                                            tem_orderlist += temp[j]+',';
                                        }
                                    } 
                                    orderlist = tem_orderlist;
									$("#orders").val(orderlist);
									
				    				
									rowCounter = rowCounter - 1;
									if(rowCounter ==0)$('#add-success').slideUp(1200);
									return false;});
		
		
		$('#sub_order').click(function(){
								
								$('#main').fadeTo(0,0.5);
								if(confirm("Are you sure u want to place this order ? "))
								{
									$('#main').fadeTo(500,1);
									return true;
								}
								else
								{
									$('#main').fadeTo(500,1);
									return false;
								}
									  
								});
        $('#add_dish').click(function(){
                document.location.href = '/addish';
        });


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
		var t = current;

    if (current != activeDone) {
  
        $('#' + activeDone + '-nav').removeClass('active');
       //  $('#' + current).fadeIn(200);
        $('#' + activeDone).fadeOut(300,function(){
												  $('#' + current + '-nav').addClass('active');
												  $('#' + current.toLowerCase().replace(' ','')).fadeIn(300)
												 });
       
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
			
			for (var k=1;k<=5;k++)
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
