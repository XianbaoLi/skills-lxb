---
workflow_id: WF-DOC-TRANSLATE
name: 数学与物理资料专业翻译
name_en: Mathematical and Physics Document Translation
version: 1.0.0
status: draft
category: document-translation
execution_model: agent-guided
implementation: documentation-only
capabilities:
  - 数学、物理及 STEM 资料的专业英译中
  - 可选中译英或中英对照
  - 专业术语表建立与跨章节一致性维护
  - 数学逻辑、条件、量词和公式语义保真
  - 保留 Markdown 结构、图片引用和来源定位
skills:
  required:
    - mathtranslations
  optional:
    - mineru
    - stem-notes
inputs:
  - 已校验的原文语言 Markdown
  - 目标语言与翻译范围
  - 可选：原始 PDF、图片资源、项目术语表和既有译文
outputs:
  - 明确标记为 candidate 的目标语言 Markdown
  - 项目级术语表
  - 必要的翻译疑点和复核记录
not_supported:
  - 普通非数学领域的通用翻译
  - 对原文习题进行求解
  - 未经要求增加教学解释、提示或总结
  - 默认生成 MathTranslations LaTeX/PDF 工程
approval_gates:
  - 使用远程翻译/术语服务或上传源文档
  - 将候选译文提升为正式接受版本
---

# WF-DOC-TRANSLATE — 数学与物理资料专业翻译

## 1. 目的与适用场景

将已经识别、整理并尽可能校验的数学、物理或 STEM 原文资料翻译为目标语言。默认英译中，默认输出中文 Markdown 候选稿。

本 Workflow 适合教材正文、定义、定理、证明、公式说明、物理习题和考试题目。它不适用于普通非数学领域的通用翻译；遇到其他学科时，应确认是否有更合适的翻译 Skill。

## 2. 支持的功能

- 数学和物理语境下的专业术语翻译。
- 保留定义、假设、量词、逻辑关系和证明结构。
- 保留公式、编号、符号、单位、图表和交叉引用。
- 对同一术语建立统一译法，并记录上下文例外。
- 对题目中的指令动词、条件和限制进行语义保真翻译。
- 输出中文、英文或中英对照版本。
- 对疑难表达保留英文原词并记录复核问题。

## 3. Skill 组成与职责

- **required — mathtranslations**：提供数学语义保真、术语一致性、原文证据优先级和翻译复核规范。阅读 skills/mathtranslations/SKILL.md，并按需读取其 references/workflow.md、references/latex-quality.md、references/review-checklist.md。
- **optional — mineru**：当原文 Markdown 中的 OCR、公式、图注或题设存在疑点时，按页面定位回看原 PDF。优先读取已有解析结果。
- **optional — stem-notes**：仅在理工科图示或公式的上下文理解确有帮助时使用。

### Markdown 适配说明

mathtranslations 上游 Skill 的原生目标是中文 LaTeX/PDF 工程。本 Workflow 只采用其适用的数学翻译原则，最终输出服从用户和项目 AGENTS.md 的 Markdown 要求。

因此不自动执行其个人封面、Logo、固定审核人署名、模板排版、LaTeX 编译或可选多模型路由流程，也不对 Markdown 运行 LaTeX 审计脚本。

## 4. 输入与输出

**输入**
- 已校验或至少已整理的原文 Markdown。
- 目标语言和处理范围；未指定时，英文原文默认翻译为简体中文。
- 可选：原始 PDF、MinerU 定位符、术语表、已有章节译文。

**输出**
- output/<document>/<unit>.zh-CN.candidate.md：候选中文版。
- _work/<document>/glossary.en-zh.md：项目术语表。
- _work/<document>/translation-issues.md：仅在存在待确认术语或语义疑点时创建。
- _work/<document>/translation-review.md：需要单独复核时创建。

原文文件不被覆盖；候选译文不得自动命名为正式译文。

## 5. 工作流程

1. **确认原文依据**：检查原文 Markdown 的范围、语言、章节层级和来源状态。若原文来自扫描 OCR，优先确认关键内容已核对；无法确认时先回到源 PDF。
2. **建立术语表**：读取既有项目术语表和已完成章节。记录英文术语、首选中文、学科语境、可接受的替代译法及来源依据。
3. **按完整语义单元翻译**：以段落、定义、证明或整道习题为单位，不割裂数学逻辑。保持原文与译文结构对应。
4. **保持数学语义**：重点区分 if / only if / iff、必要与充分、任意与存在、唯一、至少/至多、分别/对应、假设条件、边界条件和否定范围。
5. **保持题目要求**：准确区分 prove、show、derive、calculate、evaluate、estimate、sketch、compare、discuss、explain 等指令。翻译完整题设、给定数据、单位、选项和限制条件，不擅自解题。
6. **处理图表和引用**：默认复用原图，翻译图注和正文引用；保留表格数据、编号、脚注、标签和来源页码。图中嵌入文字不擅自修改。
7. **生成候选稿**：输出独立的 .zh-CN.candidate.md，在元数据中标记 translation_status: candidate 和 review_status: pending。
8. **分项复核**：分别检查内容完整性、数学语义、术语一致性和 Markdown 结构。无法确认的译法保留英文对照并记录，不伪装成确定译文。

## 6. 约束与质量标准

- 翻译数学含义，不机械复制英文语序。
- 不改变原文的假设、量词、否定、条件、比较、逻辑依赖和结论强度。
- 不改动公式内容、符号、上下标、单位、常数和编号。
- 不删掉重复表达，因为它可能承担限定或指代作用。
- 不把翻译、解释和纠错混为一谈。原书疑似错误应保留并单独记录。
- 不自动添加提示、解答、教学扩写、摘要或例题。
- 使用本地术语表；未获授权不调用外部术语服务，不上传资料。
- mathtranslations 的 LaTeX/PDF 专属规则不覆盖用户指定的 Markdown 输出格式。

## 7. 失败处理

若原文存在影响数学意义的 OCR 疑点，先使用 MinerU 定位或原 PDF 页面核对。若关键内容无法确认，应将相关部分标记为待核对，并使候选译文保持 provisional 状态。遇到术语冲突时记录上下文和备选译法，不凭字典直译。

## 8. 调用示例

- “按 WF-DOC-TRANSLATE 将 2.4.source.md 翻译成中文候选稿，不解题。”
- “沿用项目术语表，继续翻译下一节，保留全部公式和题目条件。”
- “生成中英对照版，英文原文和中文译文逐段对应。”
