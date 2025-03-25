const getArticleDetail = () => {
    $('#tooltip-bubble').addClass('d-none')

    $('.article-info').hover(function (event) {
        let articleId = $(this).data('article-id')
        $.ajax({
            url: `/api/article/${articleId}/`,
            type: 'GET',
            success: function (response) {
                if (!response.error) {
                    console.log('Id:', response.id)
                    console.log('Title:', response.title)
                    console.log('Date:', response.date)
                    console.log('Category:', response.category)
                    console.log('ReadTime:', response.readtime)
                    console.log('Words:', response.nbr_words)
                    $('#tooltip-id').text(response.id)
                    $('#tooltip-date').text(response.date)
                    $('#tooltip-title').text(response.title)
                    $('#tooltip-category').text(response.category)
                    $('#tooltip-readtime').text(response.readtime)
                    $('#tooltip-nbrwords').text(response.nbr_words)

                    $('#tooltip-bubble').removeClass('d-none').css({
                        top: event.pageY + 10,
                        left: event.pageX + 10
                    })
                }
            },
            error: function () {
                showMessage('Erreur lors de la mise a jour des preferences.', 'warning')
                console.error('Erreur lors de la mise a jour des preferences.')
            }
        })
    }, function () {
        $('#tooltip-bubble').addClass('d-none').removeAttr("style")
    })

    $(document).mousemove(function (event) {
        if (!$('#tooltip-bubble').hasClass('d-none')) {
            $('#tooltip-bubble').css({
                top: event.pageY + 10,
                left: event.pageX + 10
            })
        }
    })
}