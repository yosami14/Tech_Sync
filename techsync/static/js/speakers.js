console.log("Speaker Script loaded")
// For Selectize.js in tech stack/tool selection 
$(document).ready(function() {
    $('.selectize-speakers').selectize({
        plugins: ['remove_button'],
        delimiter: ',',
        maxOptions: 3,
        persist: false,
        create: function(input) {
            return {
                value: input,
                text: input
            }
        },
        load: function(query, callback) {
            if (!query.length) return callback();
            $.ajax({
                url: '/get_speakers/', // URL to fetch tags dynamically
                type: 'GET',
                dataType: 'json',
                data: {
                    q: query
                },
                error: function() {
                    callback();
                },
                success: function(res) {
                    callback(res);
                }
            });
        }
    });
});