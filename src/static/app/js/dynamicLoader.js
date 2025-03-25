$(document).on("click", "a.nav-link", function (event) {
    event.preventDefault()
    const url = $(this).attr("href")

    $.get(url, function (data) {
        const dynamicHtml = $('<div>').html(data).find(".dynamic-content").html()

        if (dynamicHtml) {
            $(".dynamic-content").fadeOut(100, function () {
                $(this).html(dynamicHtml).fadeIn(100)
                window.history.pushState(null, "", url)
            })
        } else {
            console.error("Erreur lors du chargement de la page dynamic")
        }
    })
})