var script = document.createElement('script');
script.src = 'https://code.jquery.com/jquery-3.7.1.min.js';
script.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(script);
$(document).ready(function () {
    function executeMessage(messageCheck) {
        var successMessage = "Your card has been downloaded. Please verify the information.\nThank You!";
        var failureMessage = "Error: Please check your AICF ID and try again.";

        if (messageCheck === 'success') {
            console.log('Alert message found:', successMessage);
        } else if (messageCheck === 'failure') {
            console.log('Alert message found:', failureMessage);
        }
    }

    var messageCheck = $('#alert-message-box').attr('message_attr');
    
    if (messageCheck === 'none') {
        $(window).on('load', function () {
            var interval = setInterval(function () {
                var updatedMessage = $('#alert-message-box').attr('message_attr');
                if (updatedMessage !== 'none') {
                    clearInterval(interval);
                    executeMessage(updatedMessage);
                }
            }, 600);
        });
    } else {
        executeMessage(messageCheck);
    }
});
