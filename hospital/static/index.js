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

const imageContainer = document.getElementById("imageContainer");
const images = imageContainer.getElementsByTagName("img");
let index = 0;

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
// Call the changeImage function initially to show the first image
changeImage();
// Call the changeImage function every 2.5 seconds
setInterval(changeImage, 2500);