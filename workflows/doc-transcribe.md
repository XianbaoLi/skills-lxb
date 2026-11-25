---
workflow_id: WF-DOC-TRANSCRIBE
name: 扫描版 PDF 忠实转写
name_en: Scanned PDF to Source Markdown
version: 1.0.0
status: draft
category: document-processing
execution_model: agent-guided
implementation: documentation-only
capabilities:
  - 扫描版或图像型 PDF 的 OCR 与内容转写
  - 指定页码、章节和小节的定范围处理
  - 数学公式、表格、图片及图注的提取与核对
  - 保留 PDF 页码、印刷页码和 MinerU 定位信息
  - 生成保留原文语言的 Markdown
skills:
  required:
    - mineru
  optional:
    - stem-notes
inputs:
  - 原始 PDF 文件
  - 用户指定的页码、章节或处理范围
  - 可选：已有 MinerU 解析结果、可编辑源文件、项目 AGENTS.md
outputs:
  - 原文语言的 source Markdown
  - Markdown 实际引用的图片资源
  - 必要的解析索引与 OCR 疑点记录
not_supported:
  - 自动翻译
  - 教材总结或知识重构
  - 自动解答习题
  - 未经要求生成 LaTeX、PDF 或学习应用
approval_gates:
  - 安装或升级 MinerU 及其依赖
  - 修改 MinerU 持久配置、启动或重启服务
  - 使用远程解析或上传原始文件
  - 改用其他解析器处理 MinerU 的可恢复错误
---

# WF-DOC-TRANSCRIBE — 扫描版 PDF 忠实转写

## 1. 目的与适用场景

将扫描版、拍照版或图像型 PDF 中指定的内容转写为可阅读、可继续编辑的 Markdown。目标是忠实恢复原文，不是总结或重新创作。

适用于英文或中文教材、讲义、习题集、论文及其他包含公式、图表和复杂排版的资料。

## 2. 支持的功能

- OCR 和文档结构解析。
- 按页码、章节或小节限定处理范围。
- 公式、矩阵、上下标、表格和列表的结构化转写。
- 原始图片、示意图、曲线图和表格的保留或裁剪。
- PDF 实际页序、书籍印刷页码和解析定位符的追踪。
- 长文档分段处理和已有解析结果复用。
- OCR 疑点与疑似原书错误的独立记录。

不负责翻译、解题、教学扩写或知识体系重构。

## 3. Skill 组成与职责

- **required — mineru**：负责 PDF 解析、OCR、公式和版面识别、分页续读、页面/Block 图片及稳定定位符。执行前遵循 skills/mineru/SKILL.md。
- **optional — stem-notes**：在理工科公式、图示、习题结构或图片处理复杂时，选择性参考其图文核对和材料组织方法。遵循 skills/stem-notes/SKILL.md 及相关参考文件，但不自动触发其问卷、LaTeX 生成和习题求解流程。

## 4. 输入与输出

**输入**
- 原始 PDF。
- 指定章节、题号或 PDF 页码范围。
- 可选：既有 MinerU 文档 ID、解析结果、TeX/Word 源文件、项目排版约定。

**输出**
- output/<document>/<unit>.source.md：原文语言的 Markdown。
- output/<document>/assets/<unit>/：正文实际引用的图片。
- _work/<document>/mineru/：可复用的解析结果和定位信息。
- _work/<document>/manifest.json：来源、范围、解析版本、质量档位、页码映射和完成状态。
- _work/<document>/ocr-issues.md：仅在存在未解决疑点时创建。

沿用用户已有目录约定，不为符合示例而创建空目录。

## 5. 工作流程

1. **确认范围与复用情况**：读取项目 AGENTS.md，定位源 PDF 和目标范围，检查已有解析结果及前次转写，区分 PDF 页序和印刷页码。
2. **检查本地环境**：检查 mineru 命令和版本。当前 MinerU Skill 要求 MinerU >=4.0,<5、Python >=3.11,<3.15。若 JSON 版本查询不兼容，按 Skill 说明尝试旧版版本查询。不得擅自安装或升级。
3. **解析目标页面**：优先复用现有 MinerU 结果；缺失时按目标页范围解析。使用结构化输出作流程判断，遵循 MinerU 返回的 next_request 或续读命令，不猜测下一页，不重复从第一页解析。
4. **整理原文 Markdown**：保留原始语言、章节层级、段落顺序、定义、定理、推导、例题、习题、题目选项、脚注、图表和交叉引用。公式使用 LaTeX，保留编号和符号。
5. **核对原始页面**：对扫描页、公式密集页、表格页、复杂图示及 OCR 疑点查看原页图像。重点核对正负号、上下标、希腊字母、矢量/算符标记、积分、求和、矩阵、单位、题设条件和图号。
6. **处理图片**：优先保留清晰原图；必要时从原 PDF 高清裁剪。不得用生成图替代原图，不凭空补全模糊标注。图片以相对路径引用。
7. **记录不确定性**：可由原页证据确认的 OCR 错误可以修正；原书疑似错误应保留原貌并另行注明。无法辨认的文字或符号标记为待核对，不按专业常识猜测。
8. **检查交付完整性**：确认请求范围均已覆盖，题号、公式、图表、单位和引用未丢失，图片路径有效，未解决问题已记录。

## 6. 约束与质量标准

- 原始 PDF 只读，不修改、不覆盖。
- 本地解析优先；不得静默添加 --remote 或上传文档。
- MinerU 缺少可用质量档位或出现可恢复错误时，先向用户说明选项，不静默改用其他解析器。
- 不因使用本 Workflow 而默认安装、下载模型、修改服务配置或清理缓存。
- OCR 结果不是事实来源；可见 PDF 页面才是原文内容依据。
- 对高保真章节转写，应逐页核对请求范围；至少所有影响语义的 OCR 疑点必须核实或明确标记。

## 7. 失败处理

遇到 MinerU 不可用、版本不兼容、没有可接受的本地解析质量、源文件损坏或关键内容无法辨认时，停止相应步骤并报告原因。需要安装、升级、远程解析或替代解析器时，等待用户明确授权。

## 8. 调用示例

- “按 WF-DOC-TRANSCRIBE 忠实转写这份扫描教材的 2.4 节，保留英文原文。”
- “只处理 PDF 第 20–28 页，生成 Markdown，不翻译、不解题。”
- “复用已有 MinerU 解析结果，继续完成下一节。”
