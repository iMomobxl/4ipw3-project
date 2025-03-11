document.addEventListener('DOMContentLoaded', () => {
    const rangeInput = document.getElementById('readTimeArticle')
    const readTimeBox = document.getElementById('readTimeBox')

    const updateReadtimeBox = (value) => {
        readTimeBox.textContent = value
    }

    rangeInput.addEventListener('input', () => {
          updateReadtimeBox(rangeInput.value)
    })

    updateReadtimeBox(rangeInput.value)

    const nbrArticle = document.getElementById('nbrArticle');
    const maxNbrArticle = document.getElementById('maxNbrArticle');

    maxNbrArticle.addEventListener('change', () => {
        nbrArticle.disabled = maxNbrArticle.checked;
    });
});