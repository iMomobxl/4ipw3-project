document.addEventListener('DOMContentLoaded', () => {
    const rangeInput = document.getElementById('readtime')
    const readtimeBox = document.getElementById('readtime_box')

    const updateReadtimeBox = (value) => {
        readtimeBox.textContent = value
    }

    rangeInput.addEventListener('input', () => {
          updateReadtimeBox(rangeInput.value)
    })

    updateReadtimeBox(rangeInput.value)
});