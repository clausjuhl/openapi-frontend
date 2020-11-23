window.addEventListener('load', function () {

    const dateForm = document.querySelector('#dateForm');
    if (dateForm) {

        // Replace simple combinated date-fields with 3 input-fields per date
        const initFrom = document.querySelector('#date-from').value;
        const initTo = document.querySelector('#date-to').value;
        const fromFields = `<div class="js-from-fields">
                <div class="inputWrapper">
                    <label for="year-from">År</label>
                    <input id="year-from" class="yearInput" type="text" pattern="^[0-2][0-9][0-9][0-9]$" name="year-from" value="${initFrom ? initFrom.slice(0,4) : ''}" min="500" max="2025">
                </div>     
                <div class="inputWrapper">
                    <label for="month-from">Måned</label>
                    <input id="month-from" class="monthInput" type="text" pattern="^[0-1][0-9]$" name="month-from" value="${initFrom ? initFrom.slice(4,6) : ''}" min="0" max="12">
                </div>
                <div class="inputWrapper">
                    <label for="day-from">Dag</label>
                    <input id="day-from" class="dayInput" type="text" pattern="^[0-3][0-9]$" name="day-from" value="${initFrom ? initFrom.slice(6,8) : ''}" min="0" max="31">
                </div>
            </div>`
        const toFields = `<div class="js-to-fields">
                <div class="inputWrapper">
                    <label for="year-to">År</label>
                    <input id="year-to" class="yearInput" type="text" pattern="^[0-2][0-9][0-9][0-9]$" name="year-to" value="${initTo ? initTo.slice(0,4) : ''}" min="0500" max="2025">
                </div>     
                <div class="inputWrapper">
                    <label for="month-to">Måned</label>
                    <input id="month-to" class="monthInput" type="text" pattern="^[0-1][0-9]$" name="month-to" value="${initTo ? initTo.slice(4,6) : ''}" min="01" max="12">
                </div>
                <div class="inputWrapper">
                    <label for="day-to">Dag</label>
                    <input id="day-to" class="dayInput" type="text" pattern="^[0-3][0-9]$" name="day-to" value="${initTo ? initTo.slice(6,8) : ''}" min="01" max="31">
                </div>
            </div>`
        
        const dateFromFieldset = document.querySelector("#date-from-fieldset");
        dateFromFieldset.removeChild(dateForm.querySelector("#date-from-wrapper"));
        dateFromFieldset.innerHTML += fromFields;

        const datetoFieldset = document.querySelector("#date-to-fieldset");
        datetoFieldset.removeChild(dateForm.querySelector("#date-to-wrapper"));
        datetoFieldset.innerHTML += toFields;

        // Replace hint-text to fit 3-input fields pattern
        const patternHints = dateForm.querySelectorAll('.pattern-hint');
        for (let i = 0; i < patternHints.length; i++) {
            let newText = patternHints[i].textContent;
            patternHints[i].textContent = newText.replace(/-/g, " ");
        }

        // On Submit, format date-inputs
        dateForm.addEventListener("submit", function() {
            let yearFrom = dateForm.querySelector('input[name="year-from"]').value;
            let monthFrom = dateForm.querySelector('input[name="month-from"]').value;
            let dayFrom = dateForm.querySelector('input[name="day-from"]').value;
            let yearTo = dateForm.querySelector('input[name="year-to"]').value;
            let monthTo = dateForm.querySelector('input[name="month-to"]').value;
            let dayTo = dateForm.querySelector('input[name="day-to"]').value;
            let dateFrom = '';
            let dateTo = '';

            // If not 'yearFrom' present, skip whole 'dateFrom'
            if (yearFrom) {
                if (monthFrom) {
                    if (monthFrom.length == 1) {
                        monthFrom = '0' + monthFrom;
                    }
                    dateFrom = yearFrom + monthFrom;
                    if (dayFrom) {
                        if (dayFrom.length == 1) {
                            dayFrom = '0' + dayFrom;
                        }
                    } else {
                        dayFrom = '01';
                    }
                    dateFrom += dayFrom;
                // No month present
                } else {
                    dateFrom = yearFrom + '0101';
                }

                // If 'dateFrom' present, apply new value, else append to form with new 'dateFrom'-value
                let existingDateFrom = dateForm.querySelector('input[name="date-from"]')
                if (existingDateFrom) {
                    existingDateFrom.value = dateFrom;
                } else {
                    let hiddenDateFrom = document.createElement('input');
                    hiddenDateFrom.setAttribute("type", "hidden");
                    hiddenDateFrom.setAttribute("name", "date_from");
                    hiddenDateFrom.value = dateFrom
                    dateForm.appendChild(hiddenDateFrom)
                }
            }

            // If not 'yearTo' present, skip whole 'dateTo'
            if (yearTo) {
                if (monthTo) {
                    if (monthTo.length == 1) {
                        monthTo = '0' + monthTo;
                    }
                    dateTo = yearTo + monthTo;
                    if (dayTo) {
                        if (dayTo.length == 1) {
                            dayTo = '0' + dayTo;
                        }
                    } else {
                        // More complex than dateFrom, as we cannot always use '31'
                        if ([ "01", "03", "05", "07", "08", "10", "12"].includes(monthTo)) {
                            dayTo = '31';
                        } else if (["04", "06", "09", "11"].includes(monthTo)) {
                            dayTo = '30';
                        } else if ((!(yearTo % 4) && yearTo % 100) || !(yearTo % 400)) {
                            dayTo = "29";
                        } else {
                            dayTo = "28";
                        }
                    }
                    dateTo += dayTo;
                } else {
                    dateTo = yearTo + '1231';
                }

                // If 'dateTo' present, apply new value, else append to form with new 'dateTo'-value
                let existingDateTo = dateForm.querySelector('input[name="date-to"]')
                if (existingDateTo) {
                    existingDateTo.value = dateTo;
                } else {
                    let hiddenDateTo = document.createElement('input');
                    hiddenDateTo.setAttribute("type", "hidden");
                    hiddenDateTo.setAttribute("name", "date_to");
                    hiddenDateTo.value = dateTo
                    dateForm.appendChild(hiddenDateTo)
                }
            }

            if (!dateFrom && !dateTo) {
                return false;
            } else {
                // Remove all individual date-part input-fields from submission-array
                // by removing their name-attribute
                dateForm.querySelector('input[name="year-from"]').removeAttribute('name');
                dateForm.querySelector('input[name="month-from"]').removeAttribute('name');
                dateForm.querySelector('input[name="day-from"]').removeAttribute('name');
                dateForm.querySelector('input[name="year-to"]').removeAttribute('name');
                dateForm.querySelector('input[name="month-to"]').removeAttribute('name');
                dateForm.querySelector('input[name="day-to"]').removeAttribute('name');
                return true;
            }
        });
    }
});