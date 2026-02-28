#!/bin/sh
# 赋值节点 - 输出蒲公英 user_id 列表（逗号分隔）
# 下游遍历节点通过 ${dag.foreach.current} 获取当前迭代值
# 调度参数: pgy_user_ids="5cf89d080000000018003029"

echo "${pgy_user_ids}"
