<?
require_once("common.php");
if ($valid_ip && isset($_POST['password']) && isset($_POST['url']) && isset($_POST['mobile']) && isset($_POST['email'])) {
 $password = $_POST['password'];
 if (!preg_match("/^[_a-zA-Z0-9-]*$/", $password)) {
  $invalid = true;
 }
 $url = $_POST['url'];
 $mobile = $_POST['mobile'];
 $email = strtolower($_POST['email']);
 if (strlen($password) < 6) {
  $invalid = true;
 }
 if (strlen($url) < 10) {
  $invalid = true;
 }
 if( !preg_match( "/^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,3})$/", $email ) ) {
  $invalid = true;
 }
 if (!preg_match("/^[+]{0,1}[0-9]*$/", $mobile)) {
  $invalid = true;
 }
 if (!$invalid) {
  $smstext = rawurlencode("Your password is \"".$password."\". You should receive URL shortly via email. Br, Futurice");
  $smsurl = "https://backupmaster2.futurice.com:13013/cgi-bin/sendsms?username=kanneluser&password=df89asj89I23hvcxSDasdf3298jvkjc839&to=".$mobile."&text=".$smstext;
  $ch = curl_init($smsurl);
  curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
  curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  $content = curl_exec($ch);
  $smsfail_reason = curl_error($ch);
  
  $headers = "From: noreply@futurice.com\r\n".
             "Reply-To: it@futurice.com\r\n".
             "X-Mailer: futurice-secure-sharing";
  $email_message = "Hi,
We have new file for you:
$url

We sent password to your mobile phone.

Br,
Futurice";
  $emailstat = mail($email, "New file on Futurice file transferring server", $email_message, $headers);
  if ($emailstat) {
   $emailmsg = "Email accepted for delivery.";
  } else {
   $emailmsg = "Sending email failed.";
  }
 }
} else {
 $invalid = true;
}

?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
<title>Futurice Share</title>
<link href="css/default.css" rel="stylesheet" type="text/css" />
</head>
<body>
<div id="header">
        <h1><a href="/">Futurice Share</a></h1>
</div> 
<div id="content">
        <p><a href="<?=$url;?>"><?=$url;?></a> has been created, the password is "<?=$password;?>".</p>


<?
if ($invalid) {
 if (!$valid_ip) {
  ?><p>You can send SMS and email message only from Futurice office.</p><?
 } else {
 ?><p>Nothing was sent. Invalid url, password, email or mobile phone number.</p>

<h2>Try again</h2>

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
 }
} else {
?><ul>
<li>SMS: <?=$content;?></li>
<?if (strlen($smsfail_reason) > 5) {?>
<li>There was an error while sending the SMS message: <?=$smsfail_reason;?></li>
<?}?>
<li><?=$emailmsg;?></li>
</ul>
<?
 
}
?>
</div>
<?require_once("footer.php");?>
</body>
</html> 
