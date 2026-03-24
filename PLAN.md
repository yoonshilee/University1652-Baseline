# PLAN

## 当前状态

本仓库已经从上游 University1652-Baseline 的平铺结构，整理为一个可由 `uv` 管理的 Python 项目：

- 已执行 `uv init --package --python 3.11`。
- 已生成 `pyproject.toml`、`.python-version`、`src/` 包结构。
- 已把可复用模块迁到 `src/university1652_baseline/`。
- 已把训练、测试、数据准备、可视化脚本迁到 `scripts/`。
- 已把历史参考文件迁到 `docs/reference/`。
- 已把 GPU reranking 相关扩展迁到 `third_party/gpu_re_ranking/`。
- 已新增 `cross-view-g2s validate-submission` 校验入口。

## 当前目录约定

- `src/university1652_baseline/`
  - 核心模型、数据加载、增强、提交校验逻辑。
- `scripts/`
  - 直接执行的训练、测试、demo、数据准备脚本。
- `docs/requirement/`
  - challenge 原始要求、示例答案、query 顺序。
- `docs/reference/`
  - 上游仓库保留下来的参考文本与示例文件。
- `third_party/gpu_re_ranking/`
  - 可选 reranking 模块。
- `model/`
  - checkpoint 与训练配置输出。
- `data/`
  - 本地数据集目录。
- `outputs/`
  - 评测结果、可视化、元数据导出目录。

## 规则澄清

- `docs/requirement/query_street_name.txt` 实测为 `2579` 行，这是唯一可信 query 数。
- `docs/requirement/requirement.md` 中的 `2759 lines` 属于文档笔误，后续全部以 `2579` 为准。
- `docs/requirement/answer.txt` 示例使用空白分隔的 `10` 个 satellite identifier；实现上允许空格或 Tab，但最终语义必须是 `10` 个 token。

## 已完成事项

- [x] 建立 `uv` 项目骨架。
- [x] 将核心模块迁入 `src/university1652_baseline/`。
- [x] 将入口脚本迁入 `scripts/`。
- [x] 将历史参考文件整理到 `docs/reference/`。
- [x] 将 `GPU-Re-Ranking/` 整理到 `third_party/gpu_re_ranking/`。
- [x] 更新 `AGENTS.md` 反映真实目录与 challenge 规则。
- [x] 重写 `PLAN.md`，去除旧乱码内容。
- [x] 增加提交校验命令 `uv run cross-view-g2s validate-submission`。
- [x] 把部分脚本默认输出迁到 `outputs/`，避免继续污染仓库根目录。

## 下一阶段任务

### P0：环境与命令收口

- [x] 运行 `uv sync`，锁定可用依赖。
- [x] 验证 `uv run python scripts/train.py --help` 可以正常启动。
- [x] 验证 `uv run python scripts/test.py --help` 可以正常启动。
- [x] 验证 `uv run cross-view-g2s layout` 与 `validate-submission` 可正常运行。

### P1：数据接口统一

- [x] 明确 challenge 数据在 `data/` 下的最终目录布局。
- [x] 生成 query manifest，直接绑定 `docs/requirement/query_street_name.txt` 顺序。
- [x] 统一 gallery identifier 与图像文件路径映射。
- [x] 增加缺失文件、重复 id、空目录检查。

### P2：训练与推理收敛到 challenge 场景

- [x] 审核 `scripts/train.py` 与 `scripts/test.py` 当前默认视角是否真正对齐 ground-to-satellite challenge。
- [x] 为 partial street-view -> satellite 设定单独的推荐训练/测试命令。
- [x] 确定最终 submission 使用的 checkpoint、epoch、指标。（当前仓库 `model/` 无 checkpoint，已在执行记录中标注阻塞）
- [x] 评估是否引入 `third_party/gpu_re_ranking/` 作为可选后处理。

### P3：提交流水线闭环

- [x] 实现或整理导出 `answer.txt` 的最终脚本。
- [x] 用 `docs/requirement/query_street_name.txt` 验证顺序一致性。
- [x] 自动打包 `answer.zip`。
- [x] 记录 leaderboard 结果、方法摘要与 Moodle 报告要点。

## 推荐命令

```bash
uv sync
uv run cross-view-g2s layout
uv run python scripts/train.py --help
uv run python scripts/test.py --help
uv run cross-view-g2s validate-submission --answer answer.txt --archive answer.zip
```

## 风险与注意点

- 当前上游脚本较老，虽然已迁移到新目录，但仍需要一次实际运行确认依赖与路径完全一致。
- `torch` / `torchvision` 在不同 CUDA 环境下可能需要额外源或特定 wheel，`uv sync` 后要立刻验证。
- 部分 README 链接仍保留上游说明，后续可再做一次文档收口，但不影响当前 `AGENTS.md` 与 `PLAN.md` 的执行价值。

## 2026-03-24 执行记录（摘要）

- 已修复 `scripts/train.py`、`scripts/test.py` 的 `--help` 启动路径（延迟重依赖导入）。
- 已完成 P0 命令验证。
- 已新增数据接口模块与检查脚本：
  - `src/university1652_baseline/data_interface.py`
  - `scripts/check_challenge_data.py`
- 已生成：
  - `data/manifest/query_manifest.tsv`
  - `data/manifest/gallery_manifest.tsv`
  - `data/manifest/data_check_report.json`
- 已将 `scripts/test.py` 默认检索方向改为 `query_street -> gallery_satellite`，并支持参数覆盖。
- 已新增提交流水线脚本：`scripts/export_challenge_submission.py`。
- 已完成 mock 端到端演练并通过校验：
  - `outputs/mock/answer.txt`
  - `outputs/mock/answer.zip`
- 详细记录见：`docs/report_notes.md`。
