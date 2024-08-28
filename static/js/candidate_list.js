$(function() {
    $("#age-slider").slider({
        range: true,
        min: 0,
        max: 100,
        values: [20, 40],
        slide: function(event, ui) {
            $("#age_min").val(ui.values[0]);
            $("#age_max").val(ui.values[1]);
        }
    });

    $("#age_min").val($("#age-slider").slider("values", 0));
    $("#age_max").val($("#age-slider").slider("values", 1));
});

$(function() {
    var defaultMin = 0; 
    var defaultMax = 1; 
    $("#age-slider").slider({
        range: true,
        min: 0,
        max: 100,
        values: [defaultMin, defaultMax],
        slide: function(event, ui) {
            $("#age_min").val(ui.values[0]);
            $("#age_max").val(ui.values[1]);
            $("#min-label").text(ui.values[0]);
            $("#max-label").text(ui.values[1]);
        },
        create: function() {
            // Initialize the values on page load
            $("#age_min").val(defaultMin);
            $("#age_max").val(defaultMax);
            $("#min-label").text(defaultMin);
            $("#max-label").text(defaultMax);
        }
    });
});

$(document).ready(function() {
    $('.btn-shortlist').on('click', function() {
        var candidateId = $(this).data('id');
        $.ajax({
            url: '/api/candidates/' + candidateId + '/shortlist/',
            type: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
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
            url: '/api/candidates/' + candidateId + '/reject/',
            type: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
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
});
