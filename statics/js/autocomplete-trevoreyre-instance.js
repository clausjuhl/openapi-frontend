new Autocomplete('#autocomplete', {

  // Search function can return a promise
  // which resolves with an array of results.
  search: input => {
    const url = `https://aarhusarkivet-staging.herokuapp.com/autosuggest?q=${encodeURI(input)}`;

    return new Promise(resolve => {
      if (input.length < 3) {
        return resolve([]);
      }

      fetch(url).
      then(response => response.json()).
      then(data => {
        // resolve(data.query.search);
        resolve(data);
      });
    });
  },

  // Control the rendering of result items.
  // Let's show the title and snippet
  renderResult: (r, props) => {
    const domains = {
      "locations": "sted",
      "people": "person",
      "organisations": "organisation",
      "objects": "objekt",
      "events": "begivenhed"
    };
    let sub_string = domains[r.domain];
    if (sub_string) {
      let sub_array = r.sub_display.split(",");
      r.sub_display = sub_array.filter((i) => i.toLowerCase() !== sub_string).join(",");
    }
    return `
    <li ${props}>
        <a class="autocomplete-result-link" href="/search?${r.domain}=${r.id}">
          <span class="autocomplete-result-label">${r.display}</span>
          <span class="autocomplete-result-sublabel">${r.sub_display}</span>
        </a>
    </li>
  `},

  // What  is to be displayed in input-field before submission
  getResultValue: result => result.display,

  // Add domain and id to a hidden fields name and value-attributes
  // remove name from input-field to keep it from being submittet
  onSubmit: result => {
    if (result) {
      let f = document.querySelector("#autocomplete");
      let hiddenField = document.createElement('input');
      hiddenField.setAttribute("type", "hidden");
      hiddenField.setAttribute("name", result.domain);
      hiddenField.value = result.id;
      f.appendChild(hiddenField);

      let i = document.querySelector("input[name='q']");
      i.removeAttribute("name");
    }
  }
});