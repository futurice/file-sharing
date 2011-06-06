<?php 
session_id(uniqid().md5(uniqid()));
session_start(); 
require_once("common.php");
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
<title>Futurice Share</title>
<link href="css/default.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="swfupload/swfupload.js"></script>
<script type="text/javascript" src="js/swfupload.queue.js"></script>
<script type="text/javascript" src="js/fileprogress.js"></script>
<script type="text/javascript" src="js/handlers.js"></script>
<script type="text/javascript">
		var swfu;

		window.onload = function() {
			var settings = {
				flash_url : "swfupload/swfupload.swf",
				upload_url: "upload.php",
				post_params: {"PHPSESSID" : "<?php echo session_id(); ?>"},
				file_size_limit : "340 MB",
				file_types : "*",
				file_types_description : "All Files",
				file_upload_limit : 500,
				file_queue_limit : 0,
				custom_settings : {
					progressTarget : "fsUploadProgress",
					cancelButtonId : "btnCancel",
		                        sessionid: "<?php echo session_id(); ?>"
				},
				debug: false,
				prevent_swf_caching: true,
			

				// Button settings
				button_image_url: "images/TestImageNoText_65x29.png",
				button_width: "65",
				button_height: "29",
				button_placeholder_id: "spanButtonPlaceHolder",
				button_text: '<span class="theFont">Upload</span>',
				button_text_style: ".theFont { font-size: 16; }",
				button_text_left_padding: 12,
				button_text_top_padding: 3,
<?/*				button_action : SWFUpload.BUTTON_ACTION.SELECT_FILE,*/?>
				
				// The event handler functions are defined in handlers.js
				file_queued_handler : fileQueued,
				file_queue_error_handler : fileQueueError,
				file_dialog_complete_handler : fileDialogComplete,
				upload_start_handler : uploadStart,
				upload_progress_handler : uploadProgress,
				upload_error_handler : uploadError,
				upload_success_handler : uploadSuccess,
				upload_complete_handler : uploadComplete,
				queue_complete_handler : queueComplete	// Queue plugin event
			};

			swfu = new SWFUpload(settings);
<?/*			swfu.BUTTON_ACTION = SELECT_FILE;*/?>
	     };
	</script>
</head>
<body>
<div id="header">
<h1>Futurice Share</h1>
</div>

<div id="content">
	<h2>Upload</h2>
	<form id="form1" action="index.php" method="post" enctype="multipart/form-data">
		<p>This page allows you to upload files and creates a password-protected zipfile out of them. Maximum filesize is 300MB. You can upload multiple files by pressing shift (or ctrl) when selecting files. ZIP will be automatically created after selecting files.</p>
                        <br/>
			<div class="fieldset flash" id="fsUploadProgress">
			<span class="legend">Files</span>
			</div>
		<div id="divStatus">0 Files Uploaded</div>
			<div>
				<span id="spanButtonPlaceHolder"></span>
				<input id="btnCancel" type="button" value="Cancel All Uploads" onclick="swfu.cancelQueue();" disabled="disabled" style="margin-left: 2px; font-size: 8pt; height: 29px;" />
			</div>

	</form>
</div>
<?require_once("footer.php");?>
</body>
</html>
