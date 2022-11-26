

$(function () {
    $('#sub').click(function () {
        console.log($('#newcontent').serialize())
        $.ajax({
            url: '/addlink',
            type: 'POST',
            data: $('#newcontent').serialize(),
            success: (response) => $('#newcontent').resetForm(),
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