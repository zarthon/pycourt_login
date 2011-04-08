function foodlistfilter (phrase, _id){
	var words = phrase.value.toLowerCase().split(" ");
	var table = document.getElementById(_id);
	var ele;
	for (var r = 0; r < table.rows.length; r++){
		ele = table.rows[r].innerHTML.replace(/<[^>]+>/g,"");
		var displayStyle = 'none';
		for (var i = 0; i < words.length; i++) {
			if (ele.toLowerCase().indexOf(words[i])>=0)
				displayStyle = '';
			else {
				displayStyle = 'none';
				break;
			}
		}
		table.rows[r].style.display = displayStyle;
	}
}
var prev_row = ""; 
function checkPendingOrders(){
	
	jQuery.ajax({
	cache: false,
	url: "/pendingorders",
	type: "GET",
	dataType: 'json',
	success: function(json){ 
		var row_shown = "";
		var count_total_prepared = 0;
		$.each(json, function(i,dish){
			var dish_id = dish.fields.order_id[0];
			row_shown = row_shown + "<tr>";
			row_shown = row_shown+'<td class="t1">'+dish.fields.dish+'</td class="t1">';
			if (dish.fields.status == 0){
				row_shown = row_shown+'<td class="t1">In Queue ('+ dish.fields.quantity +')</td class="t1">';
				}
			if (dish.fields.status == 1){
				row_shown = row_shown+'<td class="t1">Under Preparation</td class="t1">';
				}
			if (dish.fields.status == 2){
				row_shown = row_shown + '<td class="t1">Prepared</td class="t1">';
				}
			row_shown = row_shown+'<td class="t1">' + dish.fields.counterid + '</td class="t1">';
			row_shown = row_shown + "</tr>";
			$("#notify_table").html(row_shown);
			})
			if (prev_row != row_shown && prev_row != ""){
				$("#pastmonth-nav").css('color','red');
				}
			prev_row = row_shown;

		},
	});
	t = setTimeout("checkPendingOrders()",3000);
	};

$(document).ready(function (){
$("#pastmonth-nav").click(function (){
	$(this).css('color','#8D8D8D');
});
checkPendingOrders();
});


