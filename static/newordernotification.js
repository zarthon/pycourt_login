var flag = 0;
function checkAndNotify()
{
    var rows = document.getElementById("orderlist-1").rows;
	if (rows.length > 0){
		var cell = rows[rows.length - 1].cells[0];
		
		tosend = "id="+cell.innerHTML
		jQuery.ajax({
	    cache: false,
	    url: "/mostrecenttransaction",
	    type: "GET",
	    data: tosend,
	    success: function(data) {
	        jQuery('#shownoti').html(data).show();
    	    },  
	    }); 
		}
	else {
		jQuery.ajax({
	    cache: false,
	    url: "/mostrecenttransaction",
	    type: "GET",
	    data: "id=0",
	    success: function(data) {
			jQuery('#shownoti').html(data).show();
		},
		})
		}
	t = setTimeout("checkAndNotify()",3000)
    return true;
}

$(document).ready(function(){
checkAndNotify();
})



