(function() {
    const menus = document.querySelectorAll('[data-menu]');
    
    Array.prototype.forEach.call(menus, menu => {
        let heading = menu.previousElementSibling;
        menu.hidden = true;

        // Give each menuheader a toggle button child with a svg plus/minus-icon
        heading.innerHTML = `
        <button aria-expanded="false" aria-haspopup="true" data-menu-button>
            ${heading.innerHTML}
            <svg aria-hidden="true" focusable="false" viewBox="0 0 10 10">
            <rect class="vert" height="8" width="2" y="1" x="4"/>
            <rect height="2" width="8" y="4" x="1"/>
            </svg>
        </button>
        `;

        let btn = heading.querySelector('[data-menu-button]');
        btn.onclick = () => {
            // Cast the state as a boolean
            let expanded = btn.getAttribute('aria-expanded') === 'true' || false;
            // Switch the state
            btn.setAttribute('aria-expanded', !expanded);
            // Switch the content's visibility
            menu.hidden = expanded;
        }
        // btn.onfocus = () => {
        //   heading.style.outline = "1px solid";
        // }
        // btn.onblur = () => {
        //   heading.style.outline = "none";
        // }
    })
  })();