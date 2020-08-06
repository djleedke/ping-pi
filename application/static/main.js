

/*---------- On Click ----------*/

$('.edit-button').on('click', function(){

    //Modal setup
    $('.modal-title').html('Edit Website');
    $('#modal-save-button').css('display', 'inline-block');
    $('#modal-delete-button').css('display', 'inline-block');
    $('#modal-add-button').css('display', 'none');
    clearModal();
    
    //Fill w/ data
    getWebsiteData($(this));

});

$('.add-button').on('click', function(){

    //Modal setup
    $('.modal-title').html('Add Website');
    $('#modal-add-button').css('display', 'inline-block');
    $('#modal-save-button').css('display', 'none');
    $('#modal-delete-button').css('display', 'none');
    clearModal();

});

$('#modal-add-button').on('click', function(){
    
    addWebsiteData();

}); 

/*---------- AJAX ---------*/

function getWebsiteData(ele){

    $.ajax({
        type : 'POST',
        url : '/get-website-data',
        data : JSON.stringify(ele.data('siteId')),
        contentType: 'application/json; charset=utf-8',
        success: function(result){

            $('#modal-url').val(result.url)

            if(result.job_type === 'interval'){
                $('#modal-job-type').val("Interval")
            } else if (result.job_type === 'cron'){
                $('#modal-job-type').val("Daily")
            }

            $('#modal-hours').val(result.hours);
            $('#modal-minutes').val(result.minutes);
            $('#modal-seconds').val(result.seconds);
            
        }
    });
}

function addWebsiteData(){

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
        url : '/add-website-data',
        data : JSON.stringify(modal_data),
        contentType: 'application/json; charset=utf-8',
        success: function(result){
            console.log(result);
        }
    });
}

/*---------- Miscellaneous ----------*/

function clearModal(){
    $('#modal-url').val('');
    $('#modal-hours').val('');
    $('#modal-minutes').val('');
    $('#modal-seconds').val('');
}