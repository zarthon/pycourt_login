var data;
function checkAndNotify()
{
    var rows = document.getElementById("orderlist_1").rows; var cell = rows[rows.length - 1].cells[3];
	tosend = "id="+cell.innerHTML
	jQuery.ajax({
    cache: false,
    url: "/mostrecenttransaction",
    type: "GET",
    data: tosend,
    success: function(data) {
        jQuery('#shownoti').html(data).hide().fadeIn(1500);
        },  
    }); 
    t = setTimeout("checkAndNotify()",3000)
    return true;
}

$(document).ready(function(){
var rows = document.getElementById("orderlist_1").rows; var cell = rows[rows.length - 1].cells[3];
data = "id="+cell.innerHTML

checkAndNotify();
})

