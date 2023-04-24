// modal.js

// Wait for the DOM to load
$(document).ready(function() {
    // Show modal when file upload is successful
    $('#document-upload-form').on('submit', function(event) {
        event.preventDefault(); // Prevent form submission

        // Perform AJAX form submission
        var form = $(this);
        var formData = new FormData(form[0]);
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Parse JSON response
                var documentName = response.document_name;

                // Show success modal with uploaded document name
                $('#modal-document-name').text(documentName);
                $('#modal-success').show();
            },
            error: function(xhr, status, error) {
                // Show error modal with error message
                $('#modal-error').show();
            }
        });
    });

    // Close modal when close button is clicked
    $('.close-modal').on('click', function() {
        $('.modal').hide();
    });
});