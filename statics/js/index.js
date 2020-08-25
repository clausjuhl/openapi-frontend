

// The autoComplete.js Engine instance creator
const autoCompletejs = new autoComplete({
  data: {
    src: async function() {
      // Loading placeholder text
      document.querySelector("#autoComplete").setAttribute("placeholder", "Loading...");
      // Fetch External Data Source
      const query = document.querySelector("#autoComplete").value;
      const source = await fetch("https://aarhusiana.appspot.com/autocomplete_v3?t=${query}");
      const data = await source.json();
      // Returns Fetched data
      return data.result;
    }
    // key: ["food", "cities", "animals"],
  },
//   query: {
//     manipulate: function(query) {
//       return query.replace("@pizza", "burger");
//     },
//   },
  trigger: {
    event: ["input", "focusin", "focusout"]
  },
  placeHolder: "Søg i samlingerne",
  searchEngine: "strict",
  highlight: true,
  maxResults: 10,
  selector: "#autoComplete",
  threshold: 3,                        // Min. Chars length to start Engine | (Optional)
  debounce: 300,                       // Post duration for engine to start | (Optional)
  searchEngine: "strict",              // Search Engine type/mode           | (Optional)
  resultsList: {                       // Rendered results list object      | (Optional)
    render: true,
    /* if set to false, add an eventListener to the selector for event type
    "autoComplete" to handle the result */
    container: source => {
        source.setAttribute("id", "food_list");
    },
    destination: document.querySelector("#autoComplete"),
    position: "afterend",
    element: "ul"
    },
    maxResults: 5,                         // Max. number of rendered results | (Optional)
    highlight: true,                       // Highlight matching results      | (Optional)
    resultItem: {                          // Rendered result item            | (Optional)
        content: (data, source) => {
            source.innerHTML = data.match;
        },
        element: "li"
    },
    noResults: () => {                     // Action script on noResults      | (Optional)
        const result = document.createElement("li");
        result.setAttribute("class", "no_result");
        result.setAttribute("tabindex", "1");
        result.innerHTML = "No Results";
        document.querySelector("#autoComplete_list").appendChild(result);
    },
    onSelection: feedback => {             // Action script onSelection event | (Optional)
        console.log(feedback.selection.value.image_url);
    }
});


// Toggle event for search input
// showing & hidding results list onfocus / blur
["focus", "blur"].forEach(function(eventType) {
  const resultsList = document.querySelector("#autoComplete_list");

  document.querySelector("#autoComplete").addEventListener(eventType, function() {
    // Hide results list & show other elemennts
    if (eventType === "blur") {
      action("dim");
      resultsList.style.display = "none";
    } else if (eventType === "focus") {
      // Show results list & hide other elemennts
      action("light");
      resultsList.style.display = "block";
    }
  });
});

