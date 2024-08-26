// Ensures all user information is properly input otherwise alert is raised
function validateForm() {
    var user = document.forms["login"]["user"].value;
    var pass = document.forms["login"]["pass"].value;
    var start = document.forms["login"]["startDate"].value;

    if (user=='' || pass=='' || start=='') {
        alert("Please Fill In All Required Fields");
        return false;
    }
}

// Click event listener function to handle error message dismissal
document.getElementById('dismiss_error').addEventListener('click', function() {
    var div = document.getElementById('error_message');
    div.style.display = 'none';
});
