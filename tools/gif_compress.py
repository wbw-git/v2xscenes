import os
import imageio
from PIL import Image

def compress_gif(input_path, output_path, target_size_mb=20, max_resolution_factor=0.7, max_fps=15):
    try:
        # 使用 imageio.get_reader 逐帧读取 GIF 文件
        with imageio.get_reader(input_path) as reader:
            frames = []
            
            # 获取每帧显示的持续时间，如果没有获取到，则使用默认值
            try:
                duration = reader.get_meta_data()['duration']
            except KeyError:
                duration = 0.1  # 默认每帧显示 0.1 秒
            
            # 获取原始帧率（FPS），如果未获取到，则设定为 15 FPS
            fps = reader.get_meta_data().get('fps', 15)

            # 降低帧率
            if fps > max_fps:
                fps = max_fps
            
            # 逐帧处理
            for frame in reader:
                pil_frame = Image.fromarray(frame)
                
                # 如果图像是调色板图像，转换为 RGB 模式
                if pil_frame.mode == 'P' or pil_frame.mode == 'L':  # P: 使用调色板，L: 灰度图
                    pil_frame = pil_frame.convert('RGB')  # 转换为 RGB 模式，不再访问调色板

                # 调整图像分辨率（降低清晰度）
                new_width = int(pil_frame.width * max_resolution_factor)
                new_height = int(pil_frame.height * max_resolution_factor)
                pil_frame = pil_frame.resize((new_width, new_height), Image.Resampling.LANCZOS)  # 使用 LANCZOS 替代 ANTIALIAS
                frames.append(pil_frame)

        # 保存压缩后的 GIF 文件
        while True:
            imageio.mimsave(output_path, frames, duration=duration, loop=0, fps=fps)

            # 检查文件大小
            if os.path.getsize(output_path) <= target_size_mb * 1024 * 1024:
                break

            # 如果文件大小还大于目标大小，进一步减小尺寸
            max_resolution_factor *= 0.9
            if max_resolution_factor < 0.2:
                break  # 防止过度压缩

    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return  # 跳过无法处理的文件

def compress_gifs_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".gif"):
            input_path = os.path.join(directory_path, filename)
            output_path = input_path  # 覆盖原文件
            compress_gif(input_path, output_path)
            print(f"Compressed: {filename}")

if __name__ == "__main__":
    folder_path = r"E:\博士相关工作\迁移学习调研\17-STAR_dataset\v2xscenes.github.io-main\static\images"  # 替换为实际文件夹路径
    compress_gifs_in_directory(folder_path)
