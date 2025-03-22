$(function () {
    $(document).on('click', '#add-favoris-btn',function () {
        const articleId = $(this).data('article-id')

        $.ajax({
            url: `/favoris/add/${articleId}`,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                if (response.success) {
                    showMessage(response.message, "success")
                    let addFavorisBtn = $('#add-favoris-btn')
                    addFavorisBtn.removeClass('btn-outline-success')
                    addFavorisBtn.addClass('btn-outline-danger')
                    addFavorisBtn.text('Supprimer Favoris')
                    addFavorisBtn.attr('id', 'del-favoris-btn')
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