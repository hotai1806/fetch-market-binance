PYTHON101=`which python`
PATH=`pwd`
echo PATH
echo PYTHON101

( crontab -l | echo "* * * * * PYTHON101 PATH/api-p2p-binance.py" ) | crontab -