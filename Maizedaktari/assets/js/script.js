"use strict";

const addEventOnElem = function (elem, type, callback) {
  if (elem.length > 1) {
    for (let i = 0; i < elem.length; i++) {
      elem[i].addEventListener(type, callback);
    }
  } else {
    elem.addEventListener(type, callback);
  }
};
const navbar = document.querySelector("[data-navbar]");
const navTogglers = document.querySelectorAll("[data-nav-toggler]");
const navLinks = document.querySelectorAll("[data-nav-link]");
const overlay = document.querySelector("[data-overlay]");

const toggleNavbar = function () {
  navbar.classList.toggle("active");
  overlay.classList.toggle("active");
};
addEventOnElem(navTogglers, "click", toggleNavbar);

const closeNavbar = function () {
  navbar.classList.remove("active");
  overlay.classList.remove("active");
};

addEventOnElem(navLinks, "click", closeNavbar);

const header = document.querySelector("[data-header]");

window.addEventListener("scroll", function () {
  if (window.scrollY >= 100) {
    header.classList.add("active");
  } else {
    header.classList.remove("active");
  }
});

// CAMERA
function captureFromCamera(event) {
  event.preventDefault(); 

 
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function(stream) {
        
        var video = document.createElement('video');
        video.srcObject = stream;
        document.body.appendChild(video);

        
        video.addEventListener('click', function() {
          var canvas = document.createElement('canvas');
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

          
          var imageUrl = canvas.toDataURL('image/png');
          document.getElementById('image').setAttribute('src', imageUrl);

          
          stream.getTracks().forEach(function(track) {
            track.stop();
          });
          document.body.removeChild(video);
        });
      })
      .catch(function(error) {
        console.error('Error accessing camera:', error);
        
        alert("Sorry, you cannot use the camera of this device. Please upload a photo.");
      });
  } else {
    console.error('Media devices not supported.');
    
    alert("Sorry, your device does not support accessing media devices. Please upload a photo.");
  }
}