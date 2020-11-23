function test_searchfilters(details) {
    // Open filtersections root-"details"-tag in grid-view (min 46em)
    // Hide filtersections "summary"-tag when in grid-view
    let summary = details.firstElementChild;

    if (window.matchMedia(`(min-width: 46em)`).matches) {
        details.setAttribute("open", "");
        if (!summary.className.match(/(?:^|\s)sr-only(?!\S)/) ) {
            summary.className += " sr-only";
        }
    } else {
        details.removeAttribute("open");
        summary.className = summary.className.replace( /(?:^|\s)sr-only(?!\S)/g , '' );
    }
}

// Load
window.addEventListener('load', function () {
    const skipLinks = document.querySelectorAll('.skipLink');
    for (let i = 0; i < skipLinks.length; i++) {
        skipLinks[i].addEventListener("click", function () {
            id_ = this.getAttribute("href").slice(1);
            document.getElementById(id_).focus();
        })
    }
    window.filterSectionDetails = document.querySelector("#filterSection-details");
    if (filterSectionDetails) { test_searchfilters(filterSectionDetails); }
});

// Resize
window.addEventListener('resize', function () {
    if (filterSectionDetails) { test_searchfilters(filterSectionDetails); }
});