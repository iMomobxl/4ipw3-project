$(function () {
    $('#favoris-form').on('submit', function (e) {
        e.preventDefault()

        const articleList = []

        $('input[name="selected_articles"]:checked').each(function () {
            articleList.push($(this).val())
        })

        $.ajax({
            url: "/favoris/",
            type: "POST",
            data: {
                selected_articles: articleList,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                if (response.success) {
                    showMessage(response.message, "success")

                    // Supprime l'article de la liste
                    articleList.forEach(id => {
                        $(`input[value="${id}"]`).closest('li').remove()
                    })

                    // Met a jour le nombre d'article
                    const articles = $('#favoris-list li').length
                    if (articles === 0) {
                        $('#favoris-main-list').remove()
                        $('#nbrArticle').remove()
                        $('#favoris-header').after('<h3></h3>')
                        $('#favoris-header').next('h3').addClass('text-center')
                        $('#favoris-header').next('h3').text('Aucun article dans vos favoris')
                    } else {
                        $('h3').text(`Nombre d'article: ${articles}`)
                    }
                } else if (response.error) {
                    showMessage(response.message, "warning")
                }
            },
            error: function () {
                showMessage("Erreur lors de la suppression des favoris", "warning")
            }
        })
    })
})