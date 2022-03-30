# centos环境下docker内存消耗

## 环境

- CentOS 7.9.
- Docker version 20.10.14

## 数据 & 图表

[脚本](./docker-watch.sh)检测docker启动1min内的系统内存使用的变化情况

> 主要命令：free -h | grep Mem | awk '{print $3}'

> 数据分析

- **docker安装前：186M**

![image-20220330224234359](https://tva1.sinaimg.cn/large/e6c9d24ely1h0sagvidnnj212c09qt9p.jpg)

- **docker安装后，启动前：196M**

![image-20220330224536300](https://tva1.sinaimg.cn/large/e6c9d24ely1h0sak0pju6j211y08q0to.jpg)

- **docker启动后，系统内存使用从196M到282M左右稳定，大概占用86M内存，[详细数据](./memory-change.txt)，如下图**

**从裸机状态到docker启动稳定，内存占用=282-186=96M**

- **启动一个nginx容器，删除**

![image-20220330225721121](https://tva1.sinaimg.cn/large/e6c9d24ely1h0saw9httqj21qg0son24.jpg)

**从裸机状态到docker容器启动后删除，内存占用=314-186=128M**

> docker启动1min内存变化趋势图

![docker-memory](https://tva1.sinaimg.cn/large/e6c9d24ely1h0sa2b1cmuj218g0hs758.jpg)