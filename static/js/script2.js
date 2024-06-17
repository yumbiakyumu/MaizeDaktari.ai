document.addEventListener('DOMContentLoaded', function() {
    var forms = document.querySelectorAll('form');

    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); 

            var formData = new FormData(form);
            var url = form.action;

            fetch(url, {
                method: 'POST',
                body: formData
            })
            .then(function(response) {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Server responded with status ' + response.status);
                }
            })
            .then(function(data) {
              
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else if (data.message) {
                    
                    alert(data.message);
                }
            })
            .catch(function(error) {
                
                console.error(error);
                alert('An error occurred: ' + error.message);
            });
        });
    });
});