$(function () {
    $('#Submit').click(function () {
        console.log($('#billingInformationID').serialize())
        $.ajax({
            url: '/add_card',
            type: 'POST',
            data: $('#billingInformationID').serialize(),
            success: (response) => $('#billingInformationID').resetForm(),
            error: (error) => {console.log(error)}
        });
    });
});


jQuery.fn.resetForm = function() {
    var $form = $(this);
    $form.find('input:text, input:file, textarea').val('');
    return this;
};
