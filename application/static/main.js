
/*---------- On Click ----------*/

//Opens modal to edit website
$('.edit-button').on('click', function(){

    //Modal setup
    $('.modal-title').html('Edit Website');
    $('#modal-save-button').css('display', 'inline-block');
    $('#modal-delete-button').css('display', 'inline-block');
    $('#modal-add-button').css('display', 'none');
    clearModal();
    
    //Fill modal with w/ data
    getWebsiteForModal($(this));

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

//Add website button on modal
$('#modal-add-button').on('click', function(e){
    e.preventDefault();
    if(isModalFormComplete()){
        addWebsite();
    }
}); 

//Delete website button on modal
$('#modal-delete-button').on('click', function(e){
    e.preventDefault();
    deleteWebsite();
});

//Save changes button on modal
$('#modal-save-button').on('click', function(e){
    e.preventDefault();
    editWebsite();
});

/*---------- Keypress ----------*/

$('.time-input').on('keypress', function(e){
    
    //Preventing e, ., -, +
    if(e.keyCode === 101 || e.keyCode === 46 || e.keyCode === 45 || e.keyCode === 43){
        e.preventDefault();
    }

});

/*---------- Validation ----------*/

$('#modal-hours').on('input', function(e){

    //Limiting to 24 hours (23:59:59)
    if($(this).val() > 23){
        $(this).val(23);
    }

    //Prevent blank
    if($(this).val() === ''){
        $(this).val(0);
    }

});

$('#modal-minutes').on('input', function(e){

    //Limiting to 59 minutes max (23:59:59)
    if($(this).val() > 59){
        $(this).val(59);
    }

    //Prevent blank
    if($(this).val() === ''){
        $(this).val(0);
    }

});

$('#modal-seconds').on('input', function(e){

    //Limiting to 59 seconds max (23:59:59)
    if($(this).val() > 59){
        $(this).val(59);
    }

    //Prevent blank
    if($(this).val() === ''){
        $(this).val(0);
    }

});

/*---------- Countdown Timers ----------*/

var restart_timers = [];

//When the document is loaded we start up the timers
$(document).ready(function(){

    //Passing in the td elements to start the countdown in
    $('.ping-countdown').each(function(){
        startCountdownTimer($(this));
    });

});

//This interval checks periodically to see if any timers need to be restarted
setInterval(function(){

    //If we have a restart queued
    if(restart_timers.length > 0){

        for(i = 0; i < restart_timers.length; i++){
            startCountdownTimer(restart_timers[i]);
            restart_timers.shift();
        }
    }

}, 5000);

//Starts a countdown timer for the specified td element
function startCountdownTimer(ele){

    var timer = new Timer();
    var data = ele.data();

    $.ajax({
        type : 'POST',
        url : '/get-seconds-til-ping',
        data : JSON.stringify(data['siteId']),
        contentType: 'application/json; charset=utf-8',
        success: function(result){

            //Initalize timer
            timer.start({
                countdown: true,
                startValues: {seconds:result}
            });
        }
    });

    //Every second the countdown updates
    timer.addEventListener('secondsUpdated', function (e) {
        ele.html(timer.getTimeValues().toString());
    });

    //Timer completed we add the element to an array of timer elements that need to be restarted
    timer.addEventListener('targetAchieved', function (e){
        ele.html('Ping!');
        restart_timers.push(ele);
    });
}

/*---------- AJAX ---------*/

//Gets website data from database
function getWebsiteForModal(ele){

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

            $("#modal").attr('data-site-id', result.id);
            $('#modal-hours').val(result.hours);
            $('#modal-minutes').val(result.minutes);
            $('#modal-seconds').val(result.seconds);
            
        }
    });
}

//Adds website to database
function addWebsite(){

    modal_data = createModalDataObject();

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

//Delete website from database
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

//Updates website in the database
function editWebsite(){

    modal_data = createModalDataObject();

    $.ajax({
        type : 'POST',
        url : '/edit-website',
        data : JSON.stringify(modal_data),
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
    $('#modal-hours').val(0);
    $('#modal-minutes').val(0);
    $('#modal-seconds').val(0);
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

//Pulls all of the info off of the modal and formats it to send to the server
function createModalDataObject(){

    if($('#modal-job-type').val() === 'Interval'){
        job_type = 'interval'
    } else if ($('#modal-job-type').val() === 'Daily'){
        job_type = 'cron'
    }

    var modal_data = {
        id : $('#modal').attr('data-site-id'),
        url : $('#modal-url').val(),
        job_type : job_type,
        hours : $('#modal-hours').val(),
        minutes : $('#modal-minutes').val(),
        seconds : $('#modal-seconds').val()
    }
    return modal_data;
}