# Elasticsearch-Falcon

Elasticsearch 监控脚本 for Open-Falcon( http://book.open-falcon.org/ )

This project is a fork of Elasticsearch script of serialsito

https://github.com/Wprosdocimo/Elasticsearch-zabbix

These are made available by me under an Apache 2.0 license.

http://www.apache.org/licenses/LICENSE-2.0.html

该脚本只针对ES集群做数据采集监控，相应模板请根据自己实际情况进行设置选择.

# 使用方法

安装依赖

```
# yum install -y python-pbr python-pip python-urllib3 python-unittest2 python-requests
# pip install elasticsearch
```

修改FALCON_HTTP_URL & CLUSTER_NAME 两个变量

 采用agent方式收集
- copy ESFalcon.py 到 /etc/open-falcon/agent/plugin/ 下根据自己采集周期来重命名文件名

 采取crontab
- 例如 */5 * * * * /usr/bin/python /root/ESFalcon.py 2>&1 

# 简述

所有项目是用于监控 Elasticsearch 集群运行情况

主要涉及三大块:

1. Elasticsearch 节点 & 缓存 

2. Elasticsearch 集群 (集群状态，分片级监控，记录数，存储大小等)

3. Elasticsearch 服务 (ES服务状态)

配置模板时应分配给群集状态触发器：
0 = Green (OK)

1 = Yellow (Average, depends on "red")

2 = Red (High)


你可能会想要分配的ElasticSearch群集状态项的值映射

以下是当前监控项清单:

* ES 集群 (11 项)
    - Cluster-wide records indexed per second
    - Cluster-wide storage size
    - ElasticSearch Cluster Status
    - Number of active primary shards
    - Number of active shards
    - Number of data nodes
    - Number of initializing shards
    - Number of nodes
    - Number of relocating shards
    - Number of unassigned shards
    - Total number of records
* ES 服务 (1 项)
    - Elasticsearch service status
* ES 节点 (2 项) ---未完成
    - Node JVM Heap Mem Used
    - Node Storage Size
    - Records indexed per second

# TODO

1.ES 节点级监控
