# 使用方法

在项目目录中显式调用阶段 skill，或先调用总控：

```text
$workflow-orchestrator
先盘点资料并建立 task_plan.md、findings.md、progress.md；
依次完成可发表性、证据契约、分析、图表、写作、交叉审稿和投稿检查；
完成证据审计前不要生成摘要，缺项标记 BLOCKED。
```

```text
$research-positioning
将当前主题压缩为可检验问题，列出主要/替代假设、预测、目标读者、最低可发表单位、候选标题和期刊适配证据。
```

```text
$ai-research-production
建立项目配置、数据边界、双 AI 角色、运行日志和版本记录；
验证生成代理与审稿代理是否真正隔离，不能验证时标记 NON-INDEPENDENT。
```

```text
$evidence-data-audit
审计变量、单位、样本、时间窗口、配置、脚本、结果、图表、claim 和正文追踪链，输出 BLOCKED 清单。
```

```text
$analysis-build
根据作者确认的方法运行或审计分析脚本，生成字段完整、可复算的 analysis_results.json；
保留不显著、反向、失败和替代结果。
```

```text
$figure-argument
把每张图绑定到结果和 claim，生成 figure_manifest.yaml 与图注草稿；
检查单位、误差、颜色、可读性和正文引用。
```

```text
$figure-optimization
在已核验结果和 story_spine.yaml 基础上规划图表故事板；
重新安排主文图、补充图、表格和面板顺序；
提出不改变数据、统计口径和科学结论的视觉优化，并记录图表变更。
```

```text
$manuscript-reconstruction
将 manuscript_source.md 作为固定事实来源；
第一阶段生成 fact_ledger.yaml、reconstruction_brief.md、story_spine.yaml、section_map.yaml 和 rewrite_decision_log.md；
作者将 reconstruction_approval 设置为 approved 后，再按 Results、Discussion、Introduction、Conclusion、Abstract、Title 的顺序逐节重写。
```

```text
$manuscript-builder
仅使用 verified 结果和 claims.yaml 生成正文、图注和 SI；按科学论证、结构、段落、句子、用词五轮检查；
保留不显著与反向结果，不补事实。
```

```text
$cross-review
独立模拟编辑、统计、机制、图表、引用、语言和复现审稿，输出 review_round_1.md、claim_calibration.md、score_history.json 和最小修补清单。
```

```text
$submission-revision
检查目标期刊规则、作者/资助/披露、数据代码、AI 使用、校样和返修一致性；不要访问投稿入口或投稿。
```

```text
$science-communication
从已校准 claim 生成会议摘要、扩展摘要、口头报告、墙报或公众版说明；
改变受众与格式，不提高证据强度。
```

P2 项目：

```text
$p2-seaice-adapter
将结果映射到 fingerprint + process constraint，检查 FLDS、Rnet、CICE、N_HEAT、OHC 和预算账户是否越界。
```

建议每轮只修一类问题，保存输入哈希、脚本、日志、结果、审稿报告和修改记录。论文作者最终决定科学解释、署名和投稿。
