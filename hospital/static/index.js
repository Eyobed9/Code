function physicians(name)
{
    // if nothing is chosen
    if (name == "") {
        return;
    } 

    // Fade out the image
    document.getElementById("image").style.opacity = 0;
        
    // create a new ajax object
    var ajax = new XMLHttpRequest();

    ajax.onreadystatechange = function() {
        if (ajax.readyState == 4 && ajax.status == 200) {
           document.getElementById('info').innerHTML = ajax.responseText;
        }
    };

    // open the requested file and transmit the date
    ajax.open('GET', 'hospital/templates/' + name + '.html', true);
    ajax.send();   
}