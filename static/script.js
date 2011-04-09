/* variables definition */

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


// Quantity submission form for dish -- Restricted values from 1-9

$(document).ready(function() {
    $("#qty_no").keydown(function(event) {
	if ( event.keyCode == 46 || event.keyCode == 8 ){ }
        else { 
	    if (event.keyCode < 49 || event.keyCode > 57 ){
            	event.preventDefault(); 
		('#qty_no').text('1');
              	}       
        }

    });
    $('#qty_no').keydown(function() {
	var len = this.value.length;
	if (len >= 1){
	    this.value = this.value.substring(0, 0);
        }
    });
});

// help function slideup and slidedown block

$(document).ready(function(){
    
    $(".accordion pre").hide();
    $(".accordion h3").click(function(){
    $(this).next("pre").slideToggle("normal")
    
    //.siblings("pre:visible").slideUp("normal");
    
    $(this).toggleClass("active");
    
    //$(this).siblings("h3").removeClass("active");
    
    });
});


$(function() {
    
    //highlighting text fields
    $("a").click(function() {this.blur();}); 
	
    //signup-login form toggle on home.html
	
    if (activeLogin != '') {
	active = $('#' + activeLogin.toLowerCase());
	
	// call function swaplogin
        $("#signup, #login").bind("click", function() { 
                                            SwapLogin($(this).html());return false; });
	
	// highlight text boxes
        $("#signup-form input:not(.submit), #login-form input:not(.submit),  #done-form textarea").focus(function() { 
                                            $(this).parent().addClass("focused") });
	// remove text boxes
        $("#signup-form input:not(.submit), #login-form input:not(.submit),  #done-form textarea").blur(function() { 
                                            $(this).parent().removeClass("focused") });
    }

	
    $('#no-problem').bind("click", function() { $(this).parent().slideUp(400); });
    
    // border for last row in Order table
    $('#done-list li:last-child').css('border-bottom', '1px solid #E5E5E5');
	
    // Swapping Counters in Student Menu table   
    $("#done-nav a").bind("click", function() {SwapDone($(this).attr("href"));
					    return false;});

    // Order food from menu to add to cart 
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
					    
					    //menu tab is hidden
					    $(this).parent().parent().fadeOut(400);
				
					    var count_no = c[1].split("%");
					    counter_no = count_no[0];
					    $('#done-nav').hide();
					    $('#menu_t').fadeOut(400,function(){
						    //quantity tab is visible
						    $('#quantity-form').fadeIn(400); 
					    });
					    //hide tabs for seeing counters
					    $('#done-nav').css('display','none');
					    //show tabs for seeing quantity tab
					    $('#tab-qty').css('display','');
					    
					    return false;});
	
		// submitting quantity to add food item to order cart
    $("#qty_sub").bind("click",function(){
					    tempqty = $("#qty_no").attr("value"); 
					    orderlist = orderlist + tempoid +'%'+tempqty+',';
					    $("#orders").val(orderlist);
					    total_price = parseInt(tempqty) * parseInt(tempprice);
					    //max number of orders in one transaction is 10
		                            if(rowCounter < 10){
						rowCounter = rowCounter+1;
						$('#' + rowCounter + '_1').text(tempname);
                        			$('#' + rowCounter + '_2').text(tempprice);
                        			$('#' + rowCounter + '_3').text(tempqty);
						$('#' + rowCounter + '_5').text(counter_no);
						$('#' + rowCounter + '_4').text(total_price);
                        			$('#row_' + rowCounter).fadeIn(1200);
		                            }
									
					    //if orders in cart is already 10
					    else{
						    alert("Maximum Order Limit Reached !!");
					    }
									
					    //First order
					    if(rowCounter > 0 ){
						$('#add-success').slideDown(1200);	
						$('#header-cart').fadeIn(200);
					    }
					    total_final = 0;//value of total orders in order cart
					    //increase value of order cart on addition of food item
					    for(var k=1; k <= rowCounter;k++){
						total_final = total_final + parseInt($('#' + k  + '_4').text());
					    }
					    //variable value to html 
					    $('#total_disp').text(total_final);
					    //	
					    $('#done-nav').css('display','');
					    $('#tab-qty').css('display','none');
					    return false ;});
	
	//bring back menu tab and hide quantity tab
	$("#qty_sub").bind("click",function(){$('#quantity-form').fadeOut(400,function(){
					    $('#menu_t').fadeIn(400);
					    
					    });
	$('#done-nav').show();	
    });
 
	
});

