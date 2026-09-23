# 使用方法

在项目目录中显式调用阶段 skill，或先调用总控：

```text
$workflow-orchestrator
先盘点资料并建立 task_plan.md、findings.md、progress.md；
完成证据审计前不要生成摘要，缺项标记 BLOCKED。
```

```text
$research-positioning
将当前主题压缩为可检验问题，列出主要/替代假设、预测、目标读者和期刊适配证据。
```

```text
$evidence-data-audit
审计变量、单位、样本、时间窗口、配置、脚本、结果、图表和 claim 链，输出 BLOCKED 清单。
```

```text
$manuscript-builder
仅使用 verified 结果和 claims.yaml 生成正文、图注和 SI；保留不显著与反向结果，不补事实。
```

```text
$cross-review
独立模拟编辑、统计、机制和复现审稿，输出 review_round_1.md、claim_calibration.md 和最小修补清单。
```

```text
$submission-revision
检查目标期刊规则、作者/资助/披露、数据代码、AI 使用和返修一致性；不要访问投稿入口或投稿。
```

P2 项目：

```text
$p2-seaice-adapter
将结果映射到 fingerprint + process constraint，检查 FLDS、Rnet、CICE、N_HEAT、OHC 和预算账户是否越界。
```

建议每轮只修一类问题，保存输入哈希、脚本、日志、结果、审稿报告和修改记录。论文作者最终决定科学解释、署名和投稿。
