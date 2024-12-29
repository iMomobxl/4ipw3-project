document.addEventListener('DOMContentLoaded', () => {
    const rangeInput = document.getElementById('readtime')
    const readtimeBox = document.getElementById('readtime_box')
    const resetButton = document.getElementById('reset-button')

    if (rangeInput && readtimeBox && resetButton) {
        const readTime = (value) => {
            readtimeBox.textContent = value
        }

        rangeInput.addEventListener('input', (event) => {
             readTime(rangeInput.value);
        });

        resetButton.addEventListener("click", () => {
            rangeInput.value = rangeInput.getAttribute('value');
            readTime(rangeInput.value)
        })
        rangeInput.addEventListener('click', () => {
           readTime(rangeInput.value);
        });

        readTime(rangeInput.value);
    }
});
