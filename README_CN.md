# sec-paper：网络安全、Web 应用安全与系统安全科研论文套件

`sec-paper` 是一套独立维护、可与 ARIS（Codex / OpenCode 多 Agent 科研框架）无缝组合的**网络安全、Web 应用安全与系统安全**全流程科研 Skill 仓库——`/sec-research-pipeline` 一条命令跑完**从研究方向到可投稿稿件**的全链路：`sec-idea-discovery`（选题流水线）→ `sec-experiment-bridge`（实验桥）→ `sec-auto-review-loop`（自动审稿循环）→ 叙事报告 → `sec-paper-writing`（顶会成稿+投稿审计）。

目标顶会：**IEEE S&P (Oakland)、USENIX Security、ACM CCS、NDSS**，同时覆盖 **PETS、ACSAC、AsiaCCS、RAID**。

---

## 为什么要把网安论文的 Skill 单独拆出来维护？

通用 ML 选题与写作流水线（例如原版 `idea-creator`）直接套用到 Web 安全与系统安全时，会出现 6 个结构性失真：

1. **把“近两年论文关键词空白”当成真安全问题**：只读前 3 页、只查近 2 年 ML 顶会，漏掉 10 年前的系统安全奠基工作（如 *Enemy of the State*, USENIX Security '12）、协议 RFC 规范与框架实现细节。
2. **在“四合一缝合怪”和“单模块教条”之间两头犯错**：
   - 放任发散时，AI 极易写出“把依赖图 + 三层检测 + 区块链溯源 + 风险传播拼成统一框架”的拼盘点子；
   - 机械限制“只准一个模块，第二个模块就是包装”时，又会错杀需要**状态快照 + 键值推断 + 漏洞 Oracle** 闭环耦合才能成立的系统安全工作（如 *Atropos*, USENIX Security '24）。
3. **把“可行性”等同于“GPU 小时 + 静态数据集”**：忽略了 Web 安全真正的瓶颈是**测试授权、多租户/多角色状态复现、以及非循环的真值判定器（Oracle）**；甚至因为“本机无 GPU”错误跳过原本只需容器和浏览器的 Pilot 实验。
4. **把“实验无法执行（`EXPERIMENT_BLOCKED`）”误判成“科学假设被证伪（`HYPOTHESIS_REFUTED`）”**。
5. **同线程既当运动员又当裁判**：保存生成候选时的 `threadId` 并在同一上下文里续聊排序，导致强烈的自锚定偏见。
6. **强制套用“单次运行、2 小时、指标 +X%”跑分模板**：违背安全评测基本功（Klees et al., *Evaluating Fuzz Testing*, ACM CCS '18），把 HTTP 200 或未去重告警当漏洞数，或按正负号粗暴淘汰有诊断价值的负结果。

---

## `sec-paper` 的核心修正与亮点

