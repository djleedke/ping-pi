

$('.site-button').on('click', function(){


    $.ajax({
        type : 'POST',
        url : '/get-website-data',
        data : JSON.stringify($(this).data('siteId')),
        contentType: 'application/json; charset=utf-8',
        success: function(result){
            $('#edit-site-url').val(result.url)

            if(result.job_type === 'interval'){
                $('#edit-site-job-type').val("Interval")
            } else if (result.job_type === 'cron'){
                $('#edit-site-job-type').val("Daily")
            }
            
        }

    });
    
});