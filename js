// static/app.js
$(document).ready(function() {
    $("#upload-form").submit(function(e) {
        e.preventDefault();

        var formData = new FormData(this);

        $.ajax({
            type: "POST",
            url: "/diagnose",
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                $("#diagnosis-result").text(response.diagnosis);
                $("#result-container").show();
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
