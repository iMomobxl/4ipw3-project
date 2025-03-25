$(function () {
    const $rangeInput = $('#readTimeArticle')
    const $readTimeBox = $('#readTimeBox')
    // const $nbrArticle = $('#nbrArticle')
    // const $maxNbrArticle = $('#maxNbrArticle')

    const updateReadtimeBox = (value) => {
        $readTimeBox.text(value)
    }

    updateReadtimeBox($rangeInput.val())

    $rangeInput.on('input', function () {
        updateReadtimeBox($(this).val())
    })

    // $maxNbrArticle.on('change', function () {
    //     $nbrArticle.prop('disabled', $(this).is(':checked'))
    // })
})
