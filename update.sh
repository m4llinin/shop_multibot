cd /home/shop_multibot || return

git stash

git pull

systemctl restart bot

systemctl status bot