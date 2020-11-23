new Autocomplete('#globalSearchform', {
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
  renderResult: (result, props) => `
    <li ${props}>
      <div class="resource-label">
        ${result.display}
      </div>
      <div class="resource-snippet">
        ${result.sub_display}
      </div>
    </li>
  `,
  getResultValue: result => result.display,

  // Open the selected article in a new window
  onSubmit: result => {
    window.open(`https://www.aarhusarkivet.dk/${result.domain}/${result.id}`);
  }
});