import os
import cv2
import shutil
from person_search.tools.identity import identity

def GetKeyframes(video_path, scenefolder_path):
    num_frames = 6  # 只保存前5个关键帧
    frame_interval = 24  # 每24帧保存一次

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 检查视频是否成功打开
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # 创建目录，如果不存在的话
    if not os.path.exists(scenefolder_path):
        os.makedirs(scenefolder_path)
    
    frame_count = 0
    saved_frame_count = 0  # 已保存的帧计数
    success, image = cap.read()
    while success:
        # 只在每24帧的时候保存一次，且总共只保存5个关键帧
        if frame_count % frame_interval == 0 and saved_frame_count < num_frames:
            file_name = f"gallery-{saved_frame_count + 1}.jpg"
            file_path = os.path.join(scenefolder_path, file_name)
            cv2.imwrite(file_path, image)
            # print(f"Saved {file_name}")
            saved_frame_count += 1  # 更新已保存的关键帧数量

        success, image = cap.read()
        frame_count += 1  # 总帧数计数

        # 如果已保存足够的关键帧，可以提前退出循环
        if saved_frame_count >= num_frames:
            break

    # 释放视频捕获对象
    cap.release()
    print("Finished extracting keyframes.")

def GetActor(candidate_path,scenefolder_path):
    actor_similarity = {}  # 创建一个空字典用来存储角色名和相似度的对应关系
    # 检查 candidate_path 是否是目录
    if os.path.isdir(candidate_path):
        # 获取目录中的所有文件
        files = os.listdir(candidate_path)
        # 打印每个文件的完整路径
        for file_name in files:
            full_path = os.path.join(candidate_path, file_name)
            # 图片文件名去掉扩展名就是角色名
            actor_name = os.path.splitext(file_name)[0]
            # 调用 identity 函数获取相似度
            identity_similarity=identity(query_img_path=full_path, gallery_img_folder=scenefolder_path)
            actor_similarity[actor_name] = identity_similarity
            actorname = max(actor_similarity, key=actor_similarity.get)      
    else:
        print(f"提供的路径 {candidate_path} 不是一个目录")
    # print(actor_similarity)
    return actorname

def ActorTrackingAwareStoryLinking(video_path):
    KFfolders="Example/Keyframes"
    ACfolders="Example/ActorCandidate"
    VideoPath=video_path
    # get Keyframes
    GetKeyframes(video_path=VideoPath,scenefolder_path=KFfolders)
    # from the keyframes identity characters
    actor=GetActor(candidate_path=ACfolders, scenefolder_path=KFfolders)
    return actor

if __name__ == "__main__":
    actor=ActorTrackingAwareStoryLinking(video_path="Example/Video/demo.mp4")
    print(actor)