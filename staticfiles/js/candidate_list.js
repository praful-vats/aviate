$(document).ready(function() {
    // Initialize the Age Slider
    var defaultMin = 0;
    var defaultMax = 100;
    $("#age-slider").slider({
        range: true,
        min: defaultMin,
        max: defaultMax,
        values: [0, 100],
        slide: function(event, ui) {
            $("#age_min").val(ui.values[0]);
            $("#age_max").val(ui.values[1]);
            $("#min-label").text(ui.values[0]);
            $("#max-label").text(ui.values[1]);
        },
        create: function() {
            $("#age_min").val($("#age-slider").slider("values", 0));
            $("#age_max").val($("#age-slider").slider("values", 1));
            $("#min-label").text($("#age-slider").slider("values", 0));
            $("#max-label").text($("#age-slider").slider("values", 1));
        }
    });

    // Handle form submission via AJAX
    $('#search-form').on('submit', function(event) {
        event.preventDefault();

        $.ajax({
            url: $(this).attr('action'),
            type: 'GET',
            data: $(this).serialize(),
            success: function(data) {
                // Replace the table content with the new results
                $('table tbody').html($(data).find('table tbody').html());
                $('.pagination').html($(data).find('.pagination').html());
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });

    // Shortlist and Reject AJAX Calls
    $('.btn-shortlist').on('click', function() {
        var candidateId = $(this).data('id');
        $.ajax({
            url: '/api/status/' + candidateId + '/shortlist/',
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                $('#status-' + candidateId).text('Shortlisted');
                $('.btn-shortlist[data-id="' + candidateId + '"]').hide();
                $('.btn-reject[data-id="' + candidateId + '"]').hide();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });

    $('.btn-reject').on('click', function() {
        var candidateId = $(this).data('id');
        $.ajax({
            url: '/api/status/' + candidateId + '/reject/',
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                $('#status-' + candidateId).text('Rejected');
                $('.btn-shortlist[data-id="' + candidateId + '"]').hide();
                $('.btn-reject[data-id="' + candidateId + '"]').hide();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
