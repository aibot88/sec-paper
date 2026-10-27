# sec-paper：网络安全、Web 应用安全与系统安全科研论文套件

`sec-paper` 是一套独立维护、可与 ARIS（Codex / OpenCode 多 Agent 科研框架）无缝组合的**网络安全、Web 应用安全与系统安全**论文选题、实验验证与顶会写作 Skill 仓库。

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
| **[`skills/sec-idea-creator/SKILL.md`](skills/sec-idea-creator/SKILL.md)** | **安全性质先行 + 经典原语映射 + 反缝合铁律 + 独立上下文审稿 + Oracle 先行 Pilot** | 直接替代或并存于通用 `idea-creator`，产出经得起安全 PC 追问的 6 字段选题卡与四态 Pilot 结论 |
| **[`skills/sec-paper-writing/SKILL.md`](skills/sec-paper-writing/SKILL.md)** | **Big-Four 章节骨架 + Threat Model 能力边界表 + A1/A2/A3 自适应攻击者 + Fact Pack 溯源 + USENIX '26 双必选附录** | 杜绝无威胁模型主张、无自适应攻击评估、数字前后打架和未钉死 SHA/CVE 的稿件 |
| **[`references/web-and-system-threat-models.md`](references/web-and-system-threat-models.md)** | **W1–W6 六类 Web/系统攻击者模板 + A1/A2/A3 三级攻击者递进 + In/Out-of-Scope 表** | 选定方向后 3 分钟拉出标准威胁模型边界 |
| **[`references/evaluation-and-oracle-discipline.md`](references/evaluation-and-oracle-discipline.md)** | **4 类合法 Oracle vs 4 类禁用循环 Oracle + 去重单位表 + 随机实验统计规范** | 防止把告警数、覆盖率、LLM 自评或单次短跑当成论文硬证据 |
| **[`references/anti-patterns-and-forbidden-claims.md`](references/anti-patterns-and-forbidden-claims.md)** | **8 大网安立项与写作反模式（Bad → Rewritten 对照）** | 在 Phase 4 筛选和投稿前自检中直接拦下拒稿雷区 |
| **[`references/venues-and-ethics-2026.md`](references/venues-and-ethics-2026.md)** | **四大顶会规范 + Menlo Report 伦理分析 + 90 天协调披露模板 + Open Science 模板** | 把伦理、合规与复现脚本前移到实验设计阶段 |

---

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
/sec-idea-creator "Web API 网关与后端微服务之间的多租户鉴权状态不一致漏洞"
/sec-paper-writing "NARRATIVE_REPORT.md" — venue: USENIX_SEC
```
