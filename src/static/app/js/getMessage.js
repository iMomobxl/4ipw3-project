$(document).ready(function () {
        $.ajax({
            url: "/api/get-session-message/",
            type: "GET",
            dataType: "json",
            success: function (response) {
                if (response.message) {
                    showMessage(response.message, response.message_status)
                }
            },
            error: function () {
                showMessage("Erreur lors de la récupération du message.", "warning")
                console.error("Erreur lors de la récupération du message.")
            }
        });
    });