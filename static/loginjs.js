$(function () {
    $('#submit').click(function () {
        console.log($('#login-form').serialize())
        $.ajax({
        //    "{{ url_for('create_account') }}"
            url: '/run_login',
            type: 'POST',
            // Takes data from form of id accountFormID
            data: $('#login-form').serialize(),
            success: (response) => change_url(response),
            error: (error) => {console.log(error)}
        });
    });
});

function change_url(response) {
    document.write('<p>Batchest</p>');
    console.log(response.url)
    window.location.assign(response.url);
}