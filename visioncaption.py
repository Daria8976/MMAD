from VideoCaption.videocaption import videocaption
from ActorTracking import ActorTrackingAwareStoryLinking

def ADGenerate(video_path, vision_prompt_path):
    # 打开文件，将其内容清空，然后保存
    with open(vision_prompt_path, "w") as file:
        file.truncate(0)
    vc = videocaption(video_path)
    previous=""
    actor=ActorTrackingAwareStoryLinking(video_path)
    # 将情感和事件信息按照指定格式写入文本文件
    with open(vision_prompt_path, "w") as file:
        file.write(f"videocaption: {vc}\n")
        file.write(f"previous:{previous}\n")
        file.write(f"actor: {actor}\n")

if __name__ == '__main__':
    ADGenerate(video_path='Example/Video/demo.mp4',vision_prompt_path="/home/gpu15/projx/YeXiaojun/MMAD/Example/prompt/vision.txt")