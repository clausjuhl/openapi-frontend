document.addEventListener('click', function (event) {

	// If the clicked element doesn't have the right selector, bail
	if (event.target.classList.contains('bookmark-handler')) {
	    // Don't follow the link
        event.preventDefault();
        // Send request
        send_ajax(event.target);
    }

}, false);

function send_ajax(target) {
    var id_ = target.getAttribute('data-resource-id');
    var action = target.getAttribute('data-action');
    var method, url, data;

    if (action === 'delete-bookmark') {
        method = 'DELETE';
        url = '/users/me/bookmarks/' + id_;
    } else if ( action === 'create-bookmark' ) {
        method = 'POST';
        url = '/users/me/bookmarks';
        data = {
            "resource_id": id_
        };
    }

    // create request object
    var xhr = new XMLHttpRequest();
    var asynchronous = true;
    // open request
    xhr.open(method, url, asynchronous);
    // set ajax headers
    xhr.setRequestHeader('Content-Type', 'application/json; charset=utf-8');
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    // Setup our listener to process completed requests
    xhr.onload = function () {
        // Process our return data
        if (xhr.status >= 200 && xhr.status < 300) {
            // try parse json response
            try {
                var response = JSON.parse(this.responseText);
            } catch (e) {
                console.log(e);
                return false;
            }
            if (!response.error) {
                if (method === 'DELETE') {
                    // If in bookmarklist-view, remove the listitem after deletion 
                    // $('.userpage .bookmark-handler[data-resource-id="' + id_ + '"]').closest('.listitem').slideUp().remove();
                    var handler = document.querySelector('.userpage .bookmark-handler[data-resource-id="' + id_ + '"]');
                    if (handler) {
                        var listitem = handler.closest('.listitem');
                        listitem.classList.add('slideOutUp');
                        listitem.remove();
                    }
                } else if (method === 'POST') {
                    // If in searchresult-view, remove 'bookmark'-icon of the specific listitem
                    var handler = document.querySelector('.searchpage [data-resource-id="' + id_ + '"] .bookmark-handler');
                    if (handler) handler.classList.toggle('hide');
                }
                // If in record-view, toggle 'bookmark'-buttons, no matter method
                var handler = document.querySelectorAll('.resourcepage .bookmark-handler');
                if (handler) {
                    handler.forEach(function(button) {
                        button.classList.toggle('hide');
                    });
                }
            } else {
                console.log(response.error);
            }
        } else {
            // xhr.status > 300
            console.log(this.responseText);
        }
        // Code that should run regardless of the request status
        console.log(this.responseText);
    };
    // send request
    xhr.send(JSON.stringify(data));
}
