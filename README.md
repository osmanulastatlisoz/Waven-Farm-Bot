
# Waven Farm Bot  
**A Python automation tool designed to optimize repetitive tasks in Waven.**  

## Key Features  
- **Automated Gameplay:** Seamlessly integrates with AutoHotkey and OpenCV for precise, efficient game interaction.  
- **Resource Monitoring:** Tracks CPU, GPU, and RAM usage, restarting tasks when limits are exceeded.  
- **Error Management:** Logs system and task activities in real-time for effective debugging.  
- **Self-Healing Mechanism:** Automatically restarts processes for uninterrupted performance.  

## Installation and Usage  

### Requirements  
- Python 3.9 or later  
- AutoHotkey installed on your system  

### Setup  
1. Clone the repository to your local machine.  
   ```bash
   git clone https://github.com/username/Waven-Farm-Bot.git
   cd Waven-Farm-Bot
   ```  
2. Install required Python packages:  
   ```bash
   pip install -r requirements.txt
   ```  

### Run the Bot  
Start the bot using the memory watcher:  
```bash
python memory_watcher.py
```  

## Technical Implementation  

### Memory Watcher  
The `memory_watcher.py` script monitors system usage and manages processes to ensure optimal performance.  
**Key Code Snippet:**  
```python
if total_memory > MAX_RAM_USAGE_MB or gpu_usage > MAX_GPU_USAGE_PERCENT or cpu_usage > MAX_CPU_USAGE_PERCENT:
    kill_all_python_processes()
    start_watcher()
```  

### Watcher Script  
Executes in-game tasks using OpenCV for image recognition and task automation.  

**Function Example:**  
```python
def search_and_click(image_path):
    template = cv2.imread(image_path, 0)
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    if max_val > threshold:
        pyautogui.click(center_x, center_y)
```  

### AutoHotkey Integration  
Handles key press and mouse actions for real-time gameplay automation.  

**Example Macro:**  
```ahk
F8::Click  
F7::
    Click Down
    KeyWait, F7
    Click Up
return
```  

## Contributions and Licensing  
This project is open to contributions. If you have suggestions or would like to collaborate, feel free to open an issue or submit a pull request.  

**License:** MIT License  
