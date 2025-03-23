$(function () {
    let currentPage = 1
    let totalPages = 1
    const articlesPerPage = 10

    const fetchArticles = (page = 1) => {
        const csrf_token = $("input[name=csrfmiddlewaretoken]").val()
        const wordTitreArticle = $("#wordTitreArticle").val()
        const wordHookArticle = $("#wordHookArticle").val()
        const wordContentArticle = $("#wordContentArticle").val()
        const minDateArticle = $("#minDateArticle").val()
        const maxDateArticle = $("#maxDateArticle").val()
        let catArticle = $("#catArticle").val()
        if (catArticle === '0')
            catArticle = ''
        let readTimeArticle = $("#readTimeArticle").val()
        if (readTimeArticle === '0')
            readTimeArticle= ''
        const triArticle = $("#triArticle").val()
        const maxNbrArticle = $("#maxNbrArticle").is(":checked") ? true : false;
        let nbrArticle = $("#nbrArticle").val()
        if (maxNbrArticle)
            nbrArticle = ''

        console.log(`titre: ${wordTitreArticle}`)
        console.log(`hook: ${wordHookArticle}`)
        console.log(`content: ${wordContentArticle}`)
        console.log(`date-min: ${minDateArticle}`)
        console.log(`date-max: ${maxDateArticle}`)
        console.log(`category: ${catArticle}`)
        console.log(`readtime: ${readTimeArticle}`)
        console.log(`triArticle: ${triArticle}`)
        console.log(`nbrArticle: ${nbrArticle}`)
        console.log(`maxNbrArticle: ${maxNbrArticle}`)
        let requestData = {
            'wordTitleArticle': wordTitreArticle,
            'wordHookArticle': wordHookArticle,
            'wordContentArticle': wordContentArticle,
            'minDateArticle': minDateArticle,
            'maxDateArticle': maxDateArticle,
            'catArticle': catArticle,
            'readTimeArticle': readTimeArticle,
            'triArticle': triArticle,
            'nbrArticle': nbrArticle,
            'maxNbrArticle': maxNbrArticle,
            'page': page,
            'csrfmiddlewaretoken': csrf_token,
        }
        console.log(requestData)
        $.ajax({
            url: "/api/recherche/",
            type: "POST",
            dataType: "json",
            data: requestData,
            success: (response) => {
                createSearchResults()
                let articles = response.articles
                let totalResults = response.total_results
                totalPages = response.total_pages
                let resultsList = $("#results-list")
                let resultsHeader = $("#results-header")

                resultsList.empty()
                resultsHeader.text(`Résultats de la recherche: (${totalResults} articles)`)
                if (currentPage === 1) {
                    if (totalResults < 1) {
                        showMessage(`Pas de résultat avec les critéres fournis`, `warning`)
                    } else {
                        showMessage(`Résultats de la recherche: (${totalResults} articles)`)
                    }
                }

                if (articles.length === 0) {
                    let item = `<li class='list-group-item'>Aucun résultat trouvé</li>`
                    resultsList.append(item)
                } else {
                    let counter = currentPage * 10 - 9

                    articles.forEach(article => {
                        let shortTitle = article.title.length > 90 ? article.title.substring(0, 87) + "..." : article.title;
                        let listItem = `<a class="article article-info mb-2 rounded-2 link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-0-hover" 
                                                  href="/article/${article.id}" 
                                                  data-article-id="${article.id}"
                                                  target="_self">
                                                    <li class="list-group-item article article-info">
                                                            <strong>${counter}</strong> - ${shortTitle}
                                                    </li>
                                               </a>`
                        resultsList.append(listItem)
                        counter++
                    })
                }

                if (totalResults <= articlesPerPage) {
                    $("#pagination-container").hide()
                } else {
                    $("#pagination-container").show()
                    $("#current-page").text(currentPage)
                    console.log(`currentPage: ${currentPage}`)
                    $("#prev-page").toggleClass("disabled", currentPage === 1)
                    $("#next-page").toggleClass("disabled", currentPage >= totalPages)
                }
            },
            error: () => {
                console.error("Erreur lors de la récupération des résultats")
            }
        })
    }

    const createSearchResults = () => {
        if ($("#search-results").length === 0) {
            let searchResults = `
                <div id="search-results" class="col-10 col-lg-7 m-3">
                    <h5 id="results-header" class="text-center text-black"></h5>
                    <ul id="results-list" class="list-group"></ul>
                </div>`;
            $("#search-box").after(searchResults)
        }
        const searchBox = $("#search-box")
        // met a jour les proprietes bootstrap
        searchBox.removeClass("col-lg-6")
        searchBox.addClass("col-lg-4")

    }

    const removeSearchResults = () => {
        $("#search-results").remove();
        $("#search-box").removeClass("col-lg-4")
        $("#search-box").addClass("col-lg-6")
    }

    $("#wordTitreArticle, #wordHookArticle, #wordContentArticle, #minDateArticle, #maxDateArticle, #catArticle, #readTimeArticle, #nbrArticle, #triArticle, #maxNbrArticle").on("change", () => {
        currentPage = 1
        fetchArticles(currentPage)
    })

    $("#prev-page").on("click", () => {
        if (currentPage > 1) {
            currentPage--
            showMessage(`Page ${currentPage} de la recherche chargé.`)
            fetchArticles(currentPage)
        }
    })

    $("#next-page").on( "click", () => {
        if (currentPage < totalPages) {
            currentPage++
            showMessage(`Page ${currentPage} de la recherche chargé.`)
            fetchArticles(currentPage)
        }
    })

    $("#reset-button").on("click", (event) => {
        event.preventDefault()
        $("#wordTitreArticle").val("")
        $("#wordHookArticle").val("")
        $("#wordContentArticle").val("")
        $("#minDateArticle").val("")
        $("#maxDateArticle").val("")
        $("#catArticle").val("0")
        $("#readTimeArticle").val("0")
        $("#nbrArticle").val("10")
        $("#nbrArticle").removeAttr("disabled")
        $("#triArticle").val("date_art")
        $("#maxNbrArticle").prop("checked", false)
        $("#readTimeBox").text("0")
        $("#results-list").empty()
        $("#results-header").text("")
        $("#pagination-container").hide()
        showMessage('Reset du formulaire de recherche.')
        removeSearchResults()
    })
})

