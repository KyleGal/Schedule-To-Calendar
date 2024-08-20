function validateForm() {
    var user = document.forms["login"]["user"].value;
    var pass = document.forms["login"]["pass"].value;
    var start = document.forms["login"]["startDate"].value;

    if (user=='' || pass=='' || start=='') {
        alert("Please Fill In All Required Fields");
        return false;
    }
}
