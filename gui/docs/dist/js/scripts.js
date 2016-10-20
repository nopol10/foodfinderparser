$(document).ready(function() {
    document.getElementById("search")
        .addEventListener("keyup", function(event) {
            event.preventDefault();
            if (event.keyCode == 13) {
                document.getElementById("searchButton").click();
            }
        });
});