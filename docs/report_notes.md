# Report Notes (Execution Log)

Date: 2026-03-24

## 1) Environment and command checks (P0)

Executed and verified:

- `uv run python scripts/train.py --help` ✅
- `uv run python scripts/test.py --help` ✅
- `uv run cross-view-g2s layout` ✅
- `uv run cross-view-g2s validate-submission --answer docs/requirement/answer.txt --query-order docs/requirement/query_street_name.txt` ✅
- `uv run cross-view-g2s validate-submission --answer outputs/answer.txt --archive outputs/answer.zip --query-order docs/requirement/query_street_name.txt` ✅

Fixes made during check:

- `scripts/train.py`: defer heavy imports until after argument parsing, so `--help` can run robustly.
- `scripts/test.py`: defer heavy imports until after argument parsing, so `--help` can run robustly.

## 2) Data interface unification (P1)

Added:

- `src/university1652_baseline/data_interface.py`
- `scripts/check_challenge_data.py`

Generated files:

- `data/manifest/query_manifest.tsv`
- `data/manifest/gallery_manifest.tsv`
- `data/manifest/data_check_report.json`

Command executed:

- `uv run python scripts/check_challenge_data.py --query-order docs/requirement/query_street_name.txt --query-root data/raw/University-Release/test/query_street --gallery-root data/raw/University-Release/test/gallery_satellite --manifest-dir data/manifest`

Result summary:

- `query_count = 2579`
- `gallery_count = 951`
- `missing_query_count = 2579` (expected for current local non-masked split)
- `duplicate_query_name_count = 0`
- `duplicate_gallery_id_count = 0`
- `empty_directory_count = 0`

## 3) Training/inference alignment for challenge (P2)

Updated `scripts/test.py`:

- Added `--query_name` (default: `query_street`)
- Added `--gallery_name` (default: `gallery_satellite`)
- Added split name validation before feature extraction
- Removed hard-coded query/gallery selection

This aligns test defaults with challenge direction: partial street-view -> satellite.

Checkpoint status:

- `model/` currently has no trained checkpoints (`model/.gitkeep` only).
- Final challenge submission checkpoint is **not yet available** in current workspace.

Recommended command template (after training):

- `uv run python scripts/test.py --name <checkpoint_dir_name> --test_dir <challenge_test_root> --query_name query_street --gallery_name gallery_satellite`

Optional rerank path:

- `third_party/gpu_re_ranking/` remains available as post-processing option.

## 4) Submission export pipeline closure (P3)

Added:

- `scripts/export_challenge_submission.py`

What it does:

- loads `query_f` / `gallery_f` from `.mat`
- enforces query order from `docs/requirement/query_street_name.txt`
- writes compliant `answer.txt` (10 ids per line)
- writes `answer.zip` with `answer.txt` at archive root
- calls built-in validator

End-to-end dry run (mock features) completed:

- generated `outputs/mock/pytorch_result.mat`
- generated `outputs/mock/query_name.txt` and `outputs/mock/gallery_name.txt`
- exported `outputs/mock/answer.txt`
- packaged `outputs/mock/answer.zip`
- validated with `cross-view-g2s validate-submission` ✅
- confirmed `line_count = 2579`, `topk per line = 10` ✅

## 5) Moodle report-ready points

- Task setting: partial street-view -> satellite retrieval.
- Canonical query order source: `docs/requirement/query_street_name.txt`.
- Submission constraints enforced by validator and export script.
- Current blocker: final trained checkpoint absent in `model/`.
- Reproducible command path prepared for: data check -> test -> export -> validate -> zip.

## 6) 2026-03-24 extra run: real training/inference smoke

To address the gap between pipeline setup and actual model run, an end-to-end smoke run was executed on the local dataset.

Environment fix:

- Reinstalled a matched CUDA 12.8 stack:
	- `torch==2.10.0+cu128`
	- `torchvision==0.25.0+cu128`
	- `torchaudio==2.10.0+cu128`

Code fixes:

- `scripts/train.py`
	- added `--num_epochs` and `--max_batches`
	- save `net_last.pth` at the end of training
	- fixed migration path copies (`scripts/train.py`, `src/university1652_baseline/model.py`)
- `scripts/test.py`
	- fixed evaluation script path
	- added `--run_eval` (default off) to avoid legacy numpy incompatibility in optional evaluator

Executed training smoke command:

- `uv run python scripts/train.py --name smoke_street_sat --data_dir data/raw/University-Release/train --views 3 --share --h 256 --w 256 --batchsize 8 --num_epochs 1 --max_batches 2`

Artifacts generated:

- `model/smoke_street_sat/net_last.pth`
- `model/smoke_street_sat/opts.yaml`

Executed inference command:

- `uv run python scripts/test.py --name smoke_street_sat --test_dir data/raw/University-Release/test --query_name query_street --gallery_name gallery_satellite --batchsize 256`

Inference artifacts generated:

- `outputs/pytorch_result.mat`
- `outputs/query_name.txt`
- `outputs/gallery_name.txt`

Important caveat:

- local `data/raw/University-Release/test/query_street` uses repeated file names like `1.jpg/2.jpg` under class folders, while challenge requires masked unique query names from `docs/requirement/query_street_name.txt`.
- therefore local test set cannot directly produce a challenge-valid `answer.txt` aligned to masked query order.
- for final challenge submission, please run inference on the official masked challenge test set and then export with `scripts/export_challenge_submission.py`.
