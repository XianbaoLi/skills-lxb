---
workflow_id: WF-DOC-PROCESS
name: 教材与学习资料处理
name_en: Document Processing and Translation
version: 1.0.0
status: draft
category: document-processing
execution_model: agent-guided
implementation: documentation-only
supported_modes:
  - transcribe
  - translate
  - transcribe_translate
  - review_translation
capabilities:
  - 扫描版、图像型及普通 PDF 的内容识别与结构化转写
  - 指定页码、章节、小节或题目范围的增量处理
  - 数学公式、表格、图片、图注及复杂版面的识别和核对
  - 保留原文语言、章节结构、题目条件和来源页码
  - 数学、物理及 STEM 资料的专业翻译
  - 项目级中英术语表和跨章节术语一致性维护
  - 原文与译文的对照复核、问题记录及候选版本验收
skills:
  required: []
  optional:
    - mineru
    - stem-notes
    - mathtranslations
  by_mode:
    transcribe:
      required:
        - mineru
      optional:
        - stem-notes
    translate:
      required:
        - mathtranslations
      optional:
        - mineru
        - stem-notes
    transcribe_translate:
      required:
        - mineru
        - mathtranslations
      optional:
        - stem-notes
    review_translation:
      required:
        - mathtranslations
      optional:
        - mineru
inputs:
  - 原始 PDF、扫描件或图像型文档
  - 已识别或已整理的原文 Markdown
  - 用户指定的章节、页码、题目范围及目标语言
  - 可选：已有 MinerU 解析结果、图片资源、术语表、历史译文和复核记录
outputs:
  - 原文语言的 source Markdown
  - 独立的目标语言 translation candidate Markdown
  - 被正文实际引用的图片资源
  - 必要的解析索引、术语表、OCR 疑点及翻译复核记录
  - 仅在用户明确接受后生成的正式译文副本
not_supported:
  - 未经要求自动解答习题或添加教学解释
  - 将忠实转写自动改成摘要、改写或知识重构
  - 未经要求生成 LaTeX/PDF、Word 或交互式学习应用
  - 将 OCR 猜测当作原文事实
  - 自动接受候选译文或覆盖已有正式译文
approval_gates:
  - 安装、升级或重新配置本地解析环境
  - 使用远程解析、远程翻译或上传源文件
  - 静默切换 OCR/解析工具
  - 覆盖、删除或归档已有用户文件
  - 将候选译文提升为正式接受版本
---

# WF-DOC-PROCESS — 教材与学习资料处理

## 1. 目的与适用范围

本 Workflow 统一处理教材、讲义、课件、习题集、论文及其他学习资料中的识别、转写、翻译和复核任务。前置元信息中的全局 required 为空，是因为不同任务模式需要不同 Skill；实际调用要求以 skills.by_mode 为准。

它不是四条固定流水线，而是一个具有四种任务模式的统一工作流。Agent 根据用户目标选择一个模式；只有用户明确要求组合任务时，才串联多个模式。

**默认原则：忠实、可追溯、增量处理。** 不擅自总结、解题、扩写、纠错原书内容或改变题目含义。

## 2. 支持的任务模式

| 模式 | 适用请求 | 必需 Skill | 主要交付 |
|---|---|---|---|
| transcribe 忠实转写 | 识别扫描 PDF、整理原文 Markdown | mineru | .source.md |
| translate 专业翻译 | 将已有原文 Markdown 翻译成中文 | mathtranslations | .zh-CN.candidate.md |
| transcribe_translate 转写并翻译 | 从扫描 PDF 直接生成原文及候选中文版 | mineru、mathtranslations | 两份 Markdown |
| review_translation 译文复核 | 对照原文检查候选译文，必要时修订 | mathtranslations | 复核记录；获批后正式译文 |

模式选择规则：

