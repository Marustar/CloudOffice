// modal.js

$(document).ready(function() {
    $('#document-upload-form').on('submit', function(event) {
        event.preventDefault(); // Prevent form submission

        var form = $(this);
        var formData = new FormData(form[0]);
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                var documentName = response.document_name;

                $('#modal-document-name').text(documentName);
                $('#modal-success').show();
            },
            error: function(xhr, status, error) {
                $('#modal-error').show();
            }
        });
    });

    $('.close-modal').on('click', function() {
        $('.modal').hide();
    });
});
// not for now