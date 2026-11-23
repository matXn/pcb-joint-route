# ESPiezometer — Open Hardware ESP32-C3 Device for Piezometric Sensor Installation and Validation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17400783.svg)](https://doi.org/10.5281/zenodo.17400783)

<!-- Cover Image -->
![ESPiezometer Front View](5_Documentation/ESPiezometer_Assembled_Device_Front_View.png)

---

*An open hardware field tool to validate and calibrate piezometric RS485 sensors before permanent installation, reducing deployment errors and improving groundwater monitoring reliability.*

**Author:** Armando Blanco (2025)  
**Hardware License:** CERN-OHL-P v2 (mechanical files) / CERN-OHL-W v2 (PCB)  
**Firmware & App License:** GPLv3  
**Documentation License:** CC-BY-4.0  
**Status:** Open-source hardware submitted for OSHWA certification  
**Repository Structure Version:** 1.0.0

---

## Project Overview

ESPiezometer is a low-cost, open-source device designed to assist in the installation and validation of **RS485 piezometric groundwater sensors** during field monitoring campaigns.

Unlike conventional dataloggers, ESPiezometer enables **real-time field verification** before permanent installation—allowing hydrology technicians and researchers to detect communication issues, incorrect depth calibration, or installation errors directly on site.

### Key Features

- Based on **ESP32-C3** with RS485 Modbus RTU support
- Displays **raw and temperature-compensated water level** on a 0.96" OLED
- **BLE connectivity** for Android logging with **GPS-tagged CSV export**
- PCB-based design to eliminate manual wiring and increase robustness
- 3D-printed enclosure optimized for **field handling and maintainability**
- Designed for **OSHWA open hardware certification** and **HardwareX publication format**

---

## Repository Structure

ESPiezometer/
├── 1_Hardware_STL/ → 3D enclosure (.stl) + README + license notice
├── 2_PCB_Gerber_Files/ → KiCad source + Gerber outputs + documentation
├── 3_Firmware/ → ESP32-C3 Arduino firmware (.ino) + license + README
├── 4_Mobile_App/ → Android App (.apk and .aia source) + license + README
├── 5_Documentation/ → Build guide, operation manual, schematics, photos
├── 6_Validation_Data/ → CSV logs, field test report, DOI-linked media index
├── 7_Licenses/ → Full legal texts (CERN-OHL, GPLv3, CC-BY-4.0)
├── .gitignore → Ignore rules for repository cleanliness
├── LICENSE.txt → License declaration summary
└── README.md → Main repository navigation (this file)


---

## Quick Start

| Step | Action |
|------|-------|
| 1 | Clone repository or download ZIP |
| 2 | 3D print enclosure from `/1_Hardware_STL/` if enclosure is required |
| 3 | Manufacture PCB from `/2_PCB_Gerber_Files/` or edit KiCad source |
| 4 | Flash firmware (`/3_Firmware/ESPiezometer_firmware.ino`) using Arduino IDE |
| 5 | Follow assembly instructions in `/5_Documentation/Build_Instructions.pdf` |
| 6 | Install Android App from `/4_Mobile_App/ESPiezometer_APP.apk` |
| 7 | Connect RS485 sensor and start validation / field diagnostics |

---

## Navigation Index

| Section | Path |
|--------|------|
| **STL Enclosure Files** | `/1_Hardware_STL/` |
| **PCB Design & Gerbers** | `/2_PCB_Gerber_Files/` |
| **Firmware Source Code** | `/3_Firmware/` |
| **Android Mobile App** | `/4_Mobile_App/` |
| **Build & Operation Documentation** | `/5_Documentation/` |
| **Validation Data + DOI Media** | `/6_Validation_Data/` |
| **Licensing Information** | `/7_Licenses/` |

---

## OSHWA / Open Hardware Certification Readiness

This repository includes:
- ✔ Bill of Materials (BOM) with sourcing notes
- ✔ PCB project files (KiCad) — **not only Gerbers**
- ✔ STL files with metadata and print recommendations
- ✔ Firmware and App under **GPLv3**
- ✔ Media evidence and CSV data with **DOI on Zenodo**
- ✔ Build instructions, wiring documentation and field test report
- ✔ Complete license stack (**CERN-OHL-P**, **CERN-OHL-W**, **GPLv3**, **CC-BY-4.0**)

---

## Citation / Referencing

If you use this hardware in academic work, certification reports, or derivative designs, please cite it as follows:

> **Blanco, A. (2025). ESPiezometer: Open Hardware ESP32-C3 Device for Field Installation and Validation of RS485 Piezometric Sensors (Version v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.17400783**

### BibTeX Reference (for publications or HardwareX submission)

```bibtex
@misc{Blanco_ESPiezometer_2025,
  author       = {Armando Blanco},
  title        = {ESPiezometer: Open Hardware ESP32-C3 Device for Field Installation and Validation of RS485 Piezometric Sensors},
  year         = {2025},
  version      = {v1.0.0},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.17400783},
  url          = {https://doi.org/10.5281/zenodo.17400783}
}
```

For future versions, you may alternatively cite all revisions using the generic DOI: **10.5281/zenodo.17400782**

---

End of `README.md` — ESPiezometer Open Hardware Project