- 用户只要求识别、转写、重排原文：选择 transcribe。
- 用户已有可靠的原文 Markdown，只要求翻译：选择 translate。
- 用户提供扫描版 PDF，并要求中文版本：选择 transcribe_translate。
- 用户提供原文和候选译文，要求检查：选择 review_translation。
- 用户明确要求多个独立目标时，可以组合模式；不重复执行已经完成且仍然有效的阶段。
- 不因材料是整本教材就自动调用 book-to-skill。只有用户希望生成可复用、可检索的知识 Skill 时才考虑它。

## 3. Skill 组成与职责

### mineru — 文档解析

负责 PDF 解析、OCR、公式与版面识别、表格和图片提取、分页续读、页面/Block 定位及视觉核对。

在 transcribe 和 transcribe_translate 模式中必需；在其他模式中，仅当需要回看原始 PDF 或核实 OCR 疑点时调用。

开始前读取 [mineru Skill](../skills/mineru/SKILL.md)，检查当前 CLI、版本和运行环境要求。优先使用已配置的本地环境和已有解析结果。

### stem-notes — STEM 图文理解与材料组织

可选能力。仅在数学/物理公式、复杂图示、图表裁剪或理工科材料组织确有帮助时调用。

读取 [stem-notes Skill](../skills/stem-notes/SKILL.md) 和当前任务相关的参考文件。只采用与当前模式相关的能力；不得机械触发其默认问卷、LaTeX 输出、整本教材生成或习题求解流程。注意其部分工具约定源自 Claude Code，宿主不兼容时应采用可用的本地方法。

### mathtranslations — 数学与科学专业翻译

在 translate、transcribe_translate 和 review_translation 模式中必需。

读取 [mathtranslations Skill](../skills/mathtranslations/SKILL.md)，按需参考数学语义、术语管理和复核资料。其上游原生流程主要面向 LaTeX/PDF；本 Workflow 默认采用其专业翻译原则，但最终输出服从用户要求，通常为 Markdown。

不自动套用上游个人封面、Logo、固定审核人署名、模板排版、LaTeX 编译或可选多模型路由。

## 4. 通用输入与输出约定

### 输入

根据模式接受：

- 原始 PDF、扫描 PDF、页面图像或其他文档；
- 已识别、已整理的原文 Markdown；
- 用户指定的章节、小节、页码、题号或全篇范围；
- 目标语言和是否需要中英对照；
- 可选的 MinerU 解析结果、图片资源、术语表、既有译文和项目 AGENTS.md。

默认将英文专业资料翻译为简体中文。其他目标语言按用户指定执行；若现有 Skill 不覆盖该语言或学科，应明确说明能力边界。

### 输出文件命名

同一处理单元采用以下稳定命名：

- `<unit>`.source.md：原文语言转写；
- `<unit>`.zh-CN.candidate.md：中文候选译文；
- `<unit>`.zh-CN.md：用户明确接受后的正式中文译文；
- _work/`<document>`/translation-review.md：译文复核记录；
- _work/`<document>`/glossary.en-zh.md：项目术语表；
- _work/`<document>`/ocr-issues.md：OCR 或原始材料疑点；
- assets/`<unit>`/：正文实际引用的图片资源。

如果目标语言不是中文，应在文件名中使用明确的语言标识，例如 .en.candidate.md。

原文、候选译文和正式译文必须分开保存。不得把候选稿直接命名为正式稿。

## 5. 四种模式的工作流程

### 模式 A：transcribe — 忠实转写

1. 确认原始文件和处理范围；区分 PDF 实际页序与原书印刷页码。
2. 检查已有 MinerU 解析结果和上次处理记录；覆盖范围有效时直接复用。
3. 检查本地 MinerU 环境。遵循 MinerU Skill 的版本、质量档位和服务要求；不擅自安装、升级或修改持久配置。
4. 按目标页范围解析。使用结构化结果控制续读，遵循 MinerU 返回的 continuation/locator，不猜测下一页，不反复从第一页解析。
5. 以 PDF 可见页面为内容依据，整理原文 Markdown。保留标题层级、段落顺序、定义、定理、证明、推导、例题、习题、题目选项、脚注、图表和交叉引用。
6. 对公式、上下标、正负号、希腊字母、矢量/算符、积分、求和、矩阵、单位、题设条件和图号进行视觉核对。
7. 保留清晰原图；必要时从原始页面裁剪。图片使用相对于 Markdown 的路径，不以 AI 生成图替代原图。
8. 修正有原页证据支持的 OCR 错误。原书疑似错误应保留并另行注明；无法辨认的内容标记为待核对。
9. 检查范围覆盖、题号、公式、图表、图片路径和来源定位。

