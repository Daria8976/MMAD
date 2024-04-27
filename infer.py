import os
import subprocess
import time

# 定义路径
vision_prompt_path = "Example/prompt/vision.txt"
audio_prompt_path = "Example/prompt/audio.txt"


def execute_command(command):
    subprocess.run(command, shell=True)
    time.sleep(60)  

# Check if txt has content
def check_file_has_content(path):
    return os.path.exists(path) and os.path.getsize(path) > 0


def execute_steps():
    print("Executing steps...")
    os.chdir("VideoCaption")
    execute_command("pip install -e .")
    os.chdir("..")

    execute_command("python visioncaption.py")

    while not check_file_has_content(vision_prompt_path):
        print("Running python visioncaption.py...")
        execute_command("python visioncaption.py")

    execute_command("pip install transformers==4.28.1")
    execute_command("python AudioEnhancing/audiocaption.py")

    while not check_file_has_content(vision_prompt_path):
        print("Running python visioncaption.py...")
        execute_command("python AudioEnhancing/audiocaption.py")
    
    execute_command("python llama.py")

# 执行步骤
execute_steps()
