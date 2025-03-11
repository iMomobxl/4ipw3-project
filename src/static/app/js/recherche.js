$(document).ready(function () {
    let currentPage = 1
    let totalPages = 1
    const articlesPerPage = 10

    const fetchArticles = (page = 1) => {
        const csrf_token = $("input[name=csrfmiddlewaretoken]").val()
        const wordTitreArticle = $("#wordTitreArticle").val()
        const wordHookArticle = $("#wordHookArticle").val()
        const wordContentArticle = $("#wordContentArticle").val()
        const dateArticle = $("#dateArticle").val()
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
        console.log(`date: ${dateArticle}`)
        console.log(`category: ${catArticle}`)
        console.log(`readtime: ${readTimeArticle}`)
        console.log(`triArticle: ${triArticle}`)
        console.log(`nbrArticle: ${nbrArticle}`)
        console.log(`maxNbrArticle: ${maxNbrArticle}`)
        let requestData = {
            'wordTitleArticle': wordTitreArticle,
            'wordHookArticle': wordHookArticle,
            'wordContentArticle': wordContentArticle,
            'dateArticle': dateArticle,
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
                totalPages = Math.ceil(totalResults / articlesPerPage)
                let resultsList = $("#results-list")
                let resultsHeader = $("#results-header")

                resultsList.empty()
                resultsHeader.text(`Résultats de la recherche: (${totalResults} articles)`)

                if (articles.length === 0) {
                    let item = `<li class='list-group-item'>Aucun résultat trouvé</li>`
                    resultsList.append(item)
                } else {
                    let counter = currentPage * 10 - 9

                    articles.forEach(article => {
                        let shortTitle = article.title.length > 90 ? article.title.substring(0, 87) + "..." : article.title;
                        let listItem = `<a class="mb-2 rounded-2 link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-0-hover" 
                                                  href="/article/${article.id}" 
                                                  target="_self">
                                                    <li class="list-group-item article" 
                                                        data-article-id="${article.id}">
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
                getArticleDetail()
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
        searchBox.removeClass("col-lg-6")
        searchBox.addClass("col-lg-4")

    }

    const removeSearchResults = () => {
        $("#search-results").remove();
        $("#search-box").removeClass("col-lg-4")
        $("#search-box").addClass("col-lg-6")
    }

    const createPagination = () => {
        let navPagination = `
            <nav id="pagination-container" style="display: none;">
                <ul class="pagination justify-content-center mt-3">
                    <li class="page-item disabled" id="prev-page">
                        <a class="page-link icon-link icon-link-hover">
                            <svg class="bi" aria-hidden="true"><use xlink:href="#arrow-left"></use></svg>
                            Précédent
                        </a>
                    </li>
                    <li class="page-item active"><a class="page-link" id="current-page" >1</a></li>
                    <li class="page-item" id="next-page">
                        <a class="page-link icon-link icon-link-hover">
                            Suivant
                            <svg class="bi" aria-hidden="true"><use xlink:href="#arrow-right"></use></svg>
                        </a>
                    </li>
                </ul>
            </nav>`
    }

    $("#wordTitreArticle, #wordHookArticle, #wordContentArticle, #dateArticle, #catArticle, #readTimeArticle, #nbrArticle, #triArticle, #maxNbrArticle").on("change", () => {
        currentPage = 1
        fetchArticles(currentPage)
    })

    $("#prev-page").on("click", () => {
        if (currentPage > 1) {
            currentPage--
            fetchArticles(currentPage)
        }
    })

    $("#next-page").on( "click", () => {
        if (currentPage < totalPages) {
            currentPage++
            fetchArticles(currentPage)
        }
    })

    $("#reset-button").on("click", (event) => {
        event.preventDefault()

        $("#wordTitreArticle").val("")
        $("#wordHookArticle").val("")
        $("#wordContentArticle").val("")
        $("#dateArticle").val("")
        $("#catArticle").val("0")
        $("#readTimeArticle").val("0")
        $("#nbrArticle").val("10")
        $("#triArticle").val("date_art")
        $("#maxNbrArticle").prop("checked", false)

        $("#results-list").empty()
        $("#results-header").text("")
        $("#pagination-container").hide()
        removeSearchResults()
    })
})

