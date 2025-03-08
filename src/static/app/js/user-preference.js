$(function() {
    $('#font_color').on('change', function() {
        const font_color = $(this).val()
        updatePreferences('font_color', font_color)
    })

    $('#border_style').on('change', function() {
        const border_style = $(this).val()
        updatePreferences('border_style', border_style)
    })

    $('#home_category').on('change', function() {
        const home_category = $(this).val()
        console.log(`category updated to: ${home_category}`)
        updatePreferences('home_category', home_category)
    })

    $('#background_color').on('change', function() {
        const background_color = $(this).val()
        updatePreferences('background_color', background_color)
    })

    const updatePreferences = (name, value) => {
        $.ajax({
            url: '/user/',
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                [name]: value
            },
            success: function(response) {
                if (response.success) {
                    if (name === 'font_color') {
                        $('body').css('color', value)
                        console.log(`font-color updated to: ${value}`)
                    }
                    if (name === 'border_style') {
                        $('body').css('border', value === 'none' ? 'none' : value + ' solid black')
                        console.log(`border-style updated to: ${value}`)
                    }
                    if (name === 'background_color') {
                        $('body').css('background-color', value)
                        console.log(`background-color updated to: ${value}`)
                    }
                    if (response.message) {
                        showMessage(response.message, 'success')
                    }
                } else {
                    showMessage('Failed to update preferences.', 'warning');
                    console.log('Failed to update preferences')
                }
            },
            error: function() {
                showMessage('Error updating preferences.', 'warning');
                console.log('Error updating preferences')
            }
        })
    }
})