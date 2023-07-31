window.addEventListener('load', function() {
    var contentElements = document.getElementsByClassName('main-content');
    for (var i = 0; i < contentElements.length; i++) {
        contentElements[i].style.display = 'block';
      }
  });

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

document.addEventListener("DOMContentLoaded", function() {
    const imageContainer = document.getElementById("imageContainer");
    const images = imageContainer.getElementsByTagName("img");
    let index = 0;
    changeImage();


    function changeImage() {
    // Hide all images
    for (let i = 0; i < images.length; i++) {
        images[i].style.display = "none";
    }
        // increment the index
        index = (index + 1) % images.length;

        // Show the next image
        images[index].style.display = "block";
    }

    // Call the changeImage function every 2.5 seconds
    setInterval(changeImage, 4500);
});


document.addEventListener("DOMContentLoaded", function() {
    document.addEventListener("click", function(event) {
        var target = event.target;
        if (target.matches("#single")) {
            window.location.href = "/single";
        } else if (target.matches("#double")) {
            window.location.href = "/double";
        } else if (target.matches("#multiple")) {
            window.location.href = "/multiple";
        }
    });
});