var loadedtime=new Date;
var unixloadedtime=parseInt(loadedtime.getTime()/1000)

var loadUrl = "/checkneworders";

requesttosend = "time="+unixloadedtime

function checkAndNotify()
{
	$("#shownoti").load(loadUrl,requesttosend);
	t = setTimeout("checkAndNotify()",3000)
	return true;
}

$(document).ready(checkAndNotify())
