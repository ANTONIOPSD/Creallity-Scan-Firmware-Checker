# Creallity-Scan-Firmware-Checker

Creallity-Scan-Firmware-Checker is a Python 3.10+ tool that scans hardware PIDs for available firmware updates on Creality Scan devices (and other brands?) using the Orbbec OTA API. It's useful for developers, reverse engineers, and enthusiasts who want to explore or validate available firmware versions for different devices automatically.

---

## What It Does

- Connects to the Orbbec OTA API endpoint used by Creality.
- Automatically scans a range of hardware PIDs or a specific one.
- Retrieves and logs firmware version info if available.
- Saves all findings to a structured, ordered `.txt` file in real time.

---

## Features

- ✅ Compatible with Windows and Linux
- ⚙️ Fully configurable (PID range, single PID, manufacturer, concurrency)
- 🧵 Multi-threaded for fast parallel scanning
- 📝 Saves to `firmware_results.txt` immediately upon discovery
- 🔢 Output is sorted by PID and updated live

---

## Requirements

- Python 3.10 or higher
- Dependency:
  - `requests`

Install with:

    pip install requests

---

## Usage

Configure your scan mode by editing the top of the `Creallity_Scan_Firmware_Checker.py` script.

### Scan a range of PIDs

Set these values:

    SINGLE_PID = 0
    START_PID = 1600
    END_PID = 9999

Then run the script:

    python Creallity_Scan_Firmware_Checker.py

---

### Check a single PID

Set this:

    SINGLE_PID = 1692

Then run:

    python Creallity_Scan_Firmware_Checker.py

---

## Output

The script creates or updates a file named `firmware_results.txt` in real time. Each valid result is added and the file is rewritten, sorted by PID.

### Example output:

    PID: 1692
    Latest Firmware Version: 1.2.2
    Full Info: {
        'url': 'https://ob-ota.oss-cn-shenzhen.aliyuncs.com/online/20250325/07f6c2dc333143beb9763888b746baf7/MX6600_CRScan_Ferret_App%2BCfg_V1.2.2.bin',
        'version': '1.2.2',
        'md5sum': '8e78160a221551f68274f67f1ad31b8a',
        'size': 327680,
        'force_flag': False,
        'remark': 'MX6600_CRScan_Ferret_App+Cfg_V1.2.2.bin'
    }
    -------------------------------------------------------

---

## Disclaimer

This tool is for **educational and informational purposes only**.

It interacts with a public OTA endpoint used by Creality devices and performs only read-only, passive requests. Use responsibly.

---

## License

This project is licensed under the MIT License.
