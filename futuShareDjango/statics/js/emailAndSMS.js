$(function(){

//Send email and sms
$("#sendButton").click(function(){

	//Disable the send button so the user can't send again before we're done'
	$(this).attr('disabled', 'disabled'); 
	
	var that = $(this);

	var formstatus = $('#send-status');
	var form = $('#send-form');
	
	formstatus.html('<p>Sending... </p>')
	
	formstatus.html('');
	
	if (form.find("input#email").val() == ''){
		formstatus.append('<p class="error">No email address.</p>');
		that.removeAttr('disabled'); //Enable sending again

	} else if (form.find("input#sms").val() == '+358'
		|| form.find("input#sms").val() == ''){
		formstatus.append('<p class="error">No phone number.</p>');
		that.removeAttr('disabled'); //Enable sending again
		
	} else {
	
		var password = $("#pass").text();
		var file = $("#file").text();
		var email = $("#email").val();
		var phone = $("#sms").val().replace(/ /g,''); //replace spaces in number
	
		form.hide();
		
		//Send the email and sms
		$.post('/futushare/send/', { file : file, email : email, phone : phone, password : password}, function(response) {

  				if (response == 'DONE'){
  					formstatus.html('<p>The messages were sent successfully.</p>');
					$('#email').val('');
					$('#sms').val('+358');
  				} else if (response == 'BADEMAIL'){
  					formstatus.prepend('<p class="error">There was an error in the email address. Nothing was sent.</p>');
  				} else if (response == 'BADPHONE'){
  					formstatus.prepend('<p class="error">There was an error in the phone number. Nothing was sent.</p>');
  				} else if (response == 'SMSFAIL'){
  					formstatus.prepend('<p class="error">There was an error when sending the SMS. Nothing was sent.</p>');
  				} else if (response == 'EMAILFAIL'){
  					formstatus.prepend('<p class="error">There was an error when sending the email.<br>The SMS was sent successfully.</p>');
  				}
  			
  			that.removeAttr('disabled');//Enable sending again
		});
		
		form.show(); //Show the form
		
	}
});

});

