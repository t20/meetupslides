var show_add_meetup = function(event) {
    event.preventDefault();
    $('#add_meetup_wrapper').toggle();
};

var add_meetup = function() {
    var meetup_name = $('#meetup_name', $(this).parent()).val();
    var meetup_city = $('#meetup_city', $(this).parent()).val();
    $.post("/meetup/add", { ajax:1, meetup_name: meetup_name, meetup_city: meetup_city },
        function(data) {
            select_meetup(data);
        });
};

var select_meetup = function(data) {
    var meetup_name = data.name + ' ' + data.city;
    $('#meetup_id').append(
        $('<option></option>').val(data.id).html(meetup_name)
    );
    $('#meetup_id').val(data.id);
    $('#add_meetup_wrapper').hide();
};