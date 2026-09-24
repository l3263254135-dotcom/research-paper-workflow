# Claim—Evidence Schema

`claims.yaml` 的每条记录至少包含：

```yaml
- claim_id: C001
  text: ""
  evidence_ids: []
  result_ids: []
  figure_ids: []
  evidence_level: source-backed
  alternative_explanations: []
  limitations: []
  allowed_verbs: []
  status: verified
  provenance: OUR-DESIGN
  author_decision: ""
```

证据等级：`source-backed` 为直接来源支持，`inference` 为受约束推断，`to_verify` 为需额外资料，`blocked` 为依赖缺失。核心 claim 必须能定位到结果和图表；没有直接证据的句子不得写成已验证结果。

方法建议来源与科学证据分开记录：`BOOK-SUPPORTED`、`ARTICLE-SUPPORTED`、`INTERNAL-BASELINE`、`OUR-DESIGN`、`BLOCKED-SOURCE`。`provenance` 不得替代 `evidence_level`。