交付 `<unit>`.source.md 及实际引用的图片资源。此模式不翻译、不解题、不总结。

### 模式 B：translate — 专业翻译

1. 检查原文 Markdown 的来源、范围和完整性。若来自扫描 OCR，关键内容应已核对；存在影响数学意义的疑点时，先回看原始页面。
2. 读取既有项目术语表和已完成章节，建立或更新 glossary.en-zh.md。
3. 按完整语义单元翻译，例如段落、定义、证明或整道习题，不割裂数学逻辑。
4. 保留原文的假设、量词、否定、逻辑关系、必要/充分条件、唯一性、边界条件、单位和数值。
5. 准确区分 prove、show、derive、calculate、evaluate、estimate、sketch、compare、discuss、explain 等题目指令；完整翻译题设、数据、选项和限制，不擅自解题。
6. 保留公式、编号、图表、脚注、引用和来源页码。默认复用原图，只翻译图注及正文引用；不擅自修改图片内嵌文字。
7. 生成独立的候选译文，并标记 translation_status: candidate、review_status: pending。
8. 分别检查内容完整性、数学语义、术语一致性和 Markdown 结构。

交付 `<unit>`.zh-CN.candidate.md。此模式不覆盖原文，不自动生成正式译文。

### 模式 C：transcribe_translate — 转写并翻译

按顺序组合模式 A 和模式 B：

1. 先完成原文解析、转写和页面核对。
2. 在翻译前评估原文质量：
   - **READY**：影响含义的内容已识别并核对，可以翻译。
   - **READY_WITH_NOTES**：存在不影响核心含义的轻微疑点；翻译时保留并传递问题记录。
   - **BLOCKED**：公式、数字、否定、条件、图示标签或缺页等关键内容无法确认，可能改变原意。
3. 对 READY 和 READY_WITH_NOTES 的内容生成候选译文；BLOCKED 的受影响单元应先回看原页。仍无法确认时，暂停该单元或明确标记为 provisional，不得伪装成确定原文。
4. 仅基于已经整理的 .source.md 翻译，不重新 OCR 已完成的页面。
5. 对照 PDF、原文 Markdown 和中文候选稿，检查范围、段落、题号、公式、单位、图表、选项和语义是否一致。
6. 将 OCR 疑点和翻译疑点分别记录，避免混为一类问题。

默认交付两份文件：

- `<unit>`.source.md
- `<unit>`.zh-CN.candidate.md

不默认生成 PDF、Word、习题答案、总结或知识 Skill。

### 模式 D：review_translation — 译文复核与验收

1. 确认原文和候选译文来自同一教材版本、章节和页码范围。
2. 逐段检查标题、正文、定义、定理、证明、例题、习题、条件、选项、图表、脚注和引用。
3. 重点检查否定、量词、if/only if、必要与充分、唯一、分别、至少/至多、边界条件、正负号、上下标、单位和公式编号。
4. 对照术语表检查专业术语和上下文用法。
5. 当问题可能来自 OCR 时，调用 MinerU 定位或回看原始 PDF；不要把原书错误误判为翻译错误。
6. 将问题记录在独立的 translation-review.md 中，标注位置、证据、严重程度（critical / major / minor）和修改建议。
7. 用户要求修订时，修改候选稿并复核受影响内容。
8. 只有用户明确接受当前具体版本后，才生成 `<unit>`.zh-CN.md 正式副本。

复核完成不等于用户验收。不得根据沉默、普通的“继续”或 Agent 自己的检查结果推断用户接受；不得覆盖已有正式译文。

## 6. 通用质量标准与边界

### 内容忠实

