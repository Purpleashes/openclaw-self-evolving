#!/usr/bin/env python3
"""
Update the cron configuration file
"""

import json
from datetime import datetime

# Path to the cron config file
cron_config_path = "/root/.openclaw/cron/jobs.json"

# Read the current config
with open(cron_config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Update the secondary iteration review job
for job in config['jobs']:
    if job['id'] == 'secondary-iteration-review':
        # Update the message
        job['payload']['message'] = "请进行二次迭代检查：0. 首先查看前一天晚上的每日分析与迭代报告（projects/self-evolving-agents/daily-reports/day-$(date -d 'yesterday' +'%d'-daily-analysis.md）；1. 查看再往前一天的每日分析与迭代报告；2. 绘制当前迭代全景图；3. 检查架构一致性；4. 检查逻辑连贯性；5. 检查目标一致性；6. 生成检查报告，保存到projects/self-evolving-agents/iteration-reviews/iteration-review-$(date +%Y-%m-%d).md。"
        
        # Update the updatedAtMs
        job['updatedAtMs'] = int(datetime.now().timestamp() * 1000)

# Write the updated config
with open(cron_config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print("✅ Cron configuration updated successfully!")
