

$(function () {
    $('#sub').click(function () {
        console.log($('#newquiz').serialize())
        $.ajax({
            url: '/addquiz',
            type: 'POST',
            data: $('#newquiz').serialize(),
            success: (response) => $('#newquiz').resetForm(),
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