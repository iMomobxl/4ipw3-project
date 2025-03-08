const showMessage = (message, type = 'success', duration = 5000) => {
    const id = Date.now()
    const $alert = $(`
        <div id="alert-${id}" class="alert alert-${type} alert-dismissible shadow-lg m-0 mb-1" role="alert">
            <strong>${type}:</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `)
    $('#ajax-messages').append($alert)

    setTimeout(() => {
        $alert.addClass('showing')
    }, 10);

    setTimeout(() => {
        $alert.removeClass('showing')
        setTimeout(() => {
            $alert.remove()
        }, 500)
    }, duration);

    // $alert.fadeIn(1000)

    // setTimeout(() => {
    //     $alert.fadeOut(1000, () => {
    //         $alert.remove()
    //         // if ($('#ajax-messages').children().length === 0) {
    //         //     $('header').removeClass('expanded'); // 🟡 Remove expand effect
    //         // }
    //     });
    // }, duration)
}