- 原文内容、论证顺序、数学推导和题目条件不得擅自删减或扩写。
- OCR 修正必须有原始页面或可靠源文件证据。
- 疑似原书错误与 OCR 错误分开记录。
- 不凭专业常识补全无法识别的文字、公式或图中标注。

### 数学与物理语义

- 公式使用 LaTeX，保留原有符号、编号和结构。
- 重点核对上下标、正负号、量词、矢量/算符标记、单位、边界条件和近似条件。
- 翻译不得改变数学命题的逻辑强度或题目要求。
- 翻译模式不等于解题模式；除非用户明确要求，否则不添加答案、提示或推导。

### 图片与引用

- 图片必须与正文语义对应，保留原图号、图注、坐标轴、图例和有效标注。
- 优先保留原图或高清裁剪，不生成替代图。
- 图片使用相对路径；检查所有本地资源链接。
- 保留 PDF 页码、印刷页码和可用的 MinerU 定位符，三者不可混为一谈。

### 隐私与环境

- 本地解析优先。不得静默使用 MinerU --remote、远程翻译或上传用户资料。
- 不擅自安装/升级依赖、下载模型、修改服务配置、启动/重启服务、清理缓存或覆盖现有文件。
- MinerU 的可恢复错误应遵循其 Skill 的恢复选项，未经用户选择不静默切换其他解析器。
- Skill 不兼容当前宿主时，使用合理的本地替代方法，并说明降级情况。

## 7. 文件组织与状态管理

优先沿用项目已有结构。没有约定时，按需创建：

~~~text
project/
├── AGENTS.md
├── source/                         # 原始资料，只读
├── _work/
│   └── `<document>`/
│       ├── mineru/                 # 解析结果与定位信息
│       ├── pages/                  # 原页渲染与核对材料
│       ├── glossary.en-zh.md       # 项目术语表
│       ├── ocr-issues.md           # OCR/原文疑点
│       └── translation-review.md   # 译文复核记录
└── output/
    └── `<document>`/
        ├── `<unit>`.source.md
        ├── `<unit>`.zh-CN.candidate.md
        ├── `<unit>`.zh-CN.md         # 仅在用户明确接受后生成
        └── assets/
            └── `<unit>`/
~~~

只创建当前任务实际需要的目录和文件，不为满足示例而创建空目录。

状态应明确记录，不根据文件存在与否推断：

- parsed：已完成解析，尚未完成内容核对。
- transcribed：已整理原文 Markdown，仍可能存在待核对问题。
- source-reviewed：请求范围已对照原始页面核验，问题已记录。
- translation-candidate：候选译文已生成，尚未完成复核。
- reviewed-candidate：已完成复核，仍然是候选稿。
- accepted：用户明确接受的具体版本。

## 8. 失败处理

- MinerU 不可用或版本不兼容：停止并说明情况；未经批准不安装、升级或更改环境。
- 本地解析质量不足：说明当前可用选择，等待用户决定；不静默远程上传或切换解析器。
- 关键 OCR 内容无法核实：将受影响单元标记为 BLOCKED 或 provisional，不生成貌似确定的译文。
- 图片或页面缺失：保留占位和问题记录，不生成虚构替代内容。
- 术语有歧义：保留英文原词、记录语境和备选译法。
- 候选译文已存在：创建新版本或在明确授权后修订，不覆盖正式版本。
- Skill 与宿主不兼容：只执行当前宿主可支持的部分，明确说明未执行的能力。

## 9. 调用示例

- “按 WF-DOC-PROCESS 的 transcribe 模式，忠实转写这份扫描教材的 2.4 节，保留英文原文。”
- “按 WF-DOC-PROCESS 的 translate 模式，把已经校验的 2.4.source.md 翻译成候选中文版，不解题。”
- “按 WF-DOC-PROCESS 的 transcribe_translate 模式，从扫描版 PDF 生成英文原文和候选中文版。”
- “按 WF-DOC-PROCESS 的 review_translation 模式，对照英文原文复核候选译文，先列问题，不要定稿。”
- “继续处理下一节，复用已有 MinerU 解析结果和项目术语表。”
