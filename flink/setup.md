# Standalone

## Install Java
#### 1. Download Java
Download JDK from https://www.oracle.com/java/technologies/javase-jdk11-downloads.html and copy it to your machine
```shell
scp -i /Users/bytedance/Documents/personal/ecs/tcc /Users/bytedance/Documents/personal/software/java/jdk-11.0.6_linux-x64_bin.tar.gz ubuntu@129.204.135.185:~/
```

#### 2. Move the .tar.gz archive binary to the installation directory. Unpack the tarball and install Java.
```shell
ssh ubuntu@129.204.135.185

mkdir -p /usr/java
sudo cp ~/jdk-11.0.6_linux-x64_bin.tar.gz /usr/java/
cd /usr/java
sudo chown ubuntu:ubuntu jdk-11.0.6_linux-x64_bin.tar.gz
sudo tar zxvf jdk-11.0.6_linux-x64_bin.tar.gz
```

#### 3. The Java files are installed in a directory called jre1.8.0_73 in the current directory. In this example, it is installed in the /usr/java/jre1.8.0_73 directory. When the installation has completed, you will see the word Done.

#### 4. Set Environment Variable
Open .bashrc or .bash_profile
```shell
export JAVA_HOME=/usr/java/jdk-11.0.6
export CLASSPATH=.:${JAVA_HOME}/lib
export PATH=$JAVA_HOME/bin:$PATH
```

#### 5. Delete the .tar.gz file if you want to save disk space.


## Install Flink
### Setup SSH Login Without Password
```shell
# Generate keys on each node
ssh-keygen

# Copy id_rsa.pub to every other nodes(including itself) authorized_keys
```

### Download Flink
```shell
cd /opt 
sudo wget https://downloads.apache.org/flink/flink-1.10.1/flink-1.10.1-bin-scala_2.11.tgz


# or
scp -i /Users/bytedance/Documents/personal/ecs/tcc /Users/bytedance/Documents/personal/software/flink-1.10.0/flink-1.10.0-bin-scala_2.11.tgz ubuntu@129.204.135.185:~/

ssh ubuntu@129.204.135.185
sudo cp ~/flink-1.10.0-bin-scala_2.11.tgz /opt
cd /opt
sudo chown ubuntu:ubuntu flink-1.10.0-bin-scala_2.11.tgz
sudo tar zxvf flink-1.10.0-bin-scala_2.11.tgz
```

### Export Env Variable
Open .bashrc or .bash_profile
```
export PATH=$PATH:/opt/flink-1.10.1/bin
```

### Modify flink-conf.yaml
Please see the configuration page for details and additional configuration options.

In particular
* the amount of available memory per JobManager (jobmanager.heap.size),
* the amount of available memory per TaskManager (taskmanager.memory.process.size and check memory setup guide),
* the number of available CPUs per machine (taskmanager.numberOfTaskSlots),
* the total number of CPUs in the cluster (parallelism.default) and
* the temporary directories (io.tmp.dirs)
are very important configuration values.

```shell
##################### conf/flink-conf.yaml #####################
# Referenc: https://blog.csdn.net/lmalds/article/details/53736836
vim  flink/conf/flink-conf.yaml

##配置master节点ip
jobmanager.rpc.address: fmaster

##配置slave节点可用内存，单位MB
taskmanager.heap.mb: 12000m

##配置每个节点的可用slot，1 核CPU对应 1 slot
##the number of available CPUs per machine 
taskmanager.numberOfTaskSlots: 8

##默认并行度 1 slot资源
parallelism.default: 8

##JAVA_HOME
env.java.home: /usr/java/jdk-11.0.6

##################### conf/master #####################
vim masters

fmaster:8081

##################### conf/slaves #####################
vim slaves

fslave1
fslave2

##################### /etc/hostname #####################
Should modify it to the hostname of this node

##################### /etc/hosts #####################
Copy paste to all nodes

192.168.0.106 fmaster
192.168.0.105 fslave1
192.168.0.107 fslave2
```

### Submit Example Job
```shell
# Login to your master
nc -lk 9000

flink run examples/streaming/SocketWindowWordCount.jar --hostname master_hostname --port 9000
```



