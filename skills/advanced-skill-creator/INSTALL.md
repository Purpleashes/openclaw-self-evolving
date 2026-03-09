
# Advanced Skill Creator - 安装说明

## 技能信息
- **名称**: advanced-skill-creator
- **来源**: 🦞 claw123.ai 龙虾技能大全
- **功能**: 高级 OpenClaw 技能创建处理程序，执行官方 5 步研究流程

## 安装步骤

由于系统安全限制，需要手动完成安装：

### 方法一：手动复制（推荐）

```bash
# 1. 创建技能目录
mkdir -p ~/.openclaw/skills/advanced-skill-creator

# 2. 复制技能文件
cp /root/.openclaw/workspace/skills/advanced-skill-creator/SKILL.md ~/.openclaw/skills/advanced-skill-creator/

# 3. 验证安装
ls -la ~/.openclaw/skills/
```

### 方法二：直接下载（如果网络允许）

```bash
# 直接从 GitHub 获取
mkdir -p ~/.openclaw/skills/advanced-skill-creator
cd ~/.openclaw/skills/advanced-skill-creator
wget https://raw.githubusercontent.com/openclaw/skills/refs/heads/main/skills/xqicxx/advanced-skill-creator/SKILL.md
```

## 验证安装

安装完成后，技能应该会在下次会话中自动加载。可以通过以下方式验证：

1. 重新加载 OpenClaw 会话
2. 提到"写skill"、"创建技能"等关键词，看是否触发该技能

## 技能功能

这个技能会在以下情况触发：
- 用户提到"写一个触发"、"写skill"、"claw skill"等
- 用户要求创建或修改 OpenClaw/Moltbot/ClawDBot 技能

触发后会执行官方 5 步研究流程：
1. 查阅官方文档
2. 研究 ClawHub 上的相关技能
3. 搜索最佳实践
4. 方案融合与比较
5. 输出标准格式的结果

## 卸载

```bash
rm -rf ~/.openclaw/skills/advanced-skill-creator
```
