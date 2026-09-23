# P2 青藏高原—北极海冰领域规则

## INTERNAL-BASELINE

P2 的可复用定位是区域和季节海冰 fingerprint，并提供有边界的过程约束。五个名义高原高度、端点和相邻对照必须保留原始索引；响应形状不能自动升级为阈值。

## 变量边界

- `FLDS` 是向下长波诊断，不是完整净表面热通量。
- `Rnet`、FSNS、FLNS、海冰面积、体积、质量和融化项保持独立账户、单位和掩膜。
- `N_HEAT` 描述跨边界输送差异，不能直接等同局地热汇聚。
- OHC/storage 不能在缺少匹配三维资料时替代局地海洋热收支。
- 冬季冰厚先于夏末状态只能支持 association/consistency，不能单独证明中介因果。

## 配置与统计边界

未核验配置、地形实施、陆面处理、branch/restart 和 spin-up 时，不写 pure topographic effect。缺少逐年中间高度序列时，不声称完整五高度机制检验；预算不闭合时使用 approximate/timing-limited account。反向、不显著和替代路径都必须进入结果或限制。

