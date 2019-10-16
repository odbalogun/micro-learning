
$(document).ready(function(){
    $('#id_enrolled_courses-0-course').change( function(){
        console.log($(this).val());
        console.log('here');

        $.ajax({
            type: 'GET',
            url: '/admin/courses/courses/'+$(this).val()+'/get-course/',
            success: function(response){
                console.log(response);
                $('#id_enrolled_courses-0-course_fee').val(response['course_fee'].toFixed(2));
            }
        });
    });

    $('#id_course').change( function(){
        console.log($(this).val());
        console.log('here');

        $.ajax({
            type: 'GET',
            url: '/admin/courses/courses/'+$(this).val()+'/get-course/',
            success: function(response){
                console.log(response);
                $('#id_course_fee').val(response['course_fee'].toFixed(2));
            }
        });
    });
});