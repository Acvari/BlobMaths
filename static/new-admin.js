//<a class="btn btn-primary" role="button" onclick="submit()">Maths</a>


$(function () {
    $('#Submit').click(function () {
        console.log($('#accountFormID').serialize())
        $.ajax({
        //    "{{ url_for('create_account') }}"
            url: '/create_account',
            type: 'POST',
            // Takes data from form of id accountFormID
            data: $('#accountFormID').serialize(),
            success: (response) => $('#accountFormID').resetForm(),
            error: (error) => {console.log(error)}
        });
    });
});

jQuery.fn.resetForm = function() {
    var $form = $(this);

    $form.find('input:text, input:password, input:file, textarea').val('');
    $form.find('select option:selected').removeAttr('selected');
    $form.find('input:checkbox, input:radio').removeAttr('checked');

    return this;
};

//    let account_id = document.getElementById("ID").value;
//    let dob = document.getElementById("DOB").value;
//    let firstname = document.getElementById("FirstName").value;
//    let lastname = document.getElementById("LastName").value;
//    let modules = document.getElementById("Modules").value;
//    let username = document.getElementById("Username").value;
//    let password = document.getElementById("Password").value;


