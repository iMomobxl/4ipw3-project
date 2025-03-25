$(function () {
    $('#minDateArticle').on('change', function () {
        const minDateArticle = $(this).val()
        const maxDateArticle = $('#maxDateArticle')

        if (minDateArticle) {
            maxDateArticle.attr('min', minDateArticle)
        } else {
            maxDateArticle.attr('min', '2023-12-01')
        }
    })
    $('#maxDateArticle').on('change', function () {
        const maxDateArticle = $(this).val()
        const minDateArticle = $('#minDateArticle')

        if (maxDateArticle) {
            minDateArticle.attr('max', maxDateArticle)
        } else {
            minDateArticle.attr('max', '2023-12-31')
        }
    })
})