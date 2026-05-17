---
name: agent-symphony
version: 1.1.0
family: compound-engineering
description: 多技能底层互通的Agent框架 - 协调thinking/memory/search/team四大技能，提供理解需求、深度分析、规划、反思、记忆存储、信息检索、任务执行等综合能力
argument-hint: "[需求描述或任务说明]"
examples:
  - "我想搞量化交易"
  - "帮我分析石榴籽项目"
  - "给我制定一个Python学习计划"
---

# Agent Symphony 技能交响乐

> 多技能底层互通，1+1 > 2 的质变效果

## 一键使用

```
/symphony 我想搞量化交易
```

## 核心技能

| 技能 | 角色 | 说明 |
|------|------|------|
| **thinking** | 协调者 | 理解需求、提问、分析、规划、反思 |
| **memory** | 记忆中心 | 向量检索、混合搜索、智能遗忘 |
| **search** | 信息获取 | 多引擎搜索、结果路由 |
| **team** | 执行者 | 任务执行、完成度检查 |

## 工作流程

```
用户需求 → 理解 → 提问澄清 → 制定计划 → 执行 → 反思
```

## 使用方式

### 方式一：CLI 快速使用

```bash
# 直接运行
python agent_symphony_cli.py "我想搞量化交易"

# 交互模式
python agent_symphony_cli.py -i
```

### 方式二：模块调用

```python
from agent_symphony import ThinkingSkill, MemorySkill, SearchSkill
from agent_symphony.shared import SharedContext

# 初始化
context = SharedContext()
thinking = ThinkingSkill()
memory = MemorySkill()

# 理解需求
result = thinking.execute("understand", {
    "requirement": "我想搞量化交易"
})
```

## CLI 功能

- ✅ 需求理解 + 明确度评估
- ✅ 澄清问题生成
- ✅ 行动计划制定
- ✅ 记忆存储
- ✅ 交互模式（输入问题持续对话）
- ✅ 对话模式测试 (`--test`)

### CLI 命令

```bash
# 交互模式
python agent_symphony_cli.py -i

# 测试对话模式（自动演示流程）
python agent_symphony_cli.py --test

# 单次对话
python agent_symphony_cli.py "我想搞量化交易"
```

## 插入式 LLM

自动从环境变量检测：
- OPENAI_API_KEY
- DASHSCOPE_API_KEY  
- MINIMAX_API_KEY
- DEEPSEEK_API_KEY

## 交互模式（指挥家对话）

通过 `dialog` 动作启动交互式对话：

```bash
python agent_symphony_cli.py -i
```

或通过 execute 调用：

```python
thinking = ThinkingSkill()
result = thinking.execute("dialog", {
    "message": "你好",
    "answers": {},
    "skill_results": {}
})
# result["response"] - 面向用户的回复
# result["skill_requests"] - 需要执行的技能申请
# result["state"] - clarifying|planning|executing|completed
# result["done"] - 是否完成
```

### 对话流程

```
用户启动交响乐
    ↓
指挥家自我介绍
    ↓
用户说出需求
    ↓
如果需求不明确 → 提问澄清
    ↓
如果明确 → 制定计划
    ↓
用户确认计划
    ↓
执行（调用 memory/search/team）
    ↓
完成/继续
```

### 技能申请（skill_requests）

当 thinking 需要调用其他技能时，返回 `skill_requests`：

```python
{
    "response": "正在搜索...",
    "skill_requests": [
        {"skill": "memory", "action": "store", "params": {...}},
        {"skill": "search", "action": "search", "params": {...}}
    ]
}
```

OpenClaw 执行这些技能后，通过 `notify("skill.result", {...})` 回调结果。

---

## OpenClaw 集成指南

### 启动方式

用户输入 `/symphony` 或触发 skill 时，OpenClaw 需要：

1. **创建/路由到 symphony session**
2. **加载 thinking skill**
3. **将用户消息路由到 thinking.execute("dialog", {...})**

### OpenClaw 需要实现的功能

```python
# 1. 识别 /symphony 命令
if message.startswith("/symphony"):
    # 启动交响乐
    requirement = message[10:].strip()  # 去掉 /symphony
    
    # 2. 调用 thinking 的 dialog 模式
    result = thinking.execute("dialog", {
        "message": requirement,
        "answers": {},
        "skill_results": {}
    })
    
    # 3. 返回 response 给用户
    send_to_user(result["response"])
    
    # 4. 如果有 skill_requests，执行技能
    for req in result.get("skill_requests", []):
        skill = req["skill"]
        action = req["action"]
        params = req["params"]
        
        skill_result = execute_skill(skill, action, params)
        
        # 5. 回调结果给 thinking
        thinking.notify("skill.result", {
            "skill": skill,
            "result": skill_result,
            "success": skill_result.get("success", False)
        })
    
    # 6. 继续对话循环，直到 done=True
    while not result.get("done"):
        # 等待用户下一条消息
        user_message = wait_for_user_input()
        
        result = thinking.execute("dialog", {
            "message": user_message,
            "answers": {},
            "skill_results": {}
        })
        
        send_to_user(result["response"])
        
        # 处理新的 skill_requests
        for req in result.get("skill_requests", []):
            skill_result = execute_skill(req["skill"], req["action"], req["params"])
            thinking.notify("skill.result", {...})
```

### 会话状态管理

OpenClaw 需要维护 symphony session 的状态：

```python
class SymphonySession:
    thinking: ThinkingSkill  # thinking skill 实例
    phase: str               # clarifying | planning | executing | completed
    done: bool              # 是否完成
    user_id: str            # 用户 ID
```

### 必需实现

| 功能 | 必须实现 | 说明 |
|------|----------|------|
| `/symphony` 命令识别 | ✅ | 触发交响乐 |
| `dialog` 动作调用 | ✅ | 核心入口 |
| `skill_requests` 处理 | ✅ | 调用其他技能 |
| `skill.result` 回调 | ✅ | 返回结果 |
| 多轮对话维持 | ✅ | 保持上下文 |

### 可选实现

| 功能 | 可选 | 说明 |
|------|------|------|
| 独立 session 存储 | ❌ | 关闭后继续 |
| skill 懒加载 | ❌ | 需要的才加载 |

---

## 指挥（Conductor）机制

交响乐的指挥（thinking skill）负责：

1. **开场** - 自我介绍，引导用户
2. **理解** - 评估需求明确度
3. **提问** - 不明确时向用户提问
4. **规划** - 明确后制定计划
5. **协调** - 调用 memory/search/team
6. **反馈** - 汇报进度给用户

---

_技能交响乐 · Agent Symphony_