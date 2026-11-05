# skills-lxb

[XianbaoLi](https://github.com/XianbaoLi) 的 agent skills 集合 —— 用 [skills CLI](https://skills.sh) 一条命令装进 Claude Code / Codex / Cursor / GitHub Copilot / Gemini CLI / OpenCode / Hermes 等支持 SKILL.md 的 agent。

Personal agent skills, installable with `npx skills add`.

## 安装

```bash
# 安装整个集合（全局，装到所有检测到的 agent）
npx -y skills@latest add XianbaoLi/skills-lxb -g --copy

# 只装某一个
npx -y skills@latest add XianbaoLi/skills-lxb --skill grill-me -g --copy

# 装进当前项目（.agents/skills/ 等）
npx -y skills@latest add XianbaoLi/skills-lxb --skill grill-me --copy
```

离线 / 内网环境：直接把 `skills/<name>/` 拷到目标目录，或运行仓库自带脚本：

```bash
bash install.sh                    # 装到所有检测到的 agent（全局）
bash install.sh codex claude-code  # 只装指定 agent
bash install.sh --project codex    # 装进当前项目
```

## Skills

### [grill-me](skills/grill-me/SKILL.md)

面向模糊想法的多轮需求探索：确定项目框架、构建学习计划时，不需要先有完整方案。通过选择、追问和必要讲解，逐步明确诉求，再形成框架草案或分阶段计划。不是系统指令审批工具。

Multi-round, pickable-option grilling that stress-tests any topic and converges into a decision list / plan.

- **显式启用**：明确说 `grill me` / 拷打我 / 多轮梳理，或明确恢复访谈。普通计划、改代码、审批、讨论 skill 不自动启动。
- **三模式**：用户画像 / 计划·决策 / 知识拷问；**强度档**：轻 / 标准 / 重（开场可选）
- **跨平台**：按当前可用的提问工具与 schema 使用表单；没有时用编号聊天，不为提问擅自切换权限模式。
- **可点选求助**：每道选择题明确提供「我不懂这个问题，先讲解」。选中后，下一轮先解释该题和选项的区别，再用白话重问；不算选定方案，也不清空其他题的答案。讲解深度与强度分开。
- **不代审批**：理解、偏好、收束确认与行动许可分开；不绕过原生审批，也不重复拦截已授权工作。记忆、会话记录只在既有权限内写入。
- 基于 [Matt Pocock 的 grilling](https://github.com/mattpocock/skills)（MIT）移植并扩展

### 例子

```text
拷打我这个方案，标准强度；不熟悉的概念先教我。
继续昨天的访谈，重一点，但先把这一题讲清楚。
```

「修改 grill-me」「解释一下这个概念」本身不是访谈指令。选择「我倾向 A」也不等于批准安装 A。

详见 [交互示例](skills/grill-me/references/example-round.md) 与 [会话模板](skills/grill-me/templates/session.grill.md)。

## 手动 / 离线安装目录

| 平台 | 全局目录 | 项目目录 |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Cursor | `~/.cursor/skills/` | `.agents/skills/` |
| GitHub Copilot | `~/.copilot/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.agents/skills/` |
| OpenCode | `~/.config/opencode/skills/` | `.agents/skills/` |
| Windsurf | `~/.codeium/windsurf/skills/` | `.windsurf/skills/` |
| Hermes Agent | `~/.hermes/skills/` | `.hermes/skills/` |

> `.agents/skills/` 是多 agent 通用约定目录（Codex / Cursor / Copilot / Gemini / OpenCode / Cline / amp / Zed 等共用）。完整映射见 [vercel-labs/skills docs/agents.md](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)。

## 维护

- 本仓库是**分发副本**；开发原版在作者本机（Hermes skills 目录），更新后同步到这里并 push。
- 装过的机器升级：`npx skills update grill-me`（或重新执行安装命令）。

## 验证与限制

```bash
python -m unittest discover -s tests -v
```

测试检查实际 skill 的规则、示例和引用，防止回退到「答题即授权」或「不懂也逼选」。这是文档契约测试，不是所有平台的 UI/权限执行测试；skill 不能替代宿主权限系统，也不能保证模型绝不误触发。

## License

MIT。grill-me 传承自 Matt Pocock 的 skills 仓库（`grilling`，MIT）；交互形态对标 Claude Code AskUserQuestion / plan mode。