| 模块 | 核心机制 | 解决什么痛点 |
|------|----------|--------------|
| **[`skills/sec-idea-discovery/SKILL.md`](skills/sec-idea-discovery/SKILL.md)** | **W1 全流程编排器**：读约束与授权范围 → 文献 → 生成+Pilot → 查新 → PC 审稿 → 细化+实验计划；带 `run_state` 证据门与断点续跑 | 替代通用 `idea-discovery`，把"只有 idea-creator"补成完整流水线 |
| **[`skills/sec-research-lit/SKILL.md`](skills/sec-research-lit/SKILL.md)** | **Big-Four 10–15 年奠基 + 近 3 年前沿 + RFC/W3C/NVD/修复 SHA 多源检索**，按信任边界/原语映射/Oracle 拆解邻作 | 防止只看近两年 ML 论文关键词空白、漏掉系统安全奠基工作 |
| **[`skills/sec-idea-creator/SKILL.md`](skills/sec-idea-creator/SKILL.md)** | **安全性质先行 + 经典原语映射 + 反缝合铁律 + 独立上下文审稿 + Oracle 先行 Pilot** | 产出经得起安全 PC 追问的 6 字段选题卡与四态 Pilot 结论 |
| **[`skills/sec-novelty-check/SKILL.md`](skills/sec-novelty-check/SKILL.md)** | **根因机制/信任边界级查新**（而非产品名），兼容 `idea_discovery_gate.py` 的 PROCEED/CAUTION/ABANDON 回执 | 把"换个产品名"挡在门外，又不错杀有真实 delta 的邻近工作 |
| **[`skills/sec-research-review/SKILL.md`](skills/sec-research-review/SKILL.md)** | **冷读式 Big-Four PC 攻击审稿**：威胁模型循环前提、可删性、Oracle 循环、A3 缺位、伦理授权 | 替代通用 ML 评审提问（模型结构/训练曲线），直击安全拒稿点 |
| **[`skills/sec-research-refine/SKILL.md`](skills/sec-research-refine/SKILL.md)** | **双锚点细化**：Security Problem Anchor + Threat-Model Anchor 冻结，主张迁移必须显式记账 | 防止细化过程悄悄漂移威胁模型或缝合模块 |
| **[`skills/sec-experiment-plan/SKILL.md`](skills/sec-experiment-plan/SKILL.md)** | **Claim→Evidence 矩阵 + RQ1–RQ4（含强制 A3）+ 消融 + 统计协议 + 伦理检查点** | 实验规划期就锁死 Oracle 与去重单位，规划阶段拒掉循环 Oracle |
| **[`skills/sec-research-refine-pipeline/SKILL.md`](skills/sec-research-refine-pipeline/SKILL.md)** | **串接 refine → experiment-plan**，产出 FINAL_PROPOSAL + EXPERIMENT_PLAN + TRACKER + SUMMARY | 一键从选题走到可执行实验命令 |
| **[`skills/sec-research-pipeline/SKILL.md`](skills/sec-research-pipeline/SKILL.md)** | **W0 总编排器**：discovery → bridge → review-loop → summary → writing；Gate 1 选题门 + Gate 2 写作门 + run_state 阶段记录 | 一条命令从方向走到投稿，`AUTO_WRITE`/`VENUE`/`AUTHORIZATION` 可控 |
| **[`skills/sec-experiment-bridge/SKILL.md`](skills/sec-experiment-bridge/SKILL.md)** | **S1.5 实验桥**：解析 EXPERIMENT_PLAN → 实现 靶场+Oracle+去重+A3 组件 → 安全代码审查 → sanity → /run-experiment 或 /experiment-queue 部署 → Oracle 验证结果 | 交付的不是"指标"而是每行结果都带 Oracle 验证与去重单位的证据；阻断循环 Oracle 进实验 |
| **[`skills/sec-result-to-claim/SKILL.md`](skills/sec-result-to-claim/SKILL.md)** | **证据→主张路由**：`claim_supported / partial / contradicted` + 网安专属标注（`oracle_gap`/`a3_pending`/`scope_mismatch`），每批新证据后重跑 | 被证伪的主张永远进不了审稿循环 |
| **[`skills/sec-ablation-planner/SKILL.md`](skills/sec-ablation-planner/SKILL.md)** | **四轴安全消融**：组件可删性 / 攻击者层级(A1→A3) / Oracle 覆盖度 / 目标族多样性，每次只动一个变量 | 直接回应"哪个模块是装饰"的 PC 追问 |
| **[`skills/sec-experiment-audit/SKILL.md`](skills/sec-experiment-audit/SKILL.md)** | **S2.5 证据层独立审计**：幻影结果、Oracle 被绕过/假真值、去重造假、统计协议、授权合规、A3 真伪 | 代码审查查不出来的证据层造假在这里拦 |
| **[`skills/sec-auto-review-loop/SKILL.md`](skills/sec-auto-review-loop/SKILL.md)** | **S2 硬门控审稿循环**：5 条安全硬门（威胁模型/Oracle/A3/伦理/SHA 钉死）独立于分数，≤4 轮 review→fix→re-review | 分数再高硬门不过也不能 STOP；修复轮次上限防无限补丁循环 |
| **[`skills/sec-paper-writing/SKILL.md`](skills/sec-paper-writing/SKILL.md)** | **W3 编排**：复用通用 paper-plan/paper-write/figure/compile/claim-audit/citation-audit/integrity-forensics + 自有 Big-Four 骨架、Threat Model 专章、Fact Pack 写锁、双附录 | 领域中立工序复用 ARIS，安全内容契约独握 |
| **[`skills/sec-paper-improve-loop/SKILL.md`](skills/sec-paper-improve-loop/SKILL.md)** | **成稿后文本层硬门循环**：数字对齐、威胁模型一致性、A3 小节实含量化、禁用表述、匿名性、venue 合规 | 拦截润色过程引入的文本层新错 |
| **[`references/web-and-system-threat-models.md`](references/web-and-system-threat-models.md)** | **W1–W6 六类 Web/系统攻击者模板 + A1/A2/A3 三级攻击者递进 + In/Out-of-Scope 表** | 选定方向后 3 分钟拉出标准威胁模型边界 |
| **[`references/evaluation-and-oracle-discipline.md`](references/evaluation-and-oracle-discipline.md)** | **4 类合法 Oracle vs 4 类禁用循环 Oracle + 去重单位表 + 随机实验统计规范** | 防止把告警数、覆盖率、LLM 自评或单次短跑当成论文硬证据 |
| **[`references/anti-patterns-and-forbidden-claims.md`](references/anti-patterns-and-forbidden-claims.md)** | **8 大网安立项与写作反模式（Bad → Rewritten 对照）** | 在 Phase 4 筛选和投稿前自检中直接拦下拒稿雷区 |
| **[`references/venues-and-ethics-2026.md`](references/venues-and-ethics-2026.md)** | **四大顶会规范 + Menlo Report 伦理分析 + 90 天协调披露模板 + Open Science 模板** | 把伦理、合规与复现脚本前移到实验设计阶段 |

