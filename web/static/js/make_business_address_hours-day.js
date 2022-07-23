let htmlElements = "";
let htmlElementsUp = "";
var getDays = function(arr) {
    if (typeof(arr) == 'object') {
        htmlElements += ' ' + arr['week_days'] + ':  ';
        if (!arr['is_now']) {
            if (htmlElementsUp == ''){
                htmlElementsUp = 'FECHADO';
            }
        } else {
            htmlElementsUp = 'ABERTO';
            if (htmlElementsUp.indexOf('FECHADO')){
                htmlElementsUp = [htmlElementsUp].filter(e => e !== 'FECHADO');
            }
        }
        for (let i = 0; i < arr['hours'].length; i++) {
            if (arr['is_now']) {
                htmlElementsUp += ' até ' + arr['hours'][i][1];
            }
            if (i > 0) {
                console.log(i)
                htmlElements += ' e ';
            }
            htmlElements += arr['hours'][i][0] + ' às ' + arr['hours'][i][1] + '</br>';
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