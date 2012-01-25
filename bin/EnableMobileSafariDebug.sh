MobileSafari_PID=$(ps x | grep "MobileSafari" | grep -v grep | awk '{ print $1 }')

if [ "$MobileSafari_PID" == "" ]; then
  echo "Mobile Safari.app must be running in the Simulator to enable the remote inspector."
else
  
  cat <<EOM | gdb -quiet > /dev/null
  attach $MobileSafari_PID
  p (void *)[WebView _enableRemoteInspector]
  detach
EOM

fi