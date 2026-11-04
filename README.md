# skills-lxb

[XianbaoLi](https://github.com/XianbaoLi) 的 agent skills 集合 —— 用 [skills CLI](https://skills.sh) 一条命令装进 Claude Code / Codex / Cursor / GitHub Copilot / Gemini CLI / OpenCode / Hermes 等 80+ agent。

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

多轮选择式拷打（Claude Code plan 模式风格）——结构化选项点选即答，一轮一个前沿，多轮推进，收敛成决策清单 / 计划。

Multi-round, pickable-option grilling that stress-tests any topic and converges into a decision list / plan.

- **触发**：`grill me` / 拷打我 / 盘问我 / 多轮滚动访谈 / stress-test me
- **三模式**：用户画像 / 计划·决策 / 知识拷问；**强度档**：轻 / 标准 / 重（开场可选）
- **跨平台**：有表单用表单（Claude Code `AskUserQuestion`、Hermes `clarify`），无表单自动切「聊天编号格式」（Codex / Cursor / Copilot / Gemini / OpenCode …）
- 基于 [Matt Pocock 的 grilling](https://github.com/mattpocock/skills)（MIT）移植并扩展

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

## License

MIT。grill-me 传承自 Matt Pocock 的 skills 仓库（`grilling`，MIT）；交互形态对标 Claude Code AskUserQuestion / plan mode。
