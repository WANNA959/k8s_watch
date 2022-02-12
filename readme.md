## Target

- 系统环境：linux
  k8s部署：单节点集群
  变量因素：pod数量（1~n），需要有说服力，可以间隔采样
  检测数据：k8s各组件内存占用变化趋势（Kubelet、controller，apiserver，proxy和scheduler

- 在固定pod数量下，测一下apiserver随着访问数量增多的内存占用变化趋势

## Solution-arm

> 系统环境

华为云 CentOS 7.6 arm64 4G 2核

> 命令

- 按rsz降序：ps -e -o 'pid,command,rsz,vsz,stime' --sort -rsz | grep apiserver

  - pid进程号

  - comm进程名
  - rsz实际物理内存

  - vsz虚拟内存
    - 进程占用的虚拟内存空间

  - stime进程启动时间

> 初始k8s集群pod分布

![image-20220129174033896](https://tva1.sinaimg.cn/large/008i3skNgy1gyuok46l43j318o0e4776.jpg)

> image: easycode pod增加变化

- 部署pod类型：image:easycode，简单的node.js应用

```javascript
const http = require('http');
const os = require('os');

var requestCount = 0;

console.log("Kubia server starting...");

var handler = function(request, response) {
  console.log("Received request from " + request.connection.remoteAddress);
  response.writeHead(200);
  response.end("This is v3 running in pod " + os.hostname() + "\n");
};

var www = http.createServer(handler);
www.listen(8080); 
```

- replicaSet控制easycode pod数量变化
- service对外暴露接口服务
- watch.sh监控内存变化情况

### 在pod=n下各个组件内存随时间变化

> 命令(eg：pod数量=20)

kubectl scale rs kubia --replicas=20

sh watch.sh watch 20

> 数据文件

pod 数量变化3~40详见watch_file文件夹

```
watch-{n}.txt
```

> 趋势图

pod 数量变化3~40详见images文件夹

```
rsz-{n}.png
vsz-{n}.png
```

![image-20220209123315284](https://tva1.sinaimg.cn/large/008i3skNgy1gz75hquyljj30xc0m8ac2.jpg)

![vsz-20](https://tva1.sinaimg.cn/large/008i3skNgy1gz75htjad5j30xc0m8wg7.jpg)

### 单个组件内存随pod数量变化(取rs扩容3min下数据)

#### rsz(3min)

单位kb

|               | kube-apiserver | kubelet | kube-controller-manager | kube-scheduler | kube-prox |
| ------------- | -------------- | ------- | ----------------------- | -------------- | --------- |
| n=0(初始集群) | 364608         | 112064  | 95040                   | 43008          | 29184     |
| n=3           | 375360         | 107904  | 105472                  | 41984          | 30080     |
| n=10          | 372352         | 108288  | 102400                  | 46976          | 24896     |
| n=20          | 356608         | 103680  | 83328                   | 37888          | 28480     |
| n=30          | 370112         | 108608  | 94464                   | 43648          | 24320     |
| n=40          | 371392         | 109120  | 89536                   | 39104          | 19200     |
| n=50（崩溃    | 314368         | 62272   | ×                       | ×              | 12224     |

#### vsz(3min)

单位kb

|               | kube-apiserver | kubelet | kube-controller-manager | kube-scheduler | kube-prox |
| ------------- | -------------- | ------- | ----------------------- | -------------- | --------- |
| n=0(初始集群) | 1249024        | 1536896 | 823232                  | 754496         | 748160    |
| n=3           | 1245696        | 1535104 | 822720                  | 753984         | 748160    |
| n=10          | 1246208        | 1535360 | 822720                  | 753984         | 748160    |
| n=20          | 1246208        | 1535360 | 822720                  | 753984         | 748160    |
| n=30          | 1246464        | 1535616 | 822720                  | 753984         | 748160    |
| n=40          | 1246720        | 1535616 | 822720                  | 753984         | 748160    |
| n=50（崩溃    | 1178176        | 1995584 | ×                       | ×              | 748160    |

### apiserver随着访问数量增多的内存占用变化趋势

> 初始集群，固定pod数量，jmeter压测100s后内存占用情况
>
> 开放临时端口8080并代理，用以下url、不同的频率请求apiserver
>
> apiserver.sh监控内存变化情况

```
http://121.37.87.211
http://localhost
```

> 命令（n=30为例

jmeter -n -t apiserver.jmx -l ./log-30.jtl -e -o ./html-30

sh apiserver.sh api 30

> 以100s为例，apiserver内存数据

jmeter设置为100s内发送100×n个请求

| 每秒请求数 | kube-apiserver（rsz） | kube-apiserver（vsz） |
| ---------- | --------------------- | --------------------- |
| n=10       | 335296                | 1110272               |
| n=20       | 360064                | 1251712               |
| n=30       | 346176                | 1110272               |
| n=40       | 379968                | 1251712               |
| n=50       | ×                     | ×                     |

> 数据文件

不同频率下apiserver 100s内内存变化数据详见api_data_file文件夹

```
api_{n}.txt
```

> 趋势图

不同频率下apiserver 100s内内存变化折线趋势图详见api_images文件夹

```
{n}.png
```

#### jmeter聚合数据

具体可见jmeter文件夹html-{n}

> n=10

![image-20220208171538915](https://tva1.sinaimg.cn/large/008i3skNgy1gz68182a05j31tm0fyq6d.jpg)

> n=20

![image-20220208150104869](https://tva1.sinaimg.cn/large/008i3skNgy1gz6457trmoj31u80gcwhn.jpg)

> n=30

![image-20220208171603898](https://tva1.sinaimg.cn/large/008i3skNgy1gz681nf3mfj31tu0g277h.jpg)

> n=40

![image-20220208150211393](https://tva1.sinaimg.cn/large/008i3skNgy1gz646cxn43j31tm0fs77f.jpg)

> n=50

- 吞吐量为60时，超出系统最大负荷(主要是cpu资源)，jmeter和内存监控进程卡死

- 查看监控脚本输出的数据文件，发现只记录了前20s的数据，如下
  - 发现和第一个测试pod数量（n=50）超过系统负载类似，apiserver的内存占用不升反降，最终崩溃重启进程

```
1*5s后 -------------------------
31333 kube-apiserver --advertise- 328448 1110272 13:14
26939 sh apiserver.sh api 50       3200 111232 17:17
26945 grep apiserver               2624 110400 17:17
2*5s后 -------------------------
31333 kube-apiserver --advertise- 300736 1110272 13:14
26939 sh apiserver.sh api 50       2880 111232 17:17
32037 grep --color=auto apiserver  2688 110400 17:17
32034 grep apiserver               2624 110400 17:17
3*5s后 -------------------------
31333 kube-apiserver --advertise- 283968 1110272 13:14
32041 grep --color=auto apiserver  1536 110400 17:17
32043 grep apiserver               1536 110400 17:17
26939 sh apiserver.sh api 50        896 111232 17:17
4*5s后 -------------------------
31333 kube-apiserver --advertise- 283968 1110272 13:14
26939 sh apiserver.sh api 50        896 111232 17:17
32062 grep --color=auto apiserver   704 110400 17:20
32056 grep apiserver                640 110400 17:18
5*5s后 -------------------------
```

## Solution_v2-x86_64

> 系统环境

阿里云 CentOS 7.9 x86_64 32G 8核

> 命令

- 按rsz降序：ps -e -o 'pid,command,rsz,vsz,stime' --sort -rsz | grep kube

  - pid进程号

  - comm进程名
  - rsz实际物理内存

  - vsz虚拟内存
    - 进程占用的虚拟内存空间

  - stime进程启动时间

> 初始k8s集群pod分布

![image-20220210141346815](https://tva1.sinaimg.cn/large/008i3skNgy1gz8e0no0boj31cy0negs7.jpg)

> image: nginx pod增加变化

- 部署pod类型：image:nginx

![image-20220210144502905](https://tva1.sinaimg.cn/large/008i3skNgy1gz8ex5h2tzj31al0u0wj7.jpg)

- replicaSet控制nginx pod数量变化
- service对外暴露接口服务
- watch.sh监控内存变化情况
- 每组crontab任务间隔1h

### 在pod=n下各个组件内存随时间变化

> **rs控制pod数量变化 0\~3\~10\~20\~30\~40**

> 命令(eg：pod数量=20)

sh watch.sh watch 20

> 数据文件

pod 数量变化3~40详见watch_file_v2文件夹

```
watch-{n}.txt
```

> 趋势图

pod 数量变化3~40详见images_v2文件夹

```
rsz-{n}.png
vsz-{n}.png
```

![rsz-20](https://tva1.sinaimg.cn/large/008i3skNgy1gz8fztcfcqj30xc0m876b.jpg)

![vsz-20](https://tva1.sinaimg.cn/large/008i3skNgy1gz8fzyee8yj30xc0m80uh.jpg)

### 单个组件内存随pod数量变化(取rs扩容3min下数据)

#### rsz(3min)

单位kb

|               | kube-apiserver | kubelet | kube-controller-manager | kube-scheduler | kube-prox |
| ------------- | -------------- | ------- | ----------------------- | -------------- | --------- |
| n=0(初始集群) |                |         |                         |                |           |
| n=3           |                |         |                         |                |           |
| n=10          | 377236         | 134280  | 121976                  | 57224          | 43332     |
| n=20          | 381908         | 139352  | 126264                  | 57424          | 42568     |
| n=30          | 405876         | 145988  | 123716                  | 57736          | 43428     |
| n=40          | 412212         | 152744  | 125504                  | 57948          | 44112     |

#### vsz(3min)

单位kb

|               | kube-apiserver | kubelet | kube-controller-manager | kube-scheduler | kube-prox |
| ------------- | -------------- | ------- | ----------------------- | -------------- | --------- |
| n=0(初始集群) |                |         |                         |                |           |
| n=3           |                |         |                         |                |           |
| n=10          | 1179688        | 2217128 | 824508                  | 755556         | 748984    |
| n=20          | 1180564        | 2217128 | 824508                  | 755556         | 748984    |
| n=30          | 1180564        | 2217128 | 824764                  | 755556         | 748984    |
| n=40          | 1180564        | 2284780 | 824764                  | 755556         | 749240    |
