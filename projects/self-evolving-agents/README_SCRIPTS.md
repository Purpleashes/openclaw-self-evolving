
# 脚本使用指南

本目录包含Self-Evolving Agents项目的所有辅助脚本。

---

## 脚本列表

### 1. task_manager.py
**用途**: 任务管理系统的主脚本，用于查看任务状态和获取下一个任务。

**使用方式**:
```bash
python3 task_manager.py
```

**功能**:
- 显示当前任务系统状态（总任务数、已完成、进行中、待办）
- 显示优先级最高的待办任务

---

### 2. start_task.py
**用途**: 标记任务为进行中。

**使用方式**:
```bash
python3 start_task.py <task_id>
```

**示例**:
```bash
python3 start_task.py task-009
```

**功能**:
- 将指定任务的状态从"backlog"更新为"in-progress"
- 记录任务开始时间

---

### 3. complete_task.py
**用途**: 标记任务为已完成。

**使用方式**:
```bash
python3 complete_task.py <task_id>
```

**示例**:
```bash
python3 complete_task.py task-008
```

**功能**:
- 将指定任务的状态从"in-progress"更新为"completed"
- 记录任务完成时间

---

### 4. session_start_hook.py
**用途**: 会话开始钩子，每次新会话开始时自动运行。

**使用方式**:
```bash
python3 session_start_hook.py
```

**功能**:
1. 自动问候 + 日期显示
2. 回顾最近2天的记忆
3. 列出待办任务（按优先级排序）
4. 建议优先级最高的任务

**自动化约定**:
- 每次新会话开始时，柏林主动运行此钩子
- 自动展示状态更新
- 用户无需手动操作

---

### 5. memory_helper.py
**用途**: 记忆管理助手，用于向MEMORY.md添加条目。

**使用方式**:
```bash
python3 memory_helper.py <priority> <content> [--date YYYY-MM-DD]
```

**示例**:
```bash
# 添加P0条目
python3 memory_helper.py P0 "这是一个永久记忆条目"

# 添加P1条目（指定日期）
python3 memory_helper.py P1 "这是一个短期记忆条目" --date 2026-03-09
```

**参数说明**:
- `priority`: 优先级（P0、P1、P2）
- `content`: 记忆内容
- `--date`: 可选，日期（YYYY-MM-DD格式），默认为今天

---

## 工作流程示例

### 典型任务处理流程
1. 查看任务状态：`python3 task_manager.py`
2. 开始任务：`python3 start_task.py task-009`
3. 执行任务...
4. 完成任务：`python3 complete_task.py task-009`

---

## 注意事项
- 所有脚本都需要在`projects/self-evolving-agents/`目录下运行
- 任务ID格式为`task-XXX`（如task-001、task-009）
- 日期格式必须为YYYY-MM-DD（如2026-03-09）

---

**创建日期**: 2026-03-09  
**创建人**: 柏林
