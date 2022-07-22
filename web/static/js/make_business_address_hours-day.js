let htmlElements = "";
let htmlElementsUp = "";
var getDays = function(arr) {
    if (typeof(arr) == 'object') {
        htmlElements += '<div>' + ' ' + arr['week_days'] + ':  ';
        if (!arr['is_now']) {
          htmlElementsUp = '<div>' + 'FECHADO';
        } else {
            htmlElementsUp += '<p> ABERTO </p>' + '<div>';
        }
        for (let i = 0; i < arr['hours'].length; i++) {
            htmlElements += '<i class="far fa-clock" aria-hidden="true"></i> ' + arr['hours'][i][0] + ' às ' + arr['hours'][i][1] + "</div>";
            if (arr['is_now']) {
                htmlElementsUp += ' '  + ' até ' + arr['hours'][i][1] + "</div>";
            }
        }
    }
}
var getDayHours = function(hour_address) {
    let arr = hour_address[0];
    let address = hour_address[1];
    if (typeof(arr) == 'object') {
        for (let i = 0; i < arr.length; i++) {
            getDays(arr[i]);
        }
    }
    document.getElementById('up-' + address).innerHTML = htmlElementsUp;
    document.getElementById('populate-' + address).innerHTML = htmlElements;
}