<h1 align="center"> University1652-Baseline </h1>
<h2 align="center"> Satellite, Drone, Ground </h2>

![Python 3.6+](https://img.shields.io/badge/python-3.6+-green.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Citations](https://img.shields.io/badge/Citations-300%2B-brightgreen)](https://scholar.google.com/scholar?cites=16355841926251595902)
[![Stars](https://img.shields.io/github/stars/layumi/University1652-Baseline)](https://github.com/layumi/University1652-Baseline/stargazers)

[![VideoDemo](https://github.com/layumi/University1652-Baseline/blob/master/docs/index_files/youtube1.png)](https://www.youtube.com/embed/dzxXPp8tVn4?vq=hd1080)

[[Paper]](https://arxiv.org/abs/2002.12186) 
[[Slide]](http://zdzheng.xyz/files/ACM-MM-Talk.pdf)
[[Explore Drone-view Data]](https://github.com/layumi/University1652-Baseline/blob/master/docs/index_files/sample_drone.jpg?raw=true)
[[Explore Satellite-view Data]](https://github.com/layumi/University1652-Baseline/blob/master/docs/index_files/sample_satellite.jpg?raw=true)
[[Explore Street-view Data]](https://github.com/layumi/University1652-Baseline/blob/master/docs/index_files/sample_street.jpg?raw=true)
[[Video Sample]](https://www.youtube.com/embed/dzxXPp8tVn4?vq=hd1080)
[[涓枃浠嬬粛]](https://zhuanlan.zhihu.com/p/110987552)
[[Building Name List]](https://github.com/layumi/University1652-Baseline/blob/master/docs/reference/new_name_list.txt)
[[Latitude and Longitude]](https://drive.google.com/file/d/1PL8fVky9KZg7XESsuS5NCsYRyYAwui3S/view?usp=sharing)
[[Flight Path]](https://drive.google.com/file/d/1EW5Esi72tPcfL3zmoHYpufKj_SXrY-xE/view?usp=sharing)

猸?**Found this useful? Give us a star!** Help us reach more researchers in drone-based geo-localization. 馃殌

![](https://github.com/layumi/University1652-Baseline/blob/master/docs/index_files/Data.jpg)

![](https://github.com/layumi/University1652-Baseline/blob/master/docs/index_files/Motivation.png)


### Download [University-1652] upon request (Usually I will reply you in 5 minutes). You may use the request [template](https://github.com/layumi/University1652-Baseline/blob/master/docs/reference/Request.md).

This repository contains the dataset link and the code for our paper [University-1652: A Multi-view Multi-source Benchmark for Drone-based Geo-localization](https://arxiv.org/abs/2002.12186), ACM Multimedia 2020. The offical paper link is at https://dl.acm.org/doi/10.1145/3394171.3413896. We collect 1652 buildings of 72 universities around the world. Thank you for your kindly attention.

**Task 1: Drone-view target localization.** (Drone -> Satellite) Given one drone-view image or video, the task aims to find the most similar satellite-view image to localize the target building in the satellite view. 

**Task 2: Drone navigation.** (Satellite -> Drone) Given one satellite-view image, the drone intends to find the most relevant place (drone-view images) that it has passed by. According to its flight history, the drone could be navigated back to the target place.

## Workshops & Challenges 

- **ACM MM UAVM 2025**: Join our 3rd workshop! [Details](https://www.zdzheng.xyz/ACMMM2025Workshop-UAV/).
  - **Challenge Workflow**:
    1. Train on University-1652 (Drone+Satellite+Street).
    2. Download name-masked test set from [OneDrive](https://www.zdzheng.xyz/ACMMM2025Workshop-UAV/).
    3. Extract features using your model.
    4. Modify `demo.py` or `evaluate_gpu.py` to save top-10 gallery image names (follow query order).
   
<details>
 <summary><b>
  2024 Workshop and Sepcial Session
</b></summary>
 
- **ACM MM UAVM Workshop 2024** We will hold the 2nd workshop on ACM MM 2024! Please see [https://www.zdzheng.xyz/ACMMM2024Workshop-UAV/](https://www.zdzheng.xyz/ACMMM2024Workshop-UAV/) for reference.

- **ACM ICMR Workshop 2024** We are holding a workshop at ACM ICMR 2024 on  Multimedia Object Re-ID. You are welcome to show your insights. See you at Phuket, Thailand!馃槂 The workshop link is https://www.zdzheng.xyz/MORE2024/ . Submission DDL is **15 April 2024**.

- **ACM WWW Workshop 2024** We are holding a workshop at ACM WWW 2025 on  Multimedia Object Re-ID. You are welcome to show your insights. See you at Sydney!馃槂 The workshop link is https://www.zdzheng.xyz/MORE2025/ . Submission DDL is **1 Jan 2025**.

</details>

<details>
 <summary><b>
  2023 Workshop and Sepcial Session
</b></summary>

- **IEEE ITSC Special Session 2023** 
We host a special session on IEEE Intelligent Transportation Systems Conference (ITSC), covering the object re-identification & point cloud topic. The paper ddl is by **May 15, 2023** and the paper notification is at June 30, 2023. Please select the session code ``w7r4a'' during submission. More details can be found at [Special Session Website](https://2023.ieee-itsc.org/wp-content/uploads/2023/03/IEEE-ITSC-2023-Special-Session-Proposal-Safe-Critical-Scenario-Understanding-in-Intelligent-Transportation-Systems-SCSU-ITS.pdf).  

- **Remote Sensing Special Issue 2023**
We raise a special issue on Remote Sensing (IF=5.3) from now to ~~**16 June 2023**~~ **16 Dec 2023**. You are welcomed to submit your manuscript at (https://www.mdpi.com/journal/remotesensing/special_issues/EMPK490239), but you need to keep open-source fee in mind.

- **ACM Multimedia Workshop 2023**
We are holding the workshop at ACM Multimedia 2023 on Aerial-view Imaging. [Call for papers](https://www.zdzheng.xyz/ACMMM2023Workshop/) [涓枃浠嬬粛](https://zhuanlan.zhihu.com/p/620180604)

</details>

## Table of contents
* [About Dataset](#about-dataset)
* [News](#news)
* [Code Features](#code-features)
* [Prerequisites](#prerequisites)
* [Getting Started](#getting-started)
    * [Installation](#installation)
    * [Dataset Preparation](#dataset--preparation)
    * [Train Evaluation ](#train--evaluation)
    * [Trained Model](#trained-model)
    * [University-16k](#university-16k)
* [Citation](#citation)

## About Dataset
The dataset split is as follows: 
| Split | #imgs | #buildings | #universities|
| --------   | -----  | ----| ----|
|Training | 50,218 | 701 | 33 |
| Query_drone | 37,855 | 701 |  39 |
| Query_satellite | 701 | 701 | 39|
| Query_ground | 2,579 | 701 | 39|
| Gallery_drone | 51,355 | 951 | 39|
| Gallery_satellite |  951 | 951 | 39|
| Gallery_ground | 2,921 | 793  | 39|

More detailed file structure:
```
鈹溾攢鈹€ University-1652/
鈹?  鈹溾攢鈹€ readme.txt
鈹?  鈹溾攢鈹€ train/
鈹?      鈹溾攢鈹€ drone/                   /* drone-view training images 
鈹?          鈹溾攢鈹€ 0001
|           鈹溾攢鈹€ 0002
|           ...
鈹?      鈹溾攢鈹€ street/                  /* street-view training images 
鈹?      鈹溾攢鈹€ satellite/               /* satellite-view training images       
鈹?      鈹溾攢鈹€ google/                  /* noisy street-view training images (collected from Google Image)
鈹?  鈹溾攢鈹€ test/
鈹?      鈹溾攢鈹€ query_drone/  
鈹?      鈹溾攢鈹€ gallery_drone/  
鈹?      鈹溾攢鈹€ query_street/  
鈹?      鈹溾攢鈹€ gallery_street/ 
鈹?      鈹溾攢鈹€ query_satellite/  
鈹?      鈹溾攢鈹€ gallery_satellite/ 
鈹?      鈹溾攢鈹€ 4K_drone/
```

We note that there are no overlaps between 33 univeristies of training set and 39 univeristies of test set.
**Download**: Request the dataset [here](https://github.com/layumi/University1652-Baseline/blob/master/docs/reference/Request.md) (response within 5 minutes).

## News

**2 May 2025** I replace the apex with the merged supports in Pytorch for `fp16` and `bf16`.

**26 Nov 2024** Drone to BEV? You may check our new paper "Video2BEV: Transforming Drone Videos to BEVs for Video-based Geo-localization" at https://arxiv.org/abs/2411.13610.

**2 Jul 2024** Text-guided Geo-localization is accepted by [ECCV 2024](https://arxiv.org/pdf/2311.12751). [Code](https://github.com/MultimodalGeo/GeoText-1652) is available.

**26 Jan 2023** 1652 Building Name List is at [Here](https://github.com/layumi/University1652-Baseline/blob/master/docs/reference/new_name_list.txt).

**10 Jul 2022** Rainy锛烴ight锛烣oggy锛?Snow锛?You may check our new paper "Multiple-environment Self-adaptive Network for Aerial-view Geo-localization" at https://github.com/wtyhub/MuseNet (accepted by Pattern Recognition'24)  

**1 Dec 2021** Fix the issue due to the latest torchvision, which do not allow the empty subfolder. Note that some buildings do not have google images.  

**3 March 2021** [GeM Pooling](https://cmp.felk.cvut.cz/~radenfil/publications/Radenovic-arXiv17a.pdf) is added. You may use it by `--pool gem`.

**21 January 2021** The GPU-Re-Ranking,  a GNN-based real-time post-processing code, is at [Here](third_party/gpu_re_ranking/).

**21 August 2020** The transfer learning code for Oxford and Paris is at [Here](https://github.com/layumi/cnnimageretrieval-pytorch/blob/master/cirtorch/examples/test_My1652model.py).

**27 July 2020** The meta data of 1652 buildings, such as latitude and longitude, are now available at [Google Driver](https://drive.google.com/file/d/1PL8fVky9KZg7XESsuS5NCsYRyYAwui3S/view?usp=sharing). (You could use Google Earth Pro to open the kml file or use vim to check the value).  
We also provide the spiral flight tour file at [Google Driver](https://drive.google.com/file/d/1EW5Esi72tPcfL3zmoHYpufKj_SXrY-xE/view?usp=sharing). (You could open the kml file via Google Earth Pro to enable the flight camera).  

**26 July 2020** The paper is accepted by ACM Multimedia 2020.

**12 July 2020** I made the baseline of triplet loss (with soft margin) on University-1652 public available at [Here](https://github.com/layumi/University1652-triplet-loss).

**12 March 2020** I add the [state-of-the-art](https://github.com/layumi/University1652-Baseline/tree/master/docs/research/state-of-the-art) page for geo-localization and [tutorial](https://github.com/layumi/University1652-Baseline/tree/master/docs/tutorial/baseline), which will be updated soon.

## Code Features
Now we have supported:
- Float16 and BFloat16 with native pytorch support (replace apex)
- Multiple Query Evaluation
- Re-Ranking
- Random Erasing
- ResNet/VGG-16
- Visualize Training Curves
- Visualize Ranking Result
- Linear Warm-up 

## Prerequisites

- Python 3.6+
- GPU Memory >= 8G
- Numpy > 1.12.1
- Pytorch 0.3+ 

## Getting started

## Quickstart (uv + challenge submission)

This workspace is reorganized as a Python package managed by `uv` (Python 3.11). The challenge submission workflow is:

```bash
uv sync
uv run cross-view-g2s layout

# 1) Verify masked challenge test data layout + names
uv run python scripts/check_challenge_data.py \
  --query-order docs/requirement/query_street_name.txt \
  --query-root data/raw/University-Release/test/query_street \
  --gallery-root data/raw/University-Release/test/gallery_satellite \
  --manifest-dir data/manifest \
  --strict

# 2) Extract features (query_street -> gallery_satellite)
uv run python scripts/test.py \
  --name <your_model_dir_name> \
  --test_dir data/raw/University-Release/test \
  --query_name query_street \
  --gallery_name gallery_satellite

# 3) Export submission files
uv run python scripts/export_challenge_submission.py \
  --mat outputs/pytorch_result.mat \
  --query-order docs/requirement/query_street_name.txt \
  --query-paths outputs/query_name.txt \
  --gallery-paths outputs/gallery_name.txt \
  --answer outputs/answer.txt \
  --archive outputs/answer.zip \
  --topk 10

# 4) Final validation
uv run cross-view-g2s validate-submission \
  --answer outputs/answer.txt \
  --archive outputs/answer.zip \
  --query-order docs/requirement/query_street_name.txt
```

Notes:

- The canonical query order file is `docs/requirement/query_street_name.txt` (2579 lines). Do not traverse queries by filesystem order.
- If `check_challenge_data.py` reports all queries missing while the local query count is 2579, you are likely using a non-masked/incorrect query set.
### Installation
- Install Pytorch from http://pytorch.org/
- Install required packages
```bash
uv sync
```
- [Optinal] Usually it comes with pytorch. Install Torchvision from the source (Please check the README. Or directly install by anaconda. It will be Okay.)
```bash
git clone https://github.com/pytorch/vision # Please check the version to match Pytorch.
cd vision
python setup.py install
```

## Dataset & Preparation
Download [University-1652] upon request. You may use the request [template](https://github.com/layumi/University1652-Baseline/blob/master/docs/reference/Request.md).

Or download [CVUSA](http://cs.uky.edu/~jacobs/datasets/cvusa/) / [CVACT](https://github.com/Liumouliu/OriCNN). 

For CVUSA, I follow the training/test split in (https://github.com/Liumouliu/OriCNN). 

## Train & Evaluation 
### Train & Evaluation University-1652
```
python train.py --name three_view_long_share_d0.75_256_s1_google  --extra --views 3  --droprate 0.75  --share  --stride 1 --h 256  --w 256 --fp16; 
python test.py --name three_view_long_share_d0.75_256_s1_google
```

Default setting: Drone -> Satellite
If you want to try other evaluation setting, you may change these lines at: https://github.com/layumi/University1652-Baseline/blob/master/test.py#L217-L225 

### Ablation Study only Satellite & Drone
```
python train_no_street.py --name two_view_long_no_street_share_d0.75_256_s1  --share --views 3  --droprate 0.75  --stride 1 --h 256  --w 256  --fp16; 
python test.py --name two_view_long_no_street_share_d0.75_256_s1
```
Set three views but set the weight of loss on street images to zero.

### Train & Evaluation CVUSA
```
python prepare_cvusa.py
python train_cvusa.py --name usa_vgg_noshare_warm5_lr2 --warm 5 --lr 0.02 --use_vgg16 --h 256 --w 256  --fp16 --batchsize 16;
python test_cvusa.py  --name usa_vgg_noshare_warm5_lr2 
```

### Show the retrieved Top-10 result 
```
python test.py --name three_view_long_share_d0.75_256_s1_google # after test
python demo.py --query_index 0 # which image you want to query in the query set 
```
It will save an image named `outputs/show.png` containing top-10 retrieval results. 

## Trained Model

You could download the trained model at [GoogleDrive](https://drive.google.com/open?id=1iES210erZWXptIttY5EBouqgcF5JOBYO) or [OneDrive](https://studentutsedu-my.sharepoint.com/:u:/g/personal/12639605_student_uts_edu_au/EW19pLps66RCuJcMAOtWg5kB6Ux_O-9YKjyg5hP24-yWVQ?e=BZXcdM). After download, please put model folders under `./model/`.

## 馃實 University-160k Test 鈥?Always Open!
**Test anytime** 鈥?our evaluation server **never ends**!  
University160k is a challenging cross-view geo-localization test set that simulates real-world large-scale scenarios.  
It extends University-1652 with **+167,486** satellite-view distractors.
[Join & submit 鈫抅(https://codalab.lisn.upsaclay.fr/competitions/12672)

## Citation
The following paper uses and reports the result of the baseline model. You may cite it in your paper.
```bibtex
@article{zheng2020university,
  title={University-1652: A Multi-view Multi-source Benchmark for Drone-based Geo-localization},
  author={Zheng, Zhedong and Wei, Yunchao and Yang, Yi},
  journal={ACM Multimedia},
  year={2020}
}
@inproceedings{zheng2023uavm,
  title={UAVM'23: 2023 Workshop on UAVs in Multimedia: Capturing the World from a New Perspective},
  author={Zheng, Zhedong and Shi, Yujiao and Wang, Tingyu and Liu, Jun and Fang, Jianwu and Wei, Yunchao and Chua, Tat-seng},
  booktitle={Proceedings of the 31st ACM International Conference on Multimedia},
  pages={9715--9717},
  year={2023}
}
```
Instance loss is defined in 
```bibtex
@article{zheng2017dual,
  title={Dual-Path Convolutional Image-Text Embeddings with Instance Loss},
  author={Zheng, Zhedong and Zheng, Liang and Garrett, Michael and Yang, Yi and Xu, Mingliang and Shen, Yi-Dong},
  journal={ACM Transactions on Multimedia Computing, Communications, and Applications (TOMM)},
  doi={10.1145/3383184},
  volume={16},
  number={2},
  pages={1--23},
  year={2020},
  publisher={ACM New York, NY, USA}
}
```
## Related Work
- Instance Loss [Code](https://github.com/layumi/Image-Text-Embedding)
- Person re-ID from Different Viewpoints [Code](https://github.com/layumi/Person_reID_baseline_pytorch)
- Lending Orientation to Neural Networks for Cross-view Geo-localization [Code](https://github.com/Liumouliu/OriCNN)
- Predicting Ground-Level Scene Layout from Aerial Imagery [Code](https://github.com/viibridges/crossnet)

