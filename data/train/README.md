# 训练数据

[manifest.json](manifest.json) 中的 60 块板按原项目家族归组，同一 `family` 的板应一起进入训练或验证。每条记录中的路径都相对于本目录。上游公开的是已完成布线的布局，具体由人工还是自动布线器完成未作标注。

| 文件 | 内容 |
|---|---|
| `<board_id>/upstream/` | 上游原始 KiCad 板、项目规则、许可证及署名说明，按下载字节保存 |
| `<board_id>/geometry.json` | 以毫米为单位的提取结果。`condition` 含板框、层、网表、焊盘和禁布区，`labels` 含实际线段、圆弧、过孔和覆铜轮廓。划定训练目标后，应从输入中去掉相应网络的标签 |
| `<board_id>/source.json` | 原项目、固定提交、原文件链接、SHA-256 和逐板许可 |
| `<board_id>/candidates/*.npz` | 部分板上的预计算布线候选。用 `numpy.load(path, allow_pickle=False)` 打开 |

候选文件内的 `meta` 是 JSON 字符串，给出板名、分支、网格及设计规则。`groups[i]` 标出第 i 个候选所属分支，`metric[i]` 依次为铜长（mm）、同层转角数、过孔数和顶层长度占比，`conflict[i,j]` 表示两候选存在跨网铜间距冲突。候选 i 的扁平节点序列为 `path_nodes[path_index[i]:path_index[i+1]]`，按 `meta.shape` 解码为层、行、列。首批选择器实验扫描了最初的 107 份候选文件，其中 20 块板的 73 份文件产生了有监督的双网比较样本。

## 可以从哪些板入手

| 双层板 | 学习场景 | 实际走线 |
|---|---|---|
| [Mitayi-Pico-D1](CIRCUITSTATE__Mitayi-Pico-D1__Mitayi-Pico-D1/upstream/board.kicad_pcb) | RP2040 核心板的引脚扇出 | 583 段直线、111 个过孔 |
| [Battery-Powered-STM32-Board-With-USB](mohamedboubaker__Battery-Powered-STM32-Board-With-USB__ORBIT/upstream/board.kicad_pcb) | STM32、USB 串口和电池充电电路 | 299 段直线、49 个过孔 |
| [RetroWiFiModem](mecparts__RetroWiFiModem__RetroWiFiModem/upstream/board.kicad_pcb) | 串口与 Wi-Fi 通信 | 318 段直线、63 个过孔 |
| [esphome-powermon](michd__esphome-powermon__esphome-powermon/upstream/board.kicad_pcb) | 多路电能监测与信号采集 | 225 段直线、15 个过孔 |

## 筛选与来源

本轮筛查了 122 块候选板。使用 KiCad 10.0.6 和原项目规则重新填铜，检查 DRC、未连接项和每条多焊盘网络的物理连通性。34 块通过这些检查并满足布线规模要求，再结合上游对完成度、已知问题和素材来源的说明，收录 30 块。新增板均为零 error、零未连接，其中 29 块仍有 warning。旧批次的 DRC 结果另行保留，两批均可按警告、错误和未连接数筛选。[逐板质量记录](quality.json)

按原件哈希和板框、焊盘位置、网络分组的几何签名去除重复。几何签名允许平移、旋转及镜像。还移除层数差异，与公开测试模组核对签名。请按 `family` 划分训练与验证，BrickPico 和 FanPico 共用一个板族。

样本通过 [pcb-corpus 固定目录](https://github.com/punkfab/pcb-corpus/tree/1e999b4eefd5fdfcc90dc376d2882390245a8e0d) 和硬件项目上游仓库发现。每块板的 `source.json` 指向具体提交、原作者和适用的硬件设计文件许可，`upstream/` 保存对应许可和署名。其中的第三方资料按其各自声明使用。针对每块板整理的几何和候选数据按该板许可提供。
