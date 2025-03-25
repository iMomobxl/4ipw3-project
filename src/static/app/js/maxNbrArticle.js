$(function () {
    const $nbrArticle = $('#nbrArticle')
    const $maxNbrArticle = $('#maxNbrArticle')

    $maxNbrArticle.on('change', function () {
        $nbrArticle.prop('disabled', $(this).is(':checked'))
    })
})
