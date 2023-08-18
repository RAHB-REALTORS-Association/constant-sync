document.addEventListener('DOMContentLoaded', function() {
    fetch('/is_authenticated')
        .then(response => response.json())
        .then(data => {
            if (data.authenticated) {
                document.getElementById('authButton').style.display = 'none';
                document.getElementById('syncForm').style.display = 'block';
            }
        });
});
