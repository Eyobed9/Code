function physicians(name)
{
    // if nothing is chosen
    if (name == " ") {
        return;
    }

    // create a new ajax object
    var ajax = new XMLHttpRequest();

    ajax.onreadystatechange = function() {
        if (ajax.readyState == 4 && ajax.status == 200) {
           $('#info').html(ajax.responseText);
        }
    };

    // open the requested file and transmit the date
    ajax.open('GET', name + '.html', true)
    ajax.send();   
}