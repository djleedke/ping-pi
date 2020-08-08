
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

//Adds a website to database
$('#modal-add-button').on('click', function(e){
    e.preventDefault();
    if(isModalFormComplete()){
        addWebsite();
    }
}); 

$('#modal-delete-button').on('click', function(e){
    e.preventDefault();
    deleteWebsite();
});

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

    if($('#modal-job-type').val() === 'Daily'){
        if($(this).val() > 23){
            $(this).val(23);
        }
    } else {
        if($(this).val() > 168){
            $(this).val(168); //Capped at 1 week intervals
        }
    }

    //Prevent blank
    if($(this).val() === ''){
        $(this).val(0);
    }

});

$('#modal-minutes').on('input', function(e){

    if($(this).val() > 59){
        $(this).val(59);
    }

    //Prevent blank
    if($(this).val() === ''){
        $(this).val(0);
    }

});

$('#modal-seconds').on('input', function(e){

    if($(this).val() > 59){
        $(this).val(59);
    }

    //Prevent blank
    if($(this).val() === ''){
        $(this).val(0);
    }

});

/*---------- Countdown Timers ----------*/

var next_timer= false;
var restart_timers = [];

$(document).ready(function(){

    $('.ping-countdown').each(function(){
        startCountdownTimer($(this));
    });



});

setInterval(function(){

    if(restart_timers.length > 0){

        for(i = 0; i < restart_timers.length; i++){
            console.log(restart_timers[i]);
            startCountdownTimer(restart_timers[i]);
            restart_timers.shift();
        }
    }

}, 5000);

function startCountdownTimer(ele){

    var timer = new Timer();
    var data = ele.data();

    $.ajax({
        type : 'POST',
        url : '/get-time-til-ping',
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

    //Every second we tick
    timer.addEventListener('secondsUpdated', function (e) {
        ele.html(timer.getTimeValues().toString());
    });

    //Timer completed
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
            console.log(result.hours);
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

function editWebsite(){

    modal_data = createModalDataObject();

    console.log('asd');
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

function leadingZeroes(num, size){
    var s = num + "";
    while(s.length < size) s = "0" + s;
    return s;
}
