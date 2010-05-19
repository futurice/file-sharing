<?
$futurice_net = array();
$futurice_net[] = "/^10\.4\./";
$futurice_net[] = "/^10\.1\./";
$valid_ip = false;
foreach ($futurice_net as $v) {
  if (preg_match($v, $_SERVER['REMOTE_ADDR'])) {
   $valid_ip = true;
   break;
  }
}
?>
