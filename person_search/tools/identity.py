import logging
import os.path as osp
from glob import glob

import coloredlogs
import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
import math

# 保证下面的 import 能正常使用
# import _init_paths  # noqa: F401
import person_search.tools._init_paths

from models.network import Network
from utils.config import cfg_from_file


def visualize_result(img_path, detections, similarities):
    """
    可视化检测结果，将与 query 的相似度标注在检测框上，并将结果保存为与原图相同位置的文件。
    """
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.imshow(plt.imread(img_path))
    plt.axis("off")
    for detection, sim in zip(detections, similarities):
        x1, y1, x2, y2, _ = detection
        # 将张量从 GPU 移动到 CPU 并转换为 NumPy 数组
        x1 = x1.cpu().numpy()
        y1 = y1.cpu().numpy()
        x2 = x2.cpu().numpy()
        y2 = y2.cpu().numpy()
        ax.add_patch(
            plt.Rectangle(
                (x1, y1), x2 - x1, y2 - y1, fill=False, edgecolor="#4CAF50", linewidth=3.5
            )
        )
        ax.add_patch(
            plt.Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, edgecolor="white", linewidth=1)
        )
        ax.text(
            x1 + 5,
            y1 - 18,
            "{:.2f}".format(sim),
            bbox=dict(facecolor="#4CAF50", linewidth=0),
            fontsize=20,
            color="white",
        )
    plt.tight_layout()

    # 将结果文件名替换 "gallery" -> "result"（可根据需要自行修改命名规则）
    fig.savefig(img_path.replace("gallery", "result"))
    plt.show()
    plt.close(fig)


def identity(query_img_path, gallery_img_folder):
    """
    输入:
      - query_img_path: str, query 图像的全路径
      - gallery_img_folder: str, gallery 图像所在的文件夹路径

    输出:
      - global_max_similarity: float, 所有 gallery 图片中最大的相似度
    """

    # ========== 配置日志输出 ==========
    coloredlogs.install(level="INFO", fmt="%(asctime)s %(filename)s %(levelname)s %(message)s")

    logging.info("Start identity function.")
    logging.info(f"Query image path: {query_img_path}")
    logging.info(f"Gallery folder path: {gallery_img_folder}")

    # ========== 如果有需要的 config 文件（可选）==========
    # cfg_from_file("path/to/your_config.yml")  # 如不需要可注释

    # ========== 初始化网络并加载 checkpoint ==========
    net = Network()
    checkpoint_path = osp.abspath("/data15/chenjh2309/Desktop/MMAD/checkpoint/checkpoint_step_50000.pth")
    checkpoint = torch.load(checkpoint_path)
    net.load_state_dict(checkpoint["model"])
    # logging.info("Loaded checkpoint from: %s" % checkpoint_path)

    # 切换网络到评估模式
    net.eval()

    # 指定 GPU 设备
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    net.to(device)

    # ========== 提取 query 特征 ==========
    query_img = cv2.imread(query_img_path)
    # 这里的 [0, 0, w, h] 仅作示例，具体需求看你如何获得 query 的 bbox
    h, w, _ = query_img.shape
    query_roi = np.array([0, 0, w, h])  # [x1, y1, x2, y2]
    query_feat = net.inference(query_img, query_roi).view(-1, 1)

    # ========== 读取所有 gallery 图片 ==========
    gallery_imgs = sorted(glob(osp.join(gallery_img_folder, "gallery*.jpg")))

    # 用 -inf 初始化，表示“目前还没有找到任何相似度”
    global_max_similarity = -math.inf

    # ========== 遍历每张 gallery 图 ==========
    for gallery_img in gallery_imgs:
        # logging.info("Detecting %s" % gallery_img)
        detections, features = net.inference(cv2.imread(gallery_img))

        # Compute pairwise cosine similarities,
        # which equals to inner-products, as features are already L2-normed
        similarities = features.mm(query_feat).view(-1)

        # 找出该图最大相似度
        current_max = similarities.max().item()
        if current_max > global_max_similarity:
            global_max_similarity = current_max

        # 可视化结果（可根据需求决定是否保留或注释掉）
        visualize_result(gallery_img, detections, similarities)

    # logging.info(f"Global max similarity: {global_max_similarity}")
    return global_max_similarity


# 如果需要在本脚本内测试，也可加如下内容：
if __name__ == "__main__":
    # 测试时示例
    identity_similarity = identity(
        query_img_path="/data15/chenjh2309/Desktop/MMAD/Example/ActorCandidate/Don Lockwood.jpg",
        gallery_img_folder="/data15/chenjh2309/Desktop/MMAD/Example/Keyframes"
    )
    print("Test run, identity_similarity =", identity_similarity)
