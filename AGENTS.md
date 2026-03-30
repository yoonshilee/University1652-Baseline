# AGENTS

## Scope

本仓库只服务一个明确目标：基于 University-1652 与当前 UAVM challenge 材料，完成 partial street-view 到 satellite 的检索、导出合规 `answer.txt`、打包 `answer.zip`，并整理可复现实验记录与课程报告素材。

## Canonical Facts

以下事实以仓库内现有材料为准：

- 任务类型：partial street image -> satellite image cross-view retrieval。
- 规范查询顺序文件：`docs/requirement/query_street_name.txt`。
- 查询数：`2579`。
- Gallery 数：`951`。
- 每个 query 必须返回 `10` 个 satellite identifier。
- 提交文件名必须是 `answer.txt`，压缩包名必须是 `answer.zip`。
- `docs/requirement/answer.txt` 示例只包含 identifier，不带图片后缀。
- `docs/requirement/requirement.md` 中曾写到 `2759 lines`，但与真实 `query_street_name.txt` 行数不一致；仓库内统一以 `2579` 为唯一有效值。
- 当前在线提交平台以 `https://www.codabench.org/competitions/15251/` 为准；如平台 phase、deadline、指标或提交次数限制发生变化，以上传页面实时说明为最终依据。
- 课程还要求在 UM Moodle 提交简短报告或方法说明。

## Current Layout

当前仓库按 `uv` 项目组织为：

- `src/university1652_baseline/`：可复用 Python 模块。
- `scripts/`：训练、测试、数据准备、可视化、维护脚本。
- `docs/requirement/`：challenge 规则、示例答案、query 顺序。
- `docs/reference/`：上游 baseline 的历史参考文件。
- `docs/assets/`、`docs/tutorial/`、`docs/research/`：示例、教程和资料页。
- `third_party/gpu_re_ranking/`：可选 reranking 扩展。
- `model/`：训练输出 checkpoint 与 `opts.yaml`。
- `data/`：本地数据集根目录，按 `.gitignore` 不入库。
- `outputs/`：测试结果、可视化结果、中间导出，按 `.gitignore` 不入库。

## Environment Rules

- 使用 `uv` 管理环境、依赖与命令。
- Python 版本固定为 `3.11`，见 `.python-version`。
- 推荐先执行 `uv sync`。
- 核心命令：
  - `uv run python scripts/train.py --help`
  - `uv run python scripts/test.py --help`
  - `uv run cross-view-g2s layout`
  - `uv run cross-view-g2s validate-submission --answer answer.txt --archive answer.zip`
- Check cuda version before installing torch if you have to use torch in this project
- Use `uv add <package-name>` while adding lib package. Use `uv pip install --upgrade --index-url https://download.pytorch.org/whl/cu<version> torch corchvision torchaudio` while installing torch dependencies. `<>` means you have to replace the term inside.

## Dataset Layout Contract

当前仓库对“最终落地后的本地数据目录”采用扁平约定，而不是继续假设压缩包中的 `University-Release/` 目录长期存在。

- 默认训练根目录：`data/train/`
- 默认 challenge 测试根目录：`data/test/`
- 可选 tour 训练目录：`data/train_tour/`
- 可选 tour 测试目录：`data/test_tour/`

推荐把你给出的数据处理命令的产物整理到以下结构：

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

额外约束：

- `scripts/train.py` 默认应把 `data/train/` 视为训练入口。
- `scripts/test.py` 默认应把 `data/test/` 视为 challenge 推理入口。
- `scripts/check_challenge_data.py` 默认应检查 `data/test/query_street/` 与 `data/test/gallery_satellite/`。
- 只有在用户明确说明仍保留原始解压目录时，才再使用 `University-Release/train` 或 `University-Release/test` 这类旧路径。
- `train_tour/` 与 `test_tour/` 不是提交校验的 canonical 路径；只有显式实验需要时才消费。

## Agents

### 1. Rule And Submission Agent

职责：

- 维护 challenge 规则的最终解释。
- 以 `docs/requirement/` 作为唯一规则来源。
- 防止输出命名、顺序、行数、压缩结构出错。

必须检查：

