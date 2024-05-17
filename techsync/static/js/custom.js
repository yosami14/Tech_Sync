$(document).ready(function() {
    $('.skill-select').selectize({
        maxItems: 1, // Set maximum items to 1
        plugins: ['remove_button'],
        delimiter: ',',
        persist: false,
        create: function(input) {
            return {
                value: input,
                text: input
            };
        },
        load: function(query, callback) {
            if (!query.length) return callback();
            $.ajax({
                url: '/get_skills/', // URL to fetch skills dynamically
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

