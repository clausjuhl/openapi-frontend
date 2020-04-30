$(document).ready(function() {

    $(document).on('click', '.bookmark-handler', function(e) {
        e.preventDefault();
        var $this = $(this);
        var id_ = $this.attr('data-resource-id')
        var action = $this.attr('data-action')
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
        } else {
            return false;
        }

        $.ajax({
            type : method,
            url : url,
            dataType: 'json',
            data: JSON.stringify( data ),
            contentType: 'application/json;charset=UTF-8'
        })
        .done(function(resp) {
            if (!resp.error) {
                console.log(resp);
                if (method === 'DELETE') {
                    // If in bookmarklist-view, remove the listitem after deletion 
                    $('.userpage .bookmark-handler[data-resource-id="' + id_ + '"]').closest('.listitem').slideUp().remove();
                } else if (method === 'POST') {
                    // If in searchresult-view, remove 'bookmark'-icon of the specific listitem
                    $('.searchpage [data-resource-id="' + id_ + '"] .bookmark-handler').toggleClass('hide');
                }
                // If in record-view, toggle 'bookmark'-buttons, no matter method
                $('.resourcepage .bookmark-handler').toggleClass('hide');
            }
        })
        .always(function(resp) {
            console.log(resp);
        });
    });
});
