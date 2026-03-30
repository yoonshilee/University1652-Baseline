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

## 数据路径约定

- 训练集与测试集统一放在 `data/` 下的扁平目录中，不再默认依赖 `University-Release/` 中间层。
- 数据集体积过大，不随仓库提交；仓库内仅用 `.gitkeep` 或空目录约定保留路径语义。
- 推荐目录布局如下：

```text
data/
  train/
    satellite/
    street/
    drone/
    google/
  train_tour/
    ...
  test/
    query_street/
    gallery_satellite/
    query_drone/
    gallery_drone/
    query_satellite/
    gallery_street/
    ...
  test_tour/
    ...
```

- `train/` 用于模型训练，`test/` 用于 challenge 推理。
- `train_tour/` 与 `test_tour/` 作为额外数据保留，不是 challenge 提交流程的默认入口。
- `test/query_street/` 应为官方 masked challenge query 集；不得用本地非 masked 旧测试集替代最终提交。
- `docs/requirement/query_street_name.txt` 是最终 query 顺序唯一来源，不能自行按文件系统顺序遍历替代。
- 如果数据最初来自如下处理流程：
  - 解压 `University-Release.zip`
  - 生成 `train_tour/`
  - 下载并解压 `train.tar`、`test.tar`、`test_tour.tar`
  - 删除 `University-Release/`
  则最终应把有效路径理解为 `data/train/`、`data/test/`、`data/train_tour/`、`data/test_tour/`。

## 下一阶段任务

### P0：环境与命令收口

- [ ] 运行 `uv sync`，锁定可用依赖。
- [ ] 验证 `uv run python scripts/train.py --help` 可以正常启动。
- [ ] 验证 `uv run python scripts/test.py --help` 可以正常启动。
- [ ] 验证 `uv run cross-view-g2s layout` 与 `validate-submission` 可正常运行。

### P1：数据接口统一

- [ ] 明确 challenge 数据在 `data/` 下的最终目录布局。
- [ ] 生成 query manifest，直接绑定 `docs/requirement/query_street_name.txt` 顺序。
- [ ] 统一 gallery identifier 与图像文件路径映射。
- [ ] 增加缺失文件、重复 id、空目录检查。

### P2：训练与推理收敛到 challenge 场景

- [ ] 审核 `scripts/train.py` 与 `scripts/test.py` 当前默认视角是否真正对齐 ground-to-satellite challenge。
- [ ] 为 partial street-view -> satellite 设定单独的推荐训练/测试命令。
- [ ] 确定最终 submission 使用的 checkpoint、epoch、指标。（当前仓库 `model/` 无 checkpoint，已在执行记录中标注阻塞）
- [ ] 评估是否引入 `third_party/gpu_re_ranking/` 作为可选后处理。

### P3：提交流水线闭环

- [ ] 实现或整理导出 `answer.txt` 的最终脚本。
- [ ] 用 `docs/requirement/query_street_name.txt` 验证顺序一致性。
- [ ] 自动打包 `answer.zip`。
- [ ] 记录 leaderboard 结果、方法摘要与 Moodle 报告要点。

## 推荐命令

```bash
uv sync
uv run cross-view-g2s layout
uv run python scripts/train.py --help
uv run python scripts/test.py --help
uv run cross-view-g2s validate-submission --answer answer.txt --archive answer.zip
```

## 在另一台机器上的完整执行流程

### 1. 配置环境

先检查 GPU 与 CUDA 版本，再安装与之匹配的 PyTorch 轮子：

```bash
nvidia-smi
uv sync
```

- 必须先看 `nvidia-smi` 输出中的 CUDA Version，再决定 PyTorch 安装源。
- 如果 `uv sync` 后 `torch` / `torchvision` 不匹配当前机器 CUDA，请按仓库约定重新安装：

```bash
uv pip install --upgrade --index-url https://download.pytorch.org/whl/cu<version> torch torchvision torchaudio
```

- 其中 `<version>` 需要替换为与该机器匹配的 CUDA 版本号，例如 `cu128`。
- 安装完成后建议立即验证：

