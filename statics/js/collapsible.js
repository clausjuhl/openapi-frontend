/*  
    LINKS
    https://codepen.io/clausjuhl/pen/ExKvZjX
    https://inclusive-components.design/collapsible-sections/

    REQUIREMENTS
    1) A data-collapsible-header (h1-h6) with some descriptive text
    2) A block element (panel) as nextElementSibling from the data-collapsible-header

    TODO
    Combine with accordion.js to get optimal accordion-component as it includes
    keyboard-bindings
*/

(function() {
  // Get all the collapsible headings
  const headings = document.querySelectorAll('[data-collapsible-header]');
  
  Array.prototype.forEach.call(headings, heading => {
    // Width is my experiment.
    let width = false;
    heading.classList.forEach(className => {
      if (className.startsWith('js-until-')) {
        width = className.split("-")[2];
      }
    });
    if (width && window.matchMedia(`(min-width: ${width}em)`).matches) {
      console.log("media-query-match on " + heading.id);
      return;
    }

    let panel = heading.nextElementSibling;
    panel.hidden = true; // hide the panel

    // Give each collapsible header a toggle button child
    // with the SVG plus/minus icon
    heading.innerHTML = `
      <button aria-expanded="false" data-collapsible-trigger>
        <span>${heading.innerHTML}</span>
        <svg aria-hidden="true" focusable="false" viewBox="0 0 10 10">
          <rect class="vert" height="8" width="2" y="1" x="4"/>
          <rect height="2" width="8" y="4" x="1"/>
        </svg>
      </button>
    `;

    // Assign the button
    let btn = heading.querySelector('[data-collapsible-trigger]');
    
    btn.onclick = () => {
      // Cast the state as a boolean
      let expanded = btn.getAttribute('aria-expanded') === 'true' || false;
      // Switch the state
      btn.setAttribute('aria-expanded', !expanded);
      // Switch the content's visibility
      panel.hidden = expanded;
    }
    // btn.onfocus = () => {
    //   heading.style.outline = "1px solid";
    // }
    // btn.onblur = () => {
    //   heading.style.outline = "none";
    // }
  })
})();