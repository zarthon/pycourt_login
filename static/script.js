var activeLogin = '';
var activeDone = 'today';
var orderlist = '';
var tempname = '';
var tempprice = '';
var tempid ='';

$(function() {
    $("a").click(function() {this.blur();});
	

    if (activeLogin != '') {
        active = $('#' + activeLogin.toLowerCase());
		
        $("#signup, #login").bind("click", function() { SwapLogin($(this).html());return false; });

        $("#signup-form input:not(.submit), #login-form input:not(.submit),  #done-form textarea").focus(function() { $(this).parent().addClass("focused") });
        $("#signup-form input:not(.submit), #login-form input:not(.submit),  #done-form textarea").blur(function() { $(this).parent().removeClass("focused") });
    }

    $('#no-problem').bind("click", function() { $(this).parent().css('display', 'none'); });
    
    $('#sf a,  a.delete').bind("click", function() {
        if (confirm("Add to Order list?")) { orderlist = orderlist+ $(this).attr('id')+','; $("#orders").val(orderlist);
		var tempparent = $(this).parent();
        $(tempparent).parent().css('background-color', '#F7D4D4');
		var temp = $(this).attr('id') + 'a';
		var temp1 = ('#' + temp); 
		var temp2 = $(this).attr('id') + 'b';
		var temp3 = ('#' + temp2);
		var temp4 = $(this).attr('id') + 'c';
		var temp5 = ('#' + temp4);
		tempid = $(temp1).text();
		tempname = $(temp3).text(); 
		tempprice = $(temp5).text();
		$("table#t1 tr:last").after('<tr><th class="t1">'+ tempname+'</th><th class="t1">' + tempprice + '</th></tr>'); return false;
		/*<th class="t1">' + tempid +'</th>*/
		
		}
		
        else { $(this).parent().parent().css('background-color', '#EEEEEE'); return false; }
    });

    $('#done-list li:last-child').css('border-bottom', '1px solid #E5E5E5');
    $('#add-friend, #add-friend-link').click(function() { $('#add-friend-form').toggle(); });

    $('#friend-input').focus(function() { if ($(this).attr('value') == 'friend\'s username') { $(this).attr('value',''); } });

    
    
    $('#id_description').focus();
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
    current = current.html().toLowerCase().replace(' ','').replace(' ','');
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