$(document).ready(function(){
    rowCounter = 0;
    //deletion of food item from order cart
    $('#t1 img').bind("click", function(){
	var img_id = '';
	if(rowCounter < 10) {
	    img_id = $(this).attr("id").substring(3,4);
	}
	else {
	    img_id = $(this).attr("id").substring(3,5);
	    
	}
	total_final = total_final - parseInt($('#' + img_id + '_4').text());
	$('#total_disp').text(total_final);
	$('#order_cart').fadeOut(400,function(){
					    slideRows(parseInt(img_id));//calling slideRows function for deletion
					    $('#row_' + rowCounter).hide()});
	$('#order_cart').fadeIn(500,function(){
					    rowCounter = rowCounter - 1; //decrementing the number of rows in order cart
					    rowCounter = parseInt(rowCounter); 
					    //hide order cart if no food items in it
					    if( rowCounter == 0)
						$('#add-success').slideUp(1200,function(){
									$('#header-cart').fadeOut(300)});
					    });						
									
	var temp = orderlist.split(",");
	var tem_orderlist = '';
	//order list update on delete
	for(var j=0;j<temp.length-1;j++){
	    if(j != parseInt(img_id)-1){
		tem_orderlist += temp[j]+',';
	    }
	    else{
		foodlist_deleted = temp[j];
	    }
	} 
								    
	foodlist_deleted = foodlist_deleted.substring(0,7);
	$('#'+foodlist_deleted).parent().parent().fadeIn(400);
	orderlist = tem_orderlist;
	$("#orders").val(orderlist);
	return false;
	
    });
    
    // submitting order cart to vendor
    $('#sub_order').click(function(){
			$('#main').fadeTo(0,0.5);
			if(confirm("Are you sure u want to place this order ? "))//confirmation to place the order
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
    //add a dish facility for vendor
    $('#add_dish').click(function(){
			document.location.href = '/addish';
	
    });
		
    //menu editor for Vendor side
    var counter1 = $('#orderlist-4 tr:last').index();
    for (var l = 0; l <= counter1; l++){
	var temp_availability = $('#orderlist-4 tr:eq('+l+') td:eq(3)').text();

	// avalibility display on UI as database from the counter
	if( temp_availability == "False")
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
			
    //posting values to database on deletion
    $('#orderlist-4 .a').click(function(){
			var len = $(this).attr("id").length
			var id = $(this).attr("id").substring(0,parseInt(len)-1)
			var called_obj = $(this)
			jQuery.ajax({
			    cache: false,
			    url: "/changeavailability",
			    type: "GET",
			    data: "id="+id,
			    error: function(){
				    alert("Network error. Counld not contact server")
			    },
			    success: function(data){
				    called_obj.hide();
				    var rowIndex = called_obj.parent().parent().index()
				    $('#orderlist-4 tr:eq('+(rowIndex)+') td:eq(3)').text("Not Available")
				    $('#'+id+'y').show(); 
			    },
			});
	
    })
			
    //posting values to database on addition of dish
    
    $('#orderlist-4 .b').click(function(){
			var len = $(this).attr("id").length
			var id = $(this).attr("id").substring(0,parseInt(len)-1)
			var called_obj = $(this)
			jQuery.ajax({
			    cache: false,
			    url: "/changeavailability",
			    type: "GET",
			    data: "id="+id,
			    error: function(){
				    alert("Network error. Counld not contact server")
			    },
			    success: function(data){
				    
				    called_obj.hide();
				    var rowIndex = called_obj.parent().parent().index()
				    
				    $('#orderlist-4 tr:eq('+(rowIndex)+') td:eq(3)').text("Available")
				    $('#'+id+'x').show();
			    },
			});
			
	
    })
			
    //status of the dish in vendor side display in UI
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
    
    //posting change status to DB from vendor side
    $('#orderlist-1 .a').bind("click",function(){
	var img_id = $(this).attr("id").substring(0,$(this).attr("id").length - 1);
	var called_obj = $(this); 
	var rowCount2 = $(this).parent().parent().index();
	jQuery.ajax({
	    cache: false,
	    url: "/changestatus",
	    type: "GET",
	    data: "id=" + img_id,
	    error: function() {
		alert("Network error. Counld not contact server");
	    },
	    success: function(data) {
		called_obj.hide();
		$('#orderlist-1 tr:eq('+rowCount2+') td:eq(6) .b').show();
		$('#orderlist-1 tr:eq('+rowCount2+') td:eq(5)').text("Under Preparation");
	    },  
	}); 
	return false;
    });
	
    //posting change status to DB from vendor side
    $('#orderlist-1 .b').bind("click",function(){
	var img_id = $(this).attr("id").substring(0,$(this).attr("id").length - 1);
	var called_obj = $(this)
	var rowCount2 = $(this).parent().parent().index();
	jQuery.ajax({
	    cache: false,
	    url: "/changestatus",
	    type: "GET",
	    data: "id=" + img_id,
	    error: function() {
		alert("Network error. Counld not contact server");
	    },
	    success: function(data) {
		called_obj.hide();	
		$('#orderlist-1 tr:eq('+rowCount2+') td:eq(6) .c').show();
		$('#orderlist-1 tr:eq('+rowCount2+') td:eq(5)').text("Prepared");
	    },  
	}); 
	return false;
	
    });	

    //posting change status to DB from vendor side
    $('#orderlist-1 .c').bind("click",function(){
	var img_id = $(this).attr("id").substring(0,$(this).attr("id").length - 1);
	var called_obj = $(this) 
	jQuery.ajax({
	    cache: false,
	    url: "/changestatus",
	    type: "GET",
	    data: "id=" + img_id,
	    success: function(data) {
		called_obj.parent().parent().hide();
	    },  
	}); 
	return false;
	
    });	
	    
    //updating order history of vendor side according to DB
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
    
    //function for signup-login page on home.html
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

//function for tabs in student home page
function SwapDone(current) {
    current = current.toLowerCase();
    var t = current;

    if (current != activeDone) {
	$('#' + activeDone + '-nav').removeClass('active');
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

//function for removing values from order cart in student homepage
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

