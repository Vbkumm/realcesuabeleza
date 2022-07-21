let htmlElements = "";
let htmlElementsOpen = "";
var getDays = function(arr) {
    if (typeof(arr) == 'object') {
        htmlElements += '<div>' + '<i class="far fa-clock" aria-hidden="true"></i>' + ' ' + arr['week_days'] + ':  ';
        for (let i = 0; i < arr['hours'].length; i++) {
            if (arr['is_now'] != 'false') {
                htmlElements += '  ' + arr['hours'][i][0] + ' às ' + arr['hours'][i][1] + "</div>";
            } else {
                htmlElementsOpen += '  ' + arr['hours'][i][0] + ' às ' + arr['hours'][i][1] + "</div>";
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
    document.getElementById('open-' + address).innerHTML = htmlElementsOpen;
    document.getElementById('populate-' + address).innerHTML = htmlElements;
}