```bash
uv run python scripts/train.py --help
uv run python scripts/test.py --help
uv run cross-view-g2s layout
```

### 2. 检查 challenge 数据目录

先确认另一台机器上的官方 challenge 测试集已经按约定放入 `data/test/`：

```bash
uv run python scripts/check_challenge_data.py \
  --query-order docs/requirement/query_street_name.txt \
  --query-root data/test/query_street \
  --gallery-root data/test/gallery_satellite \
  --manifest-dir data/manifest \
  --strict
```

- 期望结果：
  - `query_count = 2579`
  - `gallery_count = 951`
  - `missing_query_count = 0`
  - `duplicate_query_name_count = 0`
  - `duplicate_gallery_id_count = 0`
- 如不满足，先修正数据布局，再继续训练或测试。

### 3. 训练命令

推荐从完整训练集开始训练 partial street-view -> satellite 检索模型：

```bash
uv run python scripts/train.py \
  --name street_sat_baseline \
  --data_dir data/train \
  --views 3 \
  --share \
  --h 256 \
  --w 256 \
  --batchsize 8 \
  --num_epochs 120
```

- 训练输出默认写入 `model/street_sat_baseline/`。
- 关键产物包括：
  - `model/street_sat_baseline/net_*.pth`
  - `model/street_sat_baseline/net_last.pth`
  - `model/street_sat_baseline/opts.yaml`
  - `model/street_sat_baseline/train.jpg`

### 4. 如何记录训练结果

每次准备作为候选提交的训练运行，至少记录以下信息到 `docs/report_notes.md` 或等价实验记录中：

- 机器信息：GPU 型号、`nvidia-smi` 显示的 CUDA 版本。
- 数据根目录：`data/train`。
- 完整训练命令。
- checkpoint 目录名，例如 `street_sat_baseline`。
- 最终使用的 checkpoint 文件名，例如 `net_last.pth` 或某个最佳 epoch。
- 训练轮数、输入分辨率、batch size、是否 `--share`、`--views` 配置。
- 如果做过多次训练，记录每次的差异点与最终选择理由。
- 若后续在 CodaLab 得到成绩，再把 leaderboard 指标追加到同一份记录。

建议直接按下面模板追加：

```text
Date:
Machine:
CUDA (nvidia-smi):
Train data root: data/train
Train command:
Checkpoint dir:
Chosen checkpoint:
Notes / metric / leaderboard:
```

### 5. 测试命令

训练完成后，在官方 challenge 测试集上抽取 query/gallery 特征：

```bash
uv run python scripts/test.py \
  --name street_sat_baseline \
  --test_dir data/test \
  --query_name query_street \
  --gallery_name gallery_satellite \
  --batchsize 256
```

- 该命令默认会生成：
  - `outputs/pytorch_result.mat`
  - `outputs/query_name.txt`
  - `outputs/gallery_name.txt`
- `--name` 必须对应 `model/<name>/` 下存在的已训练 checkpoint。

### 6. 导出提交文件

在特征抽取完成后，导出 challenge 合规的 `answer.txt` 与 `answer.zip`：

```bash
uv run python scripts/export_challenge_submission.py \
  --mat outputs/pytorch_result.mat \
  --query-order docs/requirement/query_street_name.txt \
  --query-paths outputs/query_name.txt \
  --gallery-paths outputs/gallery_name.txt \
  --answer outputs/answer.txt \
  --archive outputs/answer.zip \
  --topk 10
```

- 导出脚本会强制按 `docs/requirement/query_street_name.txt` 顺序写结果。
- 输出 token 只允许 satellite identifier，不带图片后缀。

### 7. 最终校验命令

导出后再次单独运行校验，确保上传前无格式错误：

```bash
uv run cross-view-g2s validate-submission \
  --answer outputs/answer.txt \
  --archive outputs/answer.zip \
  --query-order docs/requirement/query_street_name.txt
```

- 通过后再上传 `outputs/answer.zip`。
- Moodle 简短报告应同时记录所用方法、训练命令、checkpoint 与最终结果。

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
