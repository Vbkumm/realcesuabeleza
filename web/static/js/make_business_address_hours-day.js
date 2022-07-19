let htmlElements = "";
var getDays = function(arr) {
    if (typeof(arr) == 'object') {
        for (let i = 0; i < arr.length; i++) {

            if (arr[i].is_now != 'false') {
                htmlElements += '<div>' + '<i class="far fa-clock" aria-hidden="true"></i>' + ' ' + arr[i].week_days + ':  ' ;
                    if (arr[i].hours) {
                        for (let f = 0; f < arr[i].hours.length; f++) {
                            htmlElements +=  '  ' + arr[i].hours[f][0] + ' às ' + arr[i].hours[f][1]+ "</div>";
                        }
                    }
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
    document.getElementById('populate-' + address).innerHTML = htmlElements;
}