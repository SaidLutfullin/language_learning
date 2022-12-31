$(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });

    $("#site-search-reset").click(function() {
      $("#site-search").attr("value", "");
      document.getElementById("search-form").submit();
    });

    $("#writte-test").click(function() {
      $("#start-test-button").prop("href", "/test");
    });

    $("#cards").click(function() {
      $("#start-test-button").prop("href", "/cards");
    });
  });