function handleFormSubmit(evt) {


	var textArea = $("#proj_number");
	var num = textArea.val();

	// Reset the message container to be empty
	textArea.val("");
}



// function displayResultStatus(resultMsg) {
// 	var notificationArea = $("#sent-result");
// 	notificationArea.text(resultMsg);
// 	if(resultMsg === "Your message is empty" ||
// 		resultMsg === "You did not specify a message to set."){
// 		notificationArea.removeClass("alert-info").addClass("alert-danger");
// 	}
// 	else {notificationArea.addClass("alert-info").removeClass("alert-danger");}
// 	notificationArea.slideDown(function () {

// 		var self = this;
// 		setTimeout(function () {
// 		$(self).slideUp();
// 		}, 2000);
// 	});
// }