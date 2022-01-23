PYTHON101=`which python`
PATHSOURCE=`pwd`
echo $PATH
echo $PYTHON101
echo $SHELL
crontab -r
(crontab -l 2>/dev/null || true ;echo "* * * * * $PYTHON101 $PATHSOURCE/api-p2p-binance.py")  | crontab -
