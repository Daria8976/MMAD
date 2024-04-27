from wrapper import PengiWrapper as audiocaption
import os
from moviepy.editor import VideoFileClip
def from_mp4_get_wav(video_path, audio_path):

    video_clip = VideoFileClip(video_path)
    
    audio_clip = video_clip.audio
    
    audio_clip.write_audiofile(audio_path, codec='pcm_s16le')  # pcm_s16le 是WAV的默认编码
   
    audio_clip.close()
    video_clip.close()
    
    return audio_path

def audioenhancing(video_path, audio_prompt_path):
    ac = audiocaption(config="base") #base or base_no_text_enc
    # 提取视频目录路径
    video_dir = os.path.dirname(video_path)
    # 去掉 "Video" 文件夹，并添加 "Audio" 文件夹
    audio_dir = os.path.join(os.path.dirname(video_dir), "Audio")
    # 提取文件名（不包括扩展名）
    file_name = os.path.splitext(os.path.basename(video_path))[0]
    # 构建音频路径
    audio_path = os.path.join(audio_dir, file_name + ".wav")
    from_mp4_get_wav(video_path=video_path, audio_path=audio_path)
    audio_file_paths = [audio_path]
    text_prompts = ["this emotion is"]
    add_texts = [""]

    generated_response = ac.generate(
                                        audio_paths=audio_file_paths,
                                        text_prompts=text_prompts, 
                                        add_texts=add_texts, 
                                        max_len=30, 
                                        beam_size=1, 
                                        temperature=1.0, 
                                        stop_token=' <|endoftext|>',
                                        )

    generated_summary = ac.describe(
                                        audio_paths=audio_file_paths,
                                        max_len=30, 
                                        beam_size=1,  
                                        temperature=1.0,  
                                        stop_token=' <|endoftext|>',
                                        )

    # audio_prefix, audio_embeddings = ac.get_audio_embeddings(audio_paths=audio_file_paths)

    # text_prefix, text_embeddings = ac.get_prompt_embeddings(prompts=text_prompts)
    emotion = generated_response[0][0][0]
    # print("emotion:",emotion)
    audio_caption = generated_summary[0]

    # 使用字符串分割方法提取事件信息
    events_split = audio_caption.split("this audio contains sound events: ")
    events = events_split[1].strip(". ") if len(events_split) > 1 else ""
    # 将情感和事件信息按照指定格式写入文本文件
    with open(audio_prompt_path, "w") as file:
        file.truncate(0)
    with open(audio_prompt_path, "w") as file:
        file.write(f"emotion: {emotion}\n")
        file.write(f"events: {events}\n")



if __name__ == "__main__":
    audioenhancing(video_path="/home/gpu15/projx/YeXiaojun/MMAD/Example/Video/demo.mp4",audio_prompt_path="/home/gpu15/projx/YeXiaojun/MMAD/Example/prompt/audio.txt")
