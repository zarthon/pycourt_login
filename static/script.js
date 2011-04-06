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
var foodlist_deleted = '';


$(document).ready(function() {
    $("#qty_no").keydown(function(event) {
    	if ( event.keyCode == 46 || event.keyCode == 8 )
			{ }
        else {         
			if (event.keyCode < 49 || event.keyCode > 57 )
				{
            	event.preventDefault(); 
				('#qty_no').text('1');
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
									
									
                                 	$(this).parent().parent().fadeOut(400);
									
									
                                    var count_no = c[1].split("%");
                                    counter_no = count_no[0];
                                    $('#done-nav').hide();
                                    $('#menu_t').fadeOut(400,function(){
																	  $('#quantity-form').fadeIn(400);
																	 
																	  });
									
																	   
                                    
									$('#done-nav').css('display','none');
									$('#tab-qty').css('display','');
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
                        				$('#row_' + rowCounter).fadeIn(1200);
		                            }
									else
                                    {
                        				alert("Maximum Order Limit Reached !!");
                                    }
                                    if(rowCounter > 0 ){
										$('#add-success').slideDown(1200);	
										$('#header-cart').fadeIn(200);
									}
									
									total_final = 0;
                                	for(var k=1; k <= rowCounter;k++)
									{
										
										
										total_final = total_final + parseInt($('#' + k  + '_4').text());
										
									}
									$('#total_disp').text(total_final);
										
									$('#done-nav').css('display','');
									$('#tab-qty').css('display','none');
									return false ;});
	
		

	$("#qty_sub").bind("click",function(){$('#quantity-form').fadeOut(400,function(){
																				   $('#menu_t').fadeIn(400);
																				   });
											$('#done-nav').show();	
																	  });
 
	
});

$(document).ready(function(){
        rowCounter = 0;
		
		$('#t1 img').bind("click", function(){var img_id = '';
											
											if(rowCounter < 10) {img_id = $(this).attr("id").substring(3,4);}
											else {
												img_id = $(this).attr("id").substring(3,5);
											}
												
											total_final = total_final - parseInt($('#' + img_id + '_4').text());
									
									$('#total_disp').text(total_final);
									 
									$('#order_cart').fadeOut(400,function(){
																		  	slideRows(parseInt(img_id));
																		   $('#row_' + rowCounter).hide()	
																		  });
														 
									 $('#order_cart').fadeIn(500,function(){
																		  
									 rowCounter = rowCounter - 1;
									  rowCounter = parseInt(rowCounter);
									
								if( rowCounter == 0)$('#add-success').slideUp(1200,function(){
																							$('#header-cart').fadeOut(300)
																							});
								
																		  });						
									
                                    var temp = orderlist.split(",");
                                    var tem_orderlist = '';
									
                                    for(var j=0;j<temp.length-1;j++){
                                        if(j != parseInt(img_id)-1){
                                            tem_orderlist += temp[j]+',';
                                        }
										else
										{
											foodlist_deleted = temp[j];
										}
                                    } 
									foodlist_deleted = foodlist_deleted.substring(0,7);
									$('#'+foodlist_deleted).parent().parent().fadeIn(400);
									
                                    orderlist = tem_orderlist;
									$("#orders").val(orderlist);
									
				    				
									
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
		
		
		
		//var counter1 = $('#orderlist-4 tr:last').get(0).rowIndex;
		var counter1 = $('#orderlist-4 tr:last').index();
		
		for (var l = 0; l <= counter1; l++){
			var ABCD = $('#orderlist-4 tr:eq('+l+') td:eq(3)').text();
			
			if( ABCD == "False")
			{
				$('#orderlist-4 tr:eq('+l+') td:eq(4) .a').hide();
				$('#orderlist-4 tr:eq('+l+') td:eq(3)').text("Not Available")
				
			}
			else
			{
				
				$('#orderlist-4 tr:eq('+l+') td:eq(4) .b').hide();
				$('#orderlist-4 tr:eq('+l+') td:eq(3)').text("Available")
			
			}
			
			}
			$('#orderlist-4 .a').click(function(){
																
																	var len = $(this).attr("id").length
																	var id = $(this).attr("id").substring(0,parseInt(len)-1)

																	$(this).hide();
																	var rowIndex = $(this).parent().parent().index()
																	$('#orderlist-4 tr:eq('+(rowIndex)+') td:eq(3)').text("Not Available")
																	$('#'+id+'y').show(); 
																	jQuery.ajax({
																	cache: false,
																	url: "/changeavailability",
																	typr: "GET",
																	data: "id="+id,
																	success: function(data){
																		
																	 },
																	 });					  })
			$('#orderlist-4 .b').click(function(){
																
																	var len = $(this).attr("id").length
																	var id = $(this).attr("id").substring(0,parseInt(len)-1)
																	$(this).hide();
																	var rowIndex = $(this).parent().parent().index()
																	$('#orderlist-4 tr:eq('+(rowIndex)+') td:eq(3)').text("Available")
																	$('#'+id+'x').show();
																	jQuery.ajax({
																	cache: false,
																	url: "/changeavailability",
																	typr: "GET",
																	data: "id="+id,
																	success: function(data){
																		
																	 },
																	 });
																	  })
			
			var rowCount = $('#orderlist-1 tr:last').index();
			for(var l = 0 ; l <= rowCount ; l++)
			{
				var tempStatus = $('#orderlist-1 tr:eq('+l+') td:eq(5)').text();
				if (tempStatus == '0')
				{
					$('#orderlist-1 tr:eq('+l+') td:eq(5)').text("In Queue");
					$('#orderlist-1 tr:eq('+l+') td:eq(6) .b').hide();
					$('#orderlist-1 tr:eq('+l+') td:eq(6) .c').hide();
					
				}
				else if (tempStatus == '1')
				{
					$('#orderlist-1 tr:eq('+l+') td:eq(5)').text("Under Preparation");
					$('#orderlist-1 tr:eq('+l+') td:eq(6) .a').hide();
					$('#orderlist-1 tr:eq('+l+') td:eq(6) .c').hide();
					
				}
				else if (tempStatus == '2')
				{
					$('#orderlist-1 tr:eq('+l+') td:eq(5)').text("Prepared");
					$('#orderlist-1 tr:eq('+l+') td:eq(6) .a').hide();
					$('#orderlist-1 tr:eq('+l+') td:eq(6) .b').hide();
										
				}
			}
			
	$('#orderlist-1 .a').bind("click",function(){
											  		var img_id = $(this).attr("id").substring(0,$(this).attr("id").length - 1);
													 
													$(this).hide();
													var rowCount2 = $(this).parent().parent().index();
													$('#orderlist-1 tr:eq('+rowCount2+') td:eq(6) .b').show();
													jQuery.ajax({
    												cache: false,
    												url: "/changestatus",
    												type: "GET",
    												data: "id=" + img_id,
   	 												success: function(data) {
        											 	$('#orderlist-1 tr:eq('+rowCount2+') td:eq(5)').text("Under Preparation");
														
														
        											},  
													
    											}); 
													
													return false;
											  });	
	$('#orderlist-1 .b').bind("click",function(){
											  		var img_id = $(this).attr("id").substring(0,$(this).attr("id").length - 1);
													 
													$(this).hide();
													var rowCount2 = $(this).parent().parent().index();
													$('#orderlist-1 tr:eq('+rowCount2+') td:eq(6) .c').show();
													jQuery.ajax({
    												cache: false,
    												url: "/changestatus",
    												type: "GET",
    												data: "id=" + img_id,
   	 												success: function(data) {
        											 	$('#orderlist-1 tr:eq('+rowCount2+') td:eq(5)').text("Prepared");
														
														
        											},  
													
    											}); 
													
													return false;
											  });	
	
	
	$('#orderlist-1 .c').bind("click",function(){
											  		var img_id = $(this).attr("id").substring(0,$(this).attr("id").length - 1);
													 
												
													$(this).parent().parent().hide();
													
													jQuery.ajax({
    												cache: false,
    												url: "/changestatus",
    												type: "GET",
    												data: "id=" + img_id,
   	 												success: function(data) {
        											 	
														
														
        											},  
													
    											}); 
													
													return false;
											  });	
	
	var rowNumber = 0;
	rowNumber = $('#t4 tr:last').index()
	
	for(var j=0; j<=rowNumber;j++)
	{
		var tempStatus = $('#t4 tr:eq('+j+') td:eq(5)').html();
		if(tempStatus == 2)
		{
			$('#t4 tr:eq('+j+') td:eq(5)').text("Delivered");
		}
	
	}
	$('#shownoti').hide();
	
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
	
	if(number < rowCounter)
	{
    	for(var i=number ;i <= rowCounter - 1;i++)
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

