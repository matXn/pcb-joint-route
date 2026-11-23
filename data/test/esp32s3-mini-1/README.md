# ESP32-S3-MINI-1 · 37 条 GPIO 的外层布线

[routing-input.npz](routing-input.npz) 是可直接运行模型的公开测试输入。[case.json](case.json) 列出所有目标网络、焊盘、规则、坐标系及 SHA-256。先拿掉目标网络的原始铜线，再计算可走区域与可放孔位置。测试只有一块板，37 条网络要同时求解。

```python
import numpy as np

with np.load("routing-input.npz", allow_pickle=False) as data:
    print(data["net_names"].tolist())
    print(data["trace_allowed"].shape)  # 网络、层、行、列
    print(data["via_allowed"].shape)    # 网络、行、列
```

网格步长是 0.05 mm。第 0 层为顶层 F.Cu，第 1 层为底层 B.Cu。网格点的毫米坐标为 `origin_mm + step_mm * [列, 行]`，Y 轴向下。对规格中 `contact_index` 为 i 的焊盘，读取 `contact_nodes[contact_index[i]:contact_index[i+1]]`，以 `(2, 行数, 列数)` 为形状解开扁平索引，得到该焊盘可接入的网格点。

掩码描述固定障碍下单个网络可用的格点，已考虑焊盘、板边、天线禁布区和固定铜对过孔的限制。算法仍需检查相邻格点之间的线段、不同目标网之间的间距以及多个过孔之间的间距。最终连通性和间距用实际铜线复核。

## 重建 KiCad 测试工程

在本目录中使用能导入 `pcbnew` 的 KiCad 10 Python 运行以下命令。脚本从乐鑫下载 V1.1 参考包、校验 SHA-256、导入 PADS、恢复板框、移除目标走线和过孔，并重新填铜。也可传入 `--archive 已下载的文件.zip`，或用 `--kicad-cli` 指定 CLI 路径。公开包内直接提供网格数据，乐鑫原始 CAD 图签标为 Proprietary，完整工程在本地重建。[乐鑫官方设计文件](https://github.com/espressif/esp-hardware-design-guidelines/blob/master/docs/_static/esp32s3/esp32-s3-mini-1_reference_design.zip)

```text
python prepare_kicad.py --out blank
kicad-cli pcb drc --refill-zones --format json -o blank/drc.json blank/board.kicad_pcb
```

KiCad 10.0.6 下，未布目标线的测试输入有 57 项 error、59 项未连接。需要逐项比较新增错误时，在重建命令加入 `--reference-drc`，从同次导入生成原始参考板的 `reference-drc.json`。此报告只用于验收。跨次导入时 KiCad 可能重新分配网络编号及 UUID，按网络名、错误类型和几何位置比较。

使用相同版本与规则检查提交板，按网络焊盘所属的导电分量统计目标连通性，再分别报告全板 DRC 和未连接项。每条目标网都要连接该网的所有物理焊盘。验收时也要检查天线禁布区（原始 KiCad 工程未编码该实验约束），以及保留的电源和地网络是否失去原先连通的焊盘对。
