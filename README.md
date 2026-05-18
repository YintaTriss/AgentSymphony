# Agent Symphony 技能交响乐

> 多技能协作框架，通过「指挥家 + 技能团」模式完成复杂任务

---

## 核心架构

```
用户（自然语言）
    ↓
SymphonySession（指挥家）
    ↓
thinking（协调者，真实调用 LLM）
    ├── LLMRouter → 从 87 个专家中选择最相关的（ExtendedRegistry）
    ├── Jury（陪审团）→ 并行收集各专家视角分析
    └── 状态机：clarifying → planning → executing → completed
         ↓
    skill_requests（memory / search / team）
```

### 四大技能

| 技能 | 角色 | 何时调用 |
|------|------|----------|
| **thinking** | 协调者，真实调用 LLM 与用户对话 | 始终 |
| **memory** | 记忆中心，持续学习用户偏好和上下文 | 用户确认执行后，记录需求/偏好 |
| **search** | 信息获取，搜索相关信息辅助决策 | planning 阶段需要信息时 |
| **team** | 执行者，通过 ClawTeam 执行具体任务 | 用户确认后，执行 plan |

### thinking 技能的工作方式

thinking 是核心，它**真实调用 LLM**（通过 SharedContext 的 LLMProvider），不是规则匹配：

1. **clarifying 阶段**：LLM 生成澄清问题，理解用户需求
2. **planning 阶段**：
   - LLMRouter 调用真实 LLM，从 87 个专家（Python 内置 + SKILL.md 发现）中选择最相关的几个
   - Jury 并行驱动各专家视角分析（乔布斯视角、元认知、风险视角…）
   - LLM 综合输出结构化分析
   - 向用户确认计划
3. **executing 阶段**：生成 skill_requests，调用 memory/search/team
4. **completed 阶段**：汇总结果，问用户是否需要继续

---

## 工作流程详解

```
用户: "我想做一个chrome扩展"

[1] clarifying
    thinking 真实调用 LLM，问："你打算做什么样的扩展？面向谁？"

[2] planning
    LLMRouter 调用 MiniMax LLM，从 87 专家选出 7 个：
      ["jobs_perspective", "elon_perspective", "risk_detail", ...]
    Jury 并行分析：
      - 乔布斯问：这是 amazing 还是 shit？
      - Elon 问：能不能 10 倍好？
      - 风险视角问：有哪些隐患？
    LLM 综合输出，向用户确认："请告诉我可以开始执行吗？"

[3] user confirms ("好")
    → memory.store() 记录需求
    → search.search() 搜索相关信息
    （team 待集成）

[4] 技能结果回调 thinking
    → "completed, done=True"

[5] 用户可继续新需求或结束
```

---

## LLM 集成（关键）

thinking 技能的 LLM 智力来自 **SharedContext → LLMProvider**，自动从 OpenClaw 配置读取：

- minimax → Anthropic Messages API
- deepseek/openai → OpenAI Chat Completions API
- 零配置，技能不携带 API Key

LLMRouter 的专家选择流程：
1. 收集所有启用的专家（Python 内置 + SKILL.md 发现）
2. 构造 prompt，包含专家列表
3. 调用真实 LLM（MiniMax 等）
4. 解析 JSON 响应，提取选中的专家 ID
5. 验证 ID 有效性，返回 RoutingResult

---

## 目录结构

```
AgentSymphony/
├── agent_symphony_openclaw.py   # OpenClaw 集成入口（SymphonySession）
├── agent_symphony_cli.py        # CLI 入口
├── shared/                      # 共享模块
│   ├── context.py               # SharedContext + LLMProvider（插入式 LLM）
│   └── registry.py              # 技能注册表
├── skills/
│   ├── thinking/                # 协调者（真实调用 LLM）
│   │   └── skill.py             # 状态机 + Jury + LLMRouter 集成
│   ├── memory/                  # 记忆技能
│   ├── search/                  # 搜索技能
│   └── team/                    # 执行技能（ClawTeam）
└── tests/
    ├── test_dialog.py           # thinking 技能对话测试
    ├── test_symphony_full.py    # 完整流程测试
    └── test_openclaw.py         # OpenClaw 集成测试
```

---

## 快速测试

```bash
cd AgentSymphony
pip install anthropic  # 必须（LLM 调用）

# 完整流程测试
python test_symphony_full.py
```

---

## 相关项目

| 项目 | 说明 |
|------|------|
| [AgentSymphony](https://github.com/YintaTriss/AgentSymphony) | 交响乐主仓库 |
| [Agent-Superthinking](https://github.com/YintaTriss/Agent-Superthinking) | thinking 技能的专家视角框架（LLMRouter + ExtendedRegistry + Jury） |
| [AgentMemory](https://github.com/YintaTriss/AgentMemory) | 记忆技能 |
| [AgentSearch](https://github.com/YintaTriss/AgentSearch) | 搜索技能 |
| [AgentTeam](https://github.com/YintaTriss/AgentTeam) | 执行技能（ClawTeam 多智能体框架） |

---

## 版本历史

### v1.1.1 (2026-05-18)
- 修复：executing 状态无法完成（done 始终 False）
- 修复：skill_results 回调后正确转换到 completed 状态
- 依赖：`pip install anthropic`（LLM 调用必须）

### v1.1.0 (2026-05-17)
- 完整状态机：clarifying → planning → executing → completed
- thinking 技能真实调用 LLM（MiniMax 等）
- LLMRouter 集成：从 87 个专家中智能选择
- OpenClaw 技能入口（SKILL.md）
- 交响乐完整流程测试通过

---

_技能交响乐 · Agent Symphony_
