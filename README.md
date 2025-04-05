# Download Manager

This project is a Python-based Download Organizer that automatically monitors a specified folder (e.g., the Downloads folder) and organizes newly added files into categorized subfolders based on their file types. It uses the `watchdog` library to monitor file system events and the `pystray` library to provide a system tray icon for easy control.

## Features

- **Automatic File Organization**: Moves files into categorized subfolders (e.g., Images, Videos, Audio, etc.) based on their extensions.
- **Customizable Categories**: Easily add or modify file type categories in the `extension_mapping` dictionary.
- **Rotating Logs**: Logs all file movements and errors to a rotating log file (`created_file_log.txt`).
- **System Tray Icon**: Provides a system tray icon with a "Quit" option to stop the organizer.
- **Threaded Execution**: Runs the file monitoring process in a separate thread to keep the application responsive.

## Requirements

- **Python**: Version 3.6 or higher
- **Libraries**:
    - `watchdog`
    - `pystray`
    - `Pillow`

Install the required libraries using:

```bash
pip install watchdog pystray Pillow
```

## How It Works

### Folder Monitoring

- The script monitors the folder specified in the `DOWNLOAD_FOLDER_PATH` variable (default: Downloads).
- When a new file is created, it determines the file type based on its extension.

### File Categorization

- The `extension_mapping` dictionary defines the file type categories (e.g., Images, Videos, Audio, etc.).
- Files are moved to corresponding subfolders (e.g., Images, Videos, etc.) under the monitored folder.

### Logging

- All file movements and errors are logged to `created_file_log.txt` with a maximum size of 5 MB and up to 3 backup files.

### System Tray Icon

- A system tray icon is created using `pystray`.
- The icon provides a "Quit" option to stop the organizer.

## File Structure

- `main.py`: The main script that handles folder monitoring, file organization, and system tray functionality.
- `created_file_log.txt`: Log file for recording file movements and errors (auto-generated).

## Usage

1. Clone or download the repository.
2. Update the `DOWNLOAD_FOLDER_PATH` variable in `main.py` to the folder you want to monitor.
3. Run the script:

     ```bash
     python main.py
     ```

     - The script will start monitoring the folder and organizing files automatically.
     - Use the system tray icon to quit the application when needed.

## Customization

### Add/Modify File Categories

Update the `extension_mapping` dictionary to include new file types or modify existing ones.

**Example**:

```python
extension_mapping = {
        "Images": [".jpg", ".png", ".gif"],
        "Videos": [".mp4", ".avi"],
        "Audio": [".mp3", ".wav"]
}
```

### Change Log File Settings

Modify the `RotatingFileHandler` configuration to adjust log file size or backup count.

**Example**:

```python
handler = RotatingFileHandler("created_file_log.txt", maxBytes=5 * 1024 * 1024, backupCount=3)
```

## Example

If a new file `example.jpg` is added to the monitored folder, the script will:

1. Detect the file creation event.
2. Identify the file type as `Image`.
3. Move the file to the `Images` subfolder.
4. Log the action in `created_file_log.txt`.

## License

This project is open-source and available under the [MIT License](LICENSE).