$(document).ready(function(){
    $.ajax({
        type: "GET",
        url: "/../market/",
        data: {
            'categorySelect': $('#categorySelect option:selected').text(),
        },
        cache : false,
        success: function(rsp) {
    
        },
        error: function(xhr) {
            //Do Something to handle error
        }
    });
    });

