<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
<title>Futurice Share</title>
<link href="css/default.css" rel="stylesheet" type="text/css" />
</head>
<body>
<!--<br/>-->
<?php
require_once("common.php");
function handleUpload() {
  global $valid_ip;
  if (isset($_GET['token'])) {
   $SAVE_ROOT = "/tmp/futuShare/";
   $SAVE_ROOT_TMP = "/tmp/futuShare_tmp/";
   $WEB_PATH = "/var/www/futuUpload/futuShare/upload/";
   $BASEURL = "https://share.futurice.com/upload/";

   $token_tmp = preg_replace("/(\w+)/", "", $HTTP_GET_VARS['token']);
   if (strlen($token_tmp) != 0) {
    ?>Invalid token.<?
    return;
   }
   $token = $_GET['token'];
   if (strlen($token) < 10) {
    ?>Invalid token. Too short.<?
    return;
   }
   $filename = "/bin/ls";
   while (file_exists($filename)) {
    $shorturl = trim(shell_exec("pwgen -s -B 6 1"));
    $filename =  $WEB_PATH . $shorturl . ".zip";
    mkdir($SAVE_ROOT_TMP.$shorturl, 0700, true);
    $filename_tmp = $SAVE_ROOT_TMP.$shorturl."/files.zip";
   }
   $password = trim(shell_exec("pwgen -s -B 8 1"));
   $url =  $BASEURL . $shorturl . ".zip";
   $uploadpathdir =  $SAVE_ROOT . $token . "/";
   if (!is_dir($uploadpathdir)) {
    echo "No such directory. Internal error.";
    return;
   }

   shell_exec("7z a -tzip ".$filename_tmp." ".$uploadpathdir."*");
#   echo "7z a -tzip ".$filename_tmp." ".$uploadpathdir."*\n";
   shell_exec("7z a -tzip -p" . $password . " " . $filename . " " . $filename_tmp);
#   echo "7z a -tzip -p" . $password . " " . $filename . " " . $filename_tmp."\n";
   shell_exec("rm -rf " . $uploadpathdir);
   shell_exec("rm -f " . $filename_tmp);
   shell_exec("rmdir ".$SAVE_ROOT_TMP.$shorturl);
   ?><div id="header">
        <h1><a href="/">Futurice Share</a></h1>
        </div> 
        <div id="content">
        <p><a href="<?=$url;?>"><?=$url;?></a> has been created, the password is "<?=$password;?>".</p>

        <p><strong>Do not lose this information.</strong> It can not be retrieved again. If you lose address or password, you have to upload same files again.</p>

	<p>Do not deliver ZIP and password on same media. For example DO NOT send ZIP and password on same email message.</p>

<?
if ($valid_ip) {
?>
<h2>Send with email (url) and sms (password)</h2>

<p>Enter recipient's email and mobile phone number here:</p>

<form method="post" action="senddetails.php">
<input type="hidden" name="password" value="<?=$password;?>">
<input type="hidden" name="url" value="<?=$url;?>">
<table>
<tr>
<td>Email:</td>
<td><input type="text" name="email"></td>
<td></td>
</tr>
<tr>
<td>Mobile phone:</td>
<td><input type="text" name="mobile"></td>
<td>(eg +35840123123123)</td>
</tr>
<tr>
<td></td>
<td><input type="submit" value="Send"></td>
<td></td>
</tr>
</table>
</form>

<?
} // if futurice
?>
</div>



<?} else {
   ?>No token set.<?
  }

} // handleUpload
handleUpload();
?>

<?require_once("footer.php");?>
</body>
</html> 
