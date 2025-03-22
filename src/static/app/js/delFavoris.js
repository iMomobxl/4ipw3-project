$(function () {
    $(document).on('click', '#del-favoris-btn',function () {
        const articleId = $(this).data('article-id')

        $.ajax({
            url: `/favoris/del/${articleId}`,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                if (response.success) {
                    showMessage(response.message, "success")
                    let delFavorisBtn = $('#del-favoris-btn')
                    delFavorisBtn.removeClass('btn-outline-danger')
                    delFavorisBtn.addClass('btn-outline-success')
                    delFavorisBtn.text('Ajouter Favoris')
                    delFavorisBtn.attr('id', 'add-favoris-btn')
                } else if (response.error) {
                    showMessage(response.message, "warning")
                }
            },
            error: function () {
                showMessage("Une erreur est survenue lors de l'ajout aux favoris.", "warning")
            }
        })
    })
})