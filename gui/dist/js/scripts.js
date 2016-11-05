$(document).ready(function() {
    document.getElementById("search")
        .addEventListener("keyup", function(event) {
            event.preventDefault();
            if (event.keyCode == 13) {
                document.getElementById("searchButton").click();
            }
        });
});

function searchByName(isAuto) {
    var search = document.getElementById("search").value;
    document.getElementById("search").value = "";
    console.log(isAuto);
    $.ajax({
        type: "POST",
        url: "retrieve.php",
        data: {name: search, auto: isAuto ? 'yes':'no'}
    }).done(function (msg) {
        $('#restaurant-container').html(msg);
    });

}

function showSearchBar() {
    $('#search-panel').slideDown();
}