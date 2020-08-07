document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.menuButton').forEach( function(item) {
        item.addEventListener('click', function() {
            let expanded = this.getAttribute('aria-expanded') === 'true' || false;
            this.setAttribute('aria-expanded', !expanded);
            let menu = this.nextElementSibling;
            menu.hidden = !menu.hidden;
        });
    });

});
// var menuButtons = document.querySelectorAll('.menuButton');

// menuButtons.addEventListener('click', function() {
//     let expanded = this.getAttribute('aria-expanded') === 'true' || false;
//     this.setAttribute('aria-expanded', !expanded);
//     let menu = this.nextElementSibling;
//     menu.hidden = !menu.hidden;
// });