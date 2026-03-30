
# 挑战任务要求说明

## 考核基础信息

- 分值占比：10%（课程总分100+10，为可选加分项）
- 格式要求：至少2页，需使用课程提供的ACM格式LaTeX模板
- 提交截止时间：4月15日
- 提交要求：获得挑战结果后，需在UM Moodle平台提交对应的简短报告

---

## 挑战任务主题：Cross-view Ground-to-Satellite Geo-localization

To Be Decided.

### 结果提交平台

提交网站：<https://codalab.lisn.upsaclay.fr/competitions/22073>

### 任务核心定位

本年度挑战任务聚焦**局部街景图像与对应卫星图像的匹配**（相关说明详见提案文档的图3）。通过聚焦局部视图，更精准地还原现实世界中因遮挡、传感器视角受限导致视野受限的场景，例如低空无人机导航、搜救任务、自主飞行等作业场景。

### 数据集说明

本次挑战使用**University-1652**数据集，该数据集提供2579张街景图像作为查询集、951张卫星图像作为底库集。为鼓励更广泛的参与和技术创新，主办方将通过官网开放University-1652训练集、经过名称匿名化处理的测试集，同时配套公开排行榜。

### 相关资料与数据获取渠道

1. 挑战详细规则：详见提案文档第5节，链接：<https://www.zdzheng.xyz/files/MM25_Workshop_Proposal_Drone.pdf>
2. 训练集获取：可通过提交申请下载，申请链接：<https://github.com/layumi/University1652-Baseline/blob/master/Request.md>，通常会在5分钟内回复下载链接
3. 测试查询集下载：详见挑战官方网站
4. 提交示例：基线提交样例链接：<https://github.com/spyflying/ACMMM2025Workshop-UAV/blob/main/answer.zip>

### 提交规范与格式要求

1. 压缩包要求：需将结果文件压缩为 `answer.zip` 格式提交，压缩包内必须包含名为 `answer.txt` 的文件，文件命名错误将导致评估失败。
2. 结果内容要求：
   - 每行需返回对应查询图像的**Top-10匹配卫星图像名称**，按Rank-1到Rank-10的顺序排列，名称间以空格分隔
   - 格式示例：若首个查询图像为 `VdthudbGjJ4aaNkl.jpeg`，则`answer.txt`中第一行的结果格式如下：

     ```plaintext
     ptHYAN3piG3YwOft I9bzP8jnLlz9zpMi c3vVTLCzTAVzuapU gkriPL4PNtcWoHgg iIL2ASdQ5vrFsJs0 TinwNxUGYAzz0kTO XilyyHqywhUBxHfT WLasj720MnF13zPI Qz4NypYGPhHdiAvn gO2hUfIHC8N4ZWKz
     ```

3. 结果顺序要求：必须严格按照查询名称列表的顺序返回结果，查询名称列表链接：<https://github.com/spyflying/ACMMM2025Workshop-UAV/blob/main/query_street_name.txt>，最终结果文件需包含2759行。

### 技术支持

如遇任何困难，可联系课程助教与授课老师。
