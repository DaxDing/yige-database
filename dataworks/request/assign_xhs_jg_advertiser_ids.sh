#!/bin/sh
# 赋值节点 - 输出聚光 advertiser_id 列表（逗号分隔）
# 下游遍历节点通过 ${dag.foreach.current} 获取当前迭代值
# 调度参数: advertiser_ids="6209396,7152346,..."

echo "${advertiser_ids}"
