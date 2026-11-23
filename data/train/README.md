# 训练数据

[manifest.json](manifest.json) 中的 30 块板按原项目家族归组，同一 `family` 的板应一起进入训练或验证。每条记录中的路径都相对于本目录。上游公开的是已完成布线的布局，具体由人工还是自动布线器完成未作标注。

| 文件 | 内容 |
|---|---|
| `<board_id>/upstream/` | 上游原始 KiCad 板、项目规则、许可证及署名说明，按下载字节保存 |
| `<board_id>/geometry.json` | 以毫米为单位的提取结果。`condition` 含板框、层、网表、焊盘和禁布区，`labels` 含实际线段、圆弧、过孔和覆铜轮廓。划定训练目标后，应从输入中去掉相应网络的标签 |
| `<board_id>/source.json` | 原项目、固定提交、原文件链接、SHA-256 和逐板许可 |
| `<board_id>/candidates/*.npz` | 部分板上的预计算布线候选。用 `numpy.load(path, allow_pickle=False)` 打开 |

候选文件内的 `meta` 是 JSON 字符串，给出板名、分支、网格及设计规则。`groups[i]` 标出第 i 个候选所属分支，`metric[i]` 依次为铜长（mm）、同层转角数、过孔数和顶层长度占比，`conflict[i,j]` 表示两候选存在跨网铜间距冲突。候选 i 的扁平节点序列为 `path_nodes[path_index[i]:path_index[i+1]]`，按 `meta.shape` 解码为层、行、列。已有选择器实验扫描了这 107 份文件，其中 20 块板的 73 份文件产生了有监督的双网比较样本。

板源依据 [pcb-corpus 目录](https://github.com/punkfab/pcb-corpus/tree/1e999b4eefd5fdfcc90dc376d2882390245a8e0d) 定位，原作者及设计源位置见各板的 `source.json`。上游板分别使用 CERN-OHL-P-2.0、CERN-OHL-W-2.0 或 CERN-OHL-S-2.0。相应板目录内的派生几何与生成候选按该板相同许可提供。几何提取与候选生成由本挑战项目整理，原始铜线文件保留上游版本。