---

## 独立运行说明（不依赖 ARIS）

### 当前独立版的运行与验收入口

**Codex 生成/实现/执行，AntiGravity/Gemini 审稿，禁止回退 Codex 自审。**
安装器的 --project 会初始化项目配置和 .aris/sec-paper.json；旧安装可运行：

```bash
python3 /path/to/sec-paper/tools/project.py init --project /path/to/project
python3 /path/to/sec-paper/tools/project.py doctor --project /path/to/project --live
python3 -m unittest discover -s tests -v
```

完整契约见 [workflow-contract](shared-references/workflow-contract.md)。
本机作业生命周期由 tools/jobs.py 的 start/status/wait/cancel/queue 实现；
真实 Gemini 调用、trace 与输入版本绑定由 tools/review.py 实现。
新的 sec-paper-audit 包含五项独立终审（主张↔原始数据、引用语境、最强拒稿论证、
适用证明或有理由的 N/A、匿名复现包），再执行 paper_check.py 和 submission_gate.py。
它们是投稿必需项，**不再依赖 ARIS 通用审计 Skill，也不能以六项人工清单替代**。

只实现并验证了 local POSIX 作业后端；SSH/GPU 后端需明确适配，不支持就阻断。
回归测试中的模型回执和实验是显式测试夹具，不代表真实研究或论文审稿通过。
当前会场官方 CFP、真实实验、TeX/PDF 工具和真实终审仍是投稿验收前提；
最终点击投稿属于单独的人类确认操作。许可证及来源见 THIRD_PARTY_NOTICES.md。

`sec-paper` 是**自包含**项目：`tools/` 下 vendor 了运行所需的全部确定性工具——`run_state.py`（断点续跑状态）、`idea_discovery_gate.py`（已参数化为 `sec-*` 阶段名，支持 `--phases`/`--review-phases` 覆盖）、`reviewer_route.py`（审稿后端解析）、`threat_scan.py`、`research_wiki.py`、`antigravity-exec/server.py`（本机 `agy` 审稿桥）。

审稿后端配置（每个项目一次，Codex 执行 × AntiGravity/Gemini 审稿 → 跨家族 `accept` 回执）：

```bash
cp /Users/aibot/script/sec-paper/.aris/reviewer.example.json <项目>/.aris/reviewer.json
```

可选集成仅包括显示/知识连接器和通用辅助工具。核心运行、监控、队列、真实审稿与最终审计已有本仓库实现，不再以“宿主可选组件”代替。

## 一键安装与使用（不污染上游 ARIS 仓库）

```bash
# 1. 安装到指定项目（例如 ARIS 或你的研究项目目录 .agents/skills/）
bash /Users/aibot/script/sec-paper/tools/install_sec_paper.sh --project /Users/aibot/script/ARIS

# 2. 如果希望在该项目中让 /idea-creator 直接走网安版 /sec-idea-creator：
bash /Users/aibot/script/sec-paper/tools/install_sec_paper.sh --project /Users/aibot/script/ARIS --override-idea-creator

# 3. 安装到本机 OpenCode / Codex 全局技能目录：
bash /Users/aibot/script/sec-paper/tools/install_sec_paper.sh --opencode
bash /Users/aibot/script/sec-paper/tools/install_sec_paper.sh --codex
```

调用示例：

```text
# 端到端全流程（推荐入口）：方向 → 选题 → 实验 → 审稿循环 → 报告 → 投稿成稿
/sec-research-pipeline "Web API 网关与后端微服务之间的多租户鉴权状态不一致漏洞" — venue: USENIX_SEC

# 或从中间阶段进入
/sec-idea-discovery "跨租户 BOLA"           # 选题流水线（含 pilot）
/sec-experiment-bridge "EXPERIMENT_PLAN.md"  # 实现 harness+Oracle+A3 → 部署 → 收集证据
/sec-auto-review-loop "results/"             # 硬门控自动审稿循环
/sec-paper-writing "NARRATIVE_REPORT.md" — venue: USENIX_SEC
```
