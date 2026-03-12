
# Iteration 016: 记忆访问频率追踪（Hot/Warm/Cold分层）

**日期**: 2026-03-10
**项目**: Self-Evolving Agents Research

## 问题陈述
当前记忆系统只有时间分层（P0/P1/P2），没有访问频率追踪。这导致：
- 高频使用的记忆没有优先加载
- 无法识别哪些记忆是真正"活跃"的
- 记忆检索效率没有优化

## 改进想法
在现有P0/P1/P2时间分层基础上，添加访问频率追踪，实现Hot/Warm/Cold分层：
- **Hot Memory**：高频访问（过去7天accessCount > 10）
- **Warm Memory**：中频访问（过去30天accessCount 3-10）
- **Cold Memory**：低频访问（accessCount < 3）

## 实施步骤
1. **创建访问计数追踪文件**：创建`memory/access_counts.json`，用于存储所有记忆条目的访问计数
2. **修改经验文件结构**：在经验JSON文件中添加`accessCount`字段
3. **修改lesson文件结构**：在lesson JSONL文件中添加`accessCount`字段
4. **创建访问计数更新脚本**：创建`update_access_count.py`，用于手动或自动更新访问计数
5. **在start_task.py中展示Hot记忆**：修改`start_task.py`，在展示相关经验的同时，展示Hot记忆

## 预期结果
- 记忆访问计数被正确追踪
- Hot/Warm/Cold分层清晰
- 高频使用的记忆优先展示和加载
- 记忆检索效率提升

## 评估方法
- 检查`memory/access_counts.json`是否正确记录访问计数
- 验证经验和lesson文件中的`accessCount`字段是否正确更新
- 测试start_task.py是否优先展示Hot记忆
- 评估记忆检索效率是否提升

---

**创建时间**: 2026-03-10
**创建人**: 柏林
