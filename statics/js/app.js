window.addEventListener('load', function () {
    const skipLinks = document.querySelectorAll('.skipLink');
    for (let i = 0; i < skipLinks.length; i++) {
        skipLinks[i].addEventListener("click", function () {
            id_ = this.getAttribute("href").slice(1);
            document.getElementById(id_).focus();
        })
    }
});