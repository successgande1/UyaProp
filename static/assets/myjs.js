
    $(document).ready(function() {
        $('#register-form').submit(function(event) {
            event.preventDefault();
            var form = $(this);
            $.ajax({
                url: form.attr('action'),
                type: 'POST',
                data: form.serialize(),
                dataType: 'json',
                success: function(data) {
                    if (data.status === 'success') {
                        window.location.href = data.url;
                    } else if (data.status === 'error') {
                        var errors = data.errors;
                        for (var field in errors) {
                            var field_errors = errors[field];
                            var error_html = '<ul class="errorlist">';
                            for (var i = 0; i < field_errors.length; i++) {
                                error_html += '<li>' + field_errors[i] + '</li>';
                            }
                            error_html += '</ul>';
                            form.find('[name="' + field + '"]').after(error_html);
                        }
                    }
                },
                error: function(xhr, status, error) {
                    console.error(xhr.responseText);
                }
            });
        });
    });

