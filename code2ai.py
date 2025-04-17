import os
import fnmatch
from pathlib import Path

def merge_code_files(root_dir, output_file, exclude_dirs=None, exclude_exts=None):
    """
    递归合并代码文件并生成汇总文档
    :param root_dir: 要扫描的根目录
    :param output_file: 输出文件名
    :param exclude_dirs: 要排除的目录列表（支持通配符）
    :param exclude_exts: 要排除的文件后缀列表（支持通配符）
    """
    exclude_dirs = exclude_dirs or []
    exclude_exts = exclude_exts or []
    
    with open(output_file, 'w', encoding='utf-8') as out_file:
        # 遍历目录树[1,5](@ref)
        for root, dirs, files in os.walk(root_dir):
            # 目录排除处理[5,8](@ref)
            dirs[:] = [d for d in dirs if not any(
                fnmatch.fnmatch(d, pattern) for pattern in exclude_dirs)]
            
            # 处理当前目录下的文件
            for filename in files:
                filepath = os.path.join(root, filename)
                
                # 文件后缀排除[3,8](@ref)
                if any(fnmatch.fnmatch(filename, pattern) for pattern in exclude_exts):
                    continue
                
                # 获取相对路径[5,6](@ref)
                rel_path = os.path.relpath(filepath, start=root_dir)
                
                try:
                    # 写入文件头[3,4](@ref)
                    header = f"\n{'='*40}\nFile: {rel_path}\n{'='*40}\n\n"
                    out_file.write(header)
                    
                    # 读取文件内容[6,8](@ref)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        out_file.write(content + '\n')
                        
                except UnicodeDecodeError:
                    print(f"跳过二进制文件: {rel_path}")
                except Exception as e:
                    print(f"处理文件 {rel_path} 出错: {str(e)}")

if __name__ == "__main__":
    config = {
        "root_dir": "./",      # 要扫描的代码目录
        "output_file": "giveAi.txt",  # 输出文件名
        "exclude_dirs": [".git", ".idea", "__pycache__", "data", "params", "test_image", "train_image"],  # 排除的目录
        "exclude_exts": [".DS_Store", "code2ai.py", "*.log", "*.bin", "*.pyc", ".gitignore"]  # 排除的文件类型
    }
    
    # 创建输出文件的父目录[5](@ref)
    Path(config['output_file']).parent.mkdir(parents=True, exist_ok=True)
    
    merge_code_files(
        root_dir=config['root_dir'],
        output_file=config['output_file'],
        exclude_dirs=config['exclude_dirs'],
        exclude_exts=config['exclude_exts']
    )