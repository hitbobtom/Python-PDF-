import pandas as pd
import os

up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ""))
pathPrefix = up_dir_path

if __name__ == "__main__":  # 当程序执行时
    # 设置输出Excel文件名
    output_file = 'merged_excel.xlsx'

    # 创建一个空的DataFrame，用于存储合并后的数据
    all_data = pd.DataFrame()

    # 设置包含Excel文件的目录
    excel_dir = pathPrefix + "\\Excel"

    # 获取目录下所有Excel文件
    excel_files = [f for f in os.listdir(excel_dir) if f.endswith('.xlsx')]
    #排序
    # excel_files.sort(key=lambda x: x[0])  # 文件夹名称

    for file in excel_files:
        # 读取Excel文件
        df = pd.read_excel(os.path.join(excel_dir, file))
        # 将数据追加到all_data中
        all_data = all_data._append(df, ignore_index=True)

    # 将合并后的数据写入到新的Excel文件
    all_data.to_excel(output_file, index=False)