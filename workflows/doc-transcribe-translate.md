---
workflow_id: WF-DOC-TRANSCRIBE-TRANSLATE
name: 扫描版 PDF 转写并生成候选中文版
name_en: Scanned PDF Transcription and Chinese Translation
version: 1.0.0
status: draft
category: document-processing-and-translation
execution_model: agent-guided
implementation: documentation-only
capabilities:
  - 扫描版或图像型 PDF 的 OCR 与页面结构解析
  - 原文语言 Markdown 的忠实转写和核对
  - 数学、物理及 STEM 内容的专业中文翻译
  - 原文与候选译文的独立保存和范围对齐
  - 公式、图表、题设、编号及来源页码的保真
  - 术语表、OCR 疑点和翻译问题的跟踪
skills:
  required:
    - mineru
    - mathtranslations
  optional:
    - stem-notes
inputs:
  - 原始扫描版或图像型 PDF
  - 用户指定的章节、题目或页码范围
  - 可选：已有 MinerU 解析结果、原文 Markdown、图片资源、术语表
outputs:
  - 经核对的原文语言 Markdown
  - 独立的中文翻译候选 Markdown
  - 被两个文档实际引用的图片资源
  - 必要的解析索引、术语表和问题记录
not_supported:
  - 自动解答习题
  - 未经要求重新编写教材或增加教学解释
  - 自动接受或覆盖正式译文
  - 默认生成 PDF、Word 或交互式学习应用
approval_gates:
  - 安装、升级或重新配置 MinerU
  - 使用远程解析或上传源文件
  - 静默切换 OCR/解析工具
  - 将候选译文提升为正式接受版本
---

# WF-DOC-TRANSCRIBE-TRANSLATE — 扫描版 PDF 转写并生成候选中文版

## 1. 目的与适用场景

处理英文扫描版或图像型数学、物理教材及习题资料，先建立忠实、可追溯的英文 Markdown，再据此生成独立的中文翻译候选稿。

这是一个组合 Workflow，整合原文转写与专业翻译两个任务，但不把它们混成一次不可追溯的生成。

## 2. 支持的功能

- 扫描 PDF 的本地 OCR 和结构解析。
- 指定章节、页码或题目范围的增量处理。
- 公式、图片、表格、题目条件和选项的转写。
- 原文页面与 MinerU Block 的来源定位。
- 原文 Markdown 的逐页核对。
- 数学与物理专业术语翻译。
- 英文原文和中文候选稿分开交付。
- OCR 和翻译不确定性的分阶段记录。
- 已完成解析和已校验章节的复用。

## 3. Skill 组成与职责

- **required — mineru**：负责源 PDF 解析、OCR、页面/Block 定位和图片读取。
- **required — mathtranslations**：负责数学/物理语义翻译、术语表和译文复核规范，按 Markdown 任务适配。
- **optional — stem-notes**：辅助处理理工科图片、公式和复杂版面。不得因为调用该 Skill 而自动转入 LaTeX 讲义或习题求解流程。

三个 Skill 的具体约束分别以各自 SKILL.md 为准；本 Workflow 负责规定任务边界、先后顺序和交付关系。

## 4. 输入与输出

**输入**
- 原始扫描 PDF。
- 目标章节/题号/页码范围。
- 可选：已有 MinerU 解析结果、原文 Markdown、图片资源和项目术语表。

**输出**
- output/<document>/<unit>.source.md：核对后的原文转写。
- output/<document>/<unit>.zh-CN.candidate.md：中文候选译文。
- output/<document>/assets/<unit>/：两个文档实际引用的图片。
- _work/<document>/：MinerU 结果、页码映射、术语表和问题记录。

不默认生成 PDF、Word、习题答案、总结或知识 Skill。

## 5. 工作流程

### 阶段 A：确定范围并复用已有结果

读取项目 AGENTS.md，确定源 PDF 和目标范围。检查已有 MinerU 解析、原文转写、图片资源和术语表。若已有结果可靠且覆盖当前范围，直接续接，不重复 OCR。

### 阶段 B：MinerU 识别

调用 mineru Skill，使用当前已配置的本地环境和可用质量档位。按目标页范围解析，保存文档 ID、解析版本、页码映射和续读定位符。遵循 MinerU 返回的 continuation 信息。

不得擅自安装/升级、修改持久配置、重启服务或使用远程解析。遇到 MinerU 可恢复错误时，先按 Skill 规则向用户说明可选路径，不静默换工具。

### 阶段 C：原文 Markdown 转写与核对

选择性调用 stem-notes 辅助图文理解和数学核对。以 PDF 可见页面为原文依据，建立 .source.md。

核对公式、上下标、正负号、单位、题号、题设、选项、图表、跨页段落及来源页码。所有关键 OCR 疑点必须解决或记录。

### 阶段 D：原文质量门

在翻译前为本次处理单元确定状态：

- **READY**：影响含义的内容已识别并核对，可以翻译。
- **READY_WITH_NOTES**：仍有不影响核心含义的轻微疑点；翻译时继承并标记。
- **BLOCKED**：公式、数字、否定、条件、图示标签或缺页等关键内容无法确认，可能改变原意。

BLOCKED 不得作为已确认原文直接翻译。先回看原页；若仍无法解决，保留明确标记并向用户报告。

### 阶段 E：专业翻译

调用 mathtranslations，读取其数学翻译和复核规范，适配为 Markdown 输出。基于已核对的 .source.md 生成 .zh-CN.candidate.md。

建立或更新项目术语表。保持公式、题目条件、量词、否定、单位、图号、编号和来源定位的语义一致。不解题、不添加教学解释。

### 阶段 F：交叉检查与交付

对照原始 PDF、英文 Markdown 和中文候选稿，检查：

- 页码/章节范围是否一致；
- 标题、段落、题号、选项和图表是否完整；
- 数学公式、数值、单位和不等式是否一致；
- 翻译是否改变逻辑、条件或任务指令；
- 图片引用和本地路径是否有效；
- OCR 疑点是否正确传递到译文问题记录。

## 6. 约束与质量标准

- 原始 PDF 只读，原文 Markdown 与中文候选稿分离。
- 本地优先，未经明确授权不上传任何文档。
- 不把 OCR 输出直接当作准确原文。
- 不翻译尚未确认的关键数学条件而不标记其不确定性。
- 不解答题目，不把翻译任务变成讲义重构。
- 不将候选译文自动提升为正式译文。
- 不覆盖已有的正式译文；需要修改时生成新候选版本。

## 7. 失败处理

- MinerU 不可用或没有可接受的本地质量路径：停止并说明选择，不擅自安装、升级、远程解析或换工具。
- 关键 OCR 内容无法核实：对应单元设为 BLOCKED，不要伪装成确定译文。
- 图片或页面缺失：保留占位标记并记录，不生成替代图。
- 术语存在争议：保留英文原词、记录候选译法和上下文。
- 已有正式译文：保留原文件，另建候选版本。

## 8. 调用示例

“按 WF-DOC-TRANSCRIBE-TRANSLATE 处理这份扫描版英文物理教材的 2.4 节：先忠实转写英文，再生成独立的候选中文版。保留公式、图片、题目条件和页码，不解题，不生成 PDF。”
