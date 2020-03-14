# Conda Virtual Environment
```shell
conda create -n rcas python=3.6
source activate rtcas
```

# Tweepy for Twitter Streaming
```shell
pip install tweepy
```

# PRAW for Reddit Streaming
```shell
pip install praw
```

# Kafka
Please refer to this image: 
https://hub.docker.com/r/bitnami/kafka

# Kafka-Python
```shell
pip install kafka-python
```
https://kafka-python.readthedocs.io/en/master/usage.html


# Docker
## Installation
```shell
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker your-user
```

## Aliyun Mirror
```shell
sudo mkdir -p /etc/docker

sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://mj4v472j.mirror.aliyuncs.com"]
}
EOF

sudo systemctl daemon-reload
sudo systemctl restart docker
```


# Add Swap
```shell
sudo dd if=/dev/zero of=/media/swap.img bs=1024 count=4M
mkswap /media/swap.img

# Add this line to /etc/fstab
/media/swap.img swap swap sw 0 0

swapon /media/swap.img
```
**Device** – the first field specifies the mount device. These are usually device filenames. Most distributions now specify partitions by their labels or UUIDs.
**Mount point** – the second field specifies the mount point, the directory where the partition or disk will be mounted. This should usually be an empty directory in another file system.
**File system type** – the third field specifies the file system type.
**Options** – the fourth field specifies the mount options. Most file systems support several mount options, which modify how the kernel treats the file system. You may specify multiple mount options, separated by commas.
**Backup operation** – the fifth field contains a 1 if the dump utility should back up a partition or a 0 if it shouldn’t. If you never use the dump backup program, you can ignore this option.
**File system check order** – the sixth field specifies the order in which fsck checks the device/partition for errors at boot time. A 0 means that fsck should not check a file system. Higher numbers represent the check order. The root partition should have a value of 1 , and all others that need to be checked should have a value of 2.