- `answer.txt` 存在。
- 行数严格等于 `2579`。
- 每行严格等于 `10` 个 token。
- token 不带 `.jpg/.jpeg/.png` 等图片后缀。
- query 顺序与 `docs/requirement/query_street_name.txt` 一致。
- `answer.zip` 名称正确，且根目录包含 `answer.txt`。
- 上传前重新核对 CodaBench 页面上的 phase、deadline、metric 与 submission limit，避免格式正确但平台规则不符。

当前落地点：

- `src/university1652_baseline/submission.py`
- `src/university1652_baseline/cli.py`

### 2. Data Interface Agent

职责：

- 约定 `data/` 下训练集、测试集、challenge query/gallery 的布局。
- 保留 `query_street_name.txt` 的原始顺序。
- 维护 gallery identifier 与图像文件之间的映射规则。
- 优先识别扁平数据路径：`data/train/`、`data/test/`、`data/train_tour/`、`data/test_tour/`。

建议产物：

- `data/manifest/` 下的 query manifest。
- 缺失文件、重复 id、空目录检查脚本。
- 统一数据加载入口，避免脚本各自约定路径。

当前相关脚本：

- `scripts/prepare_cvusa.py`
- `scripts/prepare_limit_view.py`
- `src/university1652_baseline/folder.py`

### 3. Retrieval Modeling Agent

职责：

- 维护 backbone、embedding、loss、pooling 与多视角编码策略。
- 优先保证 partial street-view 到 satellite 的检索效果。
- 控制训练实现与导出逻辑的兼容性。

当前相关模块：

- `src/university1652_baseline/model.py`
- `src/university1652_baseline/autoaugment.py`
- `src/university1652_baseline/random_erasing.py`
- `src/university1652_baseline/circle_loss.py`

### 4. Training And Experiment Agent

职责：

- 维护可复现训练入口。
- 记录数据位置、超参数、最佳 epoch、最佳 checkpoint。
- 保证最终提交能追溯到具体模型和配置。

当前相关脚本：

- `scripts/train.py`
- `scripts/train_no_street.py`
- `scripts/train_cvusa.py`
- `scripts/train_*_sample.py`

必须记录：

- 数据根目录假设。
- 训练命令。
- 最优指标。
- 使用的 checkpoint 路径。

### 5. Retrieval And Export Agent

职责：

- 从 query/gallery 批量抽特征。
- 计算 top-10 排序。
- 导出 challenge 合规的 `answer.txt`。

硬约束：

- 只能使用 `query_street_name.txt` 定义的顺序。
- 输出只写 satellite identifier。
- 不得夹带图片扩展名。
- 默认输出应进入 `outputs/` 或提交根文件，不应再向仓库根目录散落临时文件。

当前相关脚本：

- `scripts/test.py`
- `scripts/demo.py`
- `scripts/demo_4K.py`
- `scripts/evaluate_gpu.py`

### 6. Validation And Report Agent

职责：

- 复核导出结果。
- 组装 `answer.zip`。
- 维护课程报告所需的方法、配置、结果摘要。

建议产物：

- `outputs/answer.txt`
- `outputs/answer.zip`
- `docs/report_notes.md` 或等价实验摘要

## Collaboration Rules

- Rule And Submission Agent 对提交格式拥有最终解释权。
- Data Interface Agent 负责 query 顺序与 identifier 映射，其他模块不得自行发明遍历顺序。
- Retrieval And Export Agent 必须消费 Data Interface Agent 产生的顺序或 manifest。
- Training And Experiment Agent 必须暴露最终提交所用 checkpoint。
- Validation And Report Agent 是上传前的最后一道门。

## Definition Of Done

仅当以下条件同时成立，项目才算完成：

- `uv` 已成为项目默认环境管理方式。
- 代码与文档清楚说明了训练、测试、导出、校验命令。
- 能从本地数据生成 challenge 格式的 `answer.txt`。
- `answer.txt` 恰好 `2579` 行。
- 每行恰好 `10` 个 satellite id。
- 顺序与 `docs/requirement/query_street_name.txt` 完全一致。
- `answer.zip` 文件名正确。
- `answer.zip` 根目录包含 `answer.txt`。
- 所用 checkpoint、配置、结果说明足以支撑 UM Moodle 的简短报告。
