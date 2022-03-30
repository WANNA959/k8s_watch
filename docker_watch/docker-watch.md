# centos环境下docker内存消耗

## 环境

- CentOS 7.9.
- Docker version 20.10.14

## 数据 & 图表

脚本检测docker启动1min内的系统内存使用的变化情况

> 主要命令：free -h | grep Mem | awk '{print $3}'

> 详细数据见[memory-change.txt](./memory-change.txt)

**docker启动后，系统内存使用从219M到298M左右稳定，大概占用79M内存**

> docker启动1min内存变化趋势图

![docker-memory](https://tva1.sinaimg.cn/large/e6c9d24ely1h0sa2b1cmuj218g0hs758.jpg)