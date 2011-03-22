var activeDone = 'today'


function SwapDone(current) {
    if (current != activeDone) {
        var ctemp = document.getElementById("#yesterday-nav");
        ctemp.addClass('active');
        var actemp = document.getElementById("#today-nav");
        actemp.removeClass('active');
        var cstemp = document.getElementById('#yesterday');
        cstemp.css('display','block');
        var tmp = document.getElementById('#today');
        tmp.css('display','block')
//        $('#' + activeDone + '-nav').removeClass('active');
///        $('#' + current).css('display', 'block');
//        $('#' + activeDone).css('display', 'none');
// $('#' + current.toLowerCase().replace(' ','')).css('display','block');
        activeDone = current;
        return false;
    } else {
        return false;
    }
}
