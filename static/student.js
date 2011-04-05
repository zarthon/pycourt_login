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

$(document).ready(function (){
jQuery.ajax({
	cache: false,
	url: "/pendingorders",
	type: "GET",
	dataType: 'json',
	success: function(json) {
		var count_total_prepared = 0;
		$.each(json, function(i,dish){	
			var dish_id = dish.fields.order_id[0];
			if (dish.fields.status == 2){
				count_total_prepared++;
				}
			if (dish.fields.status > 0){
				alert("Your dish "+dish.fields.dish+"with transaction id "+dish.fields.transaction_id+" has already started preparing. Check order status for more details");
				}
			if (dish.fields.status == 2){
				alert(dish.fields.dish+" is ready for you. "+"Get your ass to "+dish.fields.counterid);
				}
			})
			alert("Total dishes ready for you at the counter: "+count_total_prepared);
		},
	});
});

