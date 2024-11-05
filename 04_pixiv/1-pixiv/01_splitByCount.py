import os
import shutil

up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ""))
pathPrefix = up_dir_path

def readFile(path):
    list = []
    f4 = open(path, encoding='utf-8')
    # 利用循环全部读出
    while 1 > 0:
        line = f4.readline()
        if line == '':
            break
        line = line.strip().replace('\n', '')
        if line == '':
            break
        list.append(line)

    f4.close()
    return list

def split_images(source_folder, images_per_folder):
    # 确保目标文件夹存在
    os.makedirs(source_folder, exist_ok=True)

    # 获取源文件夹中的所有图片文件
    image_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

    # 计算需要创建的目标文件夹数量
    num_folders = len(image_files) // images_per_folder
    if len(image_files) % images_per_folder > 0:
        num_folders += 1

    # 将图片分配到目标文件夹中
    for i in range(num_folders):
        folder_name = f"folder_{i+1}"
        folder_path = os.path.join(source_folder, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # 计算当前目标文件夹应包含的图片范围
        start_index = i * images_per_folder
        end_index = (i + 1) * images_per_folder

        # 处理最后一个文件夹，如果图像数量不足images_per_folder
        if i == num_folders - 1 and len(image_files) % images_per_folder > 0:
            end_index = len(image_files)

        # 将图片复制到目标文件夹
        for j in range(start_index, end_index):
            image_file = image_files[j]
            source_file_path = os.path.join(source_folder, image_file)
            destination_file_path = os.path.join(folder_path, image_file)
            shutil.move(source_file_path, destination_file_path)

        print(f"Created folder {folder_name} and copied {end_index - start_index} images.")


if __name__ == "__main__":
    # 示例用法
    file_content = readFile(pathPrefix + "\\" + "resource.txt")
    source_path = file_content[0]
    images_per_folder = int(file_content[1])

    split_images(source_path, images_per_folder)
