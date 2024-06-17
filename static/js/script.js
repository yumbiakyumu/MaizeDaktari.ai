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


const sections = document.querySelectorAll("[data-section]");

const reveal = function () {
  for (let i = 0; i < sections.length; i++) {

    if (sections[i].getBoundingClientRect().top < window.innerHeight / 2) {
      sections[i].classList.add("active");
    }

  }
}

reveal();
addEventOnElem(window, "scroll", reveal);

// Logout
const logoutButton = document.querySelector('.logout-btn');

if (logoutButton) {
  logoutButton.addEventListener('click', () => {
    fetch('/logout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(() => {
      window.location.reload();
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  });
}

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

// #Diagnostic
function diagnose() {
  const imageInput = document.getElementById('image');
  const file = imageInput.files[0];
  if (!file) {
    alert('Please select an image file');
    return;
  }

  const formData = new FormData();
  formData.append('image', file);

  fetch('/predict', {
    method: 'POST',
    body: formData,
  })
    .then(response => response.json())
    .then(data => {
      window.location.href = `/results?prediction=${encodeURIComponent(data.prediction)}&control_info=${encodeURIComponent(data.control_info)}&image_url=${encodeURIComponent(data.image_url)}`;
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while processing the image.');
    });
}