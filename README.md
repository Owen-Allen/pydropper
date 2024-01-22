# Py-Dropper

Py-Dropper is a Python script that displays the name of the color beneath your cursor. This tool may be useful for people with vision impairements, or for designers and developers who want a faster way to get hex color values.

## Setup

To set up Py-Dropper, follow these steps:

1. **Create a Virtual Environment:**
   ```bash
   python3.10 -m venv myenv
   ```

2. **Activate Virtual Environment**
    ```bash
    source myenv/bin/activate
    ```

3. **Install Required Packages:**
    ```
    pip install -r requirements.txt
    ```

Now you should be able to run the program by running the command
    ```
    python3 pydropper.py
    ```

If you want to run the script as an App on mac, you can use automator.app


### Setup Automator

Open automator app, select Application > Utilities > Run Shell Script. In the script body, include the following    
```
source /<path-to-your-repo>/pydropper/myenv/bin/activate
python3 /<path-to-your-repo>/pydropper/pydropper.py
```

Where \<path-to-your-repo\> is the location that you installed the pydropper files.
