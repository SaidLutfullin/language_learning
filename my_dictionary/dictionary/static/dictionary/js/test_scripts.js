$(document).ready(function($) {
    $(document).keypress(function (e) {
        if (e.which == 13) {
                document.getElementById("read_aloud").click();
        }
    });
});