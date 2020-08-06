

/*---------- On Click ----------*/

//Opens modal to edit website
$('.edit-button').on('click', function(){

    //Modal setup
    $('.modal-title').html('Edit Website');
    $('#modal-save-button').css('display', 'inline-block');
    $('#modal-delete-button').css('display', 'inline-block');
    $('#modal-add-button').css('display', 'none');
    clearModal();
    
    //Fill w/ data
    getWebsite($(this));

});

//Opens modal to add website
$('.add-button').on('click', function(){

    //Modal setup
    $('.modal-title').html('Add Website');
    $('#modal-add-button').css('display', 'inline-block');
    $('#modal-save-button').css('display', 'none');
    $('#modal-delete-button').css('display', 'none');
    clearModal();

});

//Adds a website to database
$('#modal-add-button').on('click', function(){
    
    if(isModalFormComplete()){
        addWebsite();
    }

}); 

$('#modal-delete-button').on('click', function(){

    deleteWebsite();

})

/*---------- AJAX ---------*/

//Gets website data from database
function getWebsite(ele){

    $.ajax({
        type : 'POST',
        url : '/get-website',
        data : JSON.stringify(ele.data('siteId')),
        contentType: 'application/json; charset=utf-8',
        success: function(result){

            $('#modal-url').val(result.url)

            if(result.job_type === 'interval'){
                $('#modal-job-type').val("Interval")
            } else if (result.job_type === 'cron'){
                $('#modal-job-type').val("Daily")
            }
            console.log(result.id);
            $("#modal").attr('data-site-id', result.id);
            $('#modal-hours').val(result.hours);
            $('#modal-minutes').val(result.minutes);
            $('#modal-seconds').val(result.seconds);
            
        }
    });
}

//Adds website to database
function addWebsite(){

    if($('#modal-job-type').val() === 'Interval'){
        job_type = 'interval'
    } else if ($('#modal-job-type').val() === 'Daily'){
        job_type = 'cron'
    }

    modal_data = {
        url : $('#modal-url').val(),
        job_type : job_type,
        hours : $('#modal-hours').val(),
        minutes : $('#modal-minutes').val(),
        seconds : $('#modal-seconds').val()
    }

    $.ajax({
        type : 'POST',
        url : '/add-website',
        data : JSON.stringify(modal_data),
        contentType: 'application/json; charset=utf-8',
        success: function(result){
            location.reload();
        }
    });
}

function deleteWebsite(){

    $.ajax({
        type : 'POST',
        url : '/delete-website',
        data : $('#modal').attr('data-site-id'),
        contentType: 'application/json; charset=utf-8',
        success: function(result){
            location.reload();
        }
    });

}

/*---------- Miscellaneous ----------*/

//Clears the modal input values
function clearModal(){
    $('#modal-url').val('');
    $('#modal-hours').val('');
    $('#modal-minutes').val('');
    $('#modal-seconds').val('');
    $("#modal").attr('data-site-id', '');
}

//Returns true if modal form fields are all filled out
function isModalFormComplete(){

    if($('#modal-url').val() !== '' &&
        $('#modal-hours').val() !== '' &&
        $('#modal-minutes').val() !== '' &&
        $('#modal-seconds').val() !== ''){
        return true
    } else {
        return false
    }

}