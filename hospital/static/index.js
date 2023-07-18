function physicians(name)
{
    // if nothing is chosen
    if (name == "") {
        return;
    } 

    // Hide the image
    document.getElementById("image").style.display = "none";
        
    // create a new ajax object
    var ajax = new XMLHttpRequest();

    ajax.onreadystatechange = function() {
        if (ajax.readyState == 4 && ajax.status == 200) {
           document.getElementById('info').innerHTML = ajax.responseText;
        }
    };

    // open the requested file and transmit the date
    ajax.open('GET', '/physicians?name=' + name, true);
    ajax.send();   
}