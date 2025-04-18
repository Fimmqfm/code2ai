import os
import fnmatch
from pathlib import Path

def generate_directory_tree(root_dir, exclude_dirs=None, exclude_exts=None):
    """
    生成带ASCII连接线的目录树结构
    """
    exclude_dirs = exclude_dirs or []
    exclude_exts = exclude_exts or []

    root_name = os.path.basename(os.path.abspath(root_dir))
    tree = [f"{root_name}/"]
    
    # 使用递归遍历构建树形结构
    def walk_dir(current_dir, prefix='', is_last=False):
        entries = []
        
        # 获取目录内容并排序
        try:
            dir_content = sorted(os.listdir(current_dir))
        except PermissionError:
            return
        
        # 分离目录和文件
        dirs = [d for d in dir_content 
                if os.path.isdir(os.path.join(current_dir, d)) 
                and not any(fnmatch.fnmatch(d, p) for p in exclude_dirs)]
        
        files = [f for f in dir_content 
                 if os.path.isfile(os.path.join(current_dir, f)) 
                 and not any(fnmatch.fnmatch(f, p) for p in exclude_exts)]
        
        # 合并目录和文件，目录优先
        entries = [(d, True) for d in dirs] + [(f, False) for f in files]
        
        for index, (name, is_dir) in enumerate(entries):
            # 判断是否是最后一项
            last_item = index == len(entries) - 1
            connector = "└── " if last_item else "├── "
            
            # 添加当前条目
            tree.append(f"{prefix}{connector}{name}{'/' if is_dir else ''}")
            
            # 如果是目录则递归处理
            if is_dir:
                extension = "    " if last_item else "│   "
                walk_dir(
                    os.path.join(current_dir, name),
                    prefix=prefix + extension,
                    is_last=last_item
                )
    
    walk_dir(root_dir)
    return "\n".join(tree)

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
    
    # 生成目录树
    directory_tree = generate_directory_tree(root_dir, exclude_dirs, exclude_exts)
    
    with open(output_file, "w", encoding="utf-8") as out_file:
        # 写入目录树
        out_file.write("Directory Tree:\n")
        out_file.write(directory_tree)
        out_file.write("\n\n" + "=" * 40 + "\n\n")
        
        # 遍历目录树
        for root, dirs, files in os.walk(root_dir):
            # 目录排除处理
            dirs[:] = [d for d in dirs if not any(
                fnmatch.fnmatch(d, pattern) for pattern in exclude_dirs)]
            
            # 处理当前目录下的文件
            for filename in files:
                filepath = os.path.join(root, filename)
                
                # 文件后缀排除
                if any(fnmatch.fnmatch(filename, pattern) for pattern in exclude_exts):
                    continue
                
                # 获取相对路径
                rel_path = os.path.relpath(filepath, start=root_dir)
                
                try:
                    # 写入文件头
                    header = f"\n{'='*40}\nFile: {rel_path}\n{'='*40}\n\n"
                    out_file.write(header)
                    
                    # 读取文件内容
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        out_file.write(content + "\n")
                        
                except UnicodeDecodeError:
                    print(f"跳过二进制文件: {rel_path}")
                except Exception as e:
                    print(f"处理文件 {rel_path} 出错: {str(e)}")

if __name__ == "__main__":
    config = {
        "root_dir": "./",
        "output_file": "giveAi.txt",
        "exclude_dirs": [".git", ".idea", "__pycache__"],
        "exclude_exts": [".DS_Store", "code2ai.py", "*.log", "*.bin", "*.pyc", ".gitignore"]
    }
    
    # 创建输出文件的父目录
    Path(config["output_file"]).parent.mkdir(parents=True, exist_ok=True)
    
    merge_code_files(
        root_dir=config["root_dir"],
        output_file=config["output_file"],
        exclude_dirs=config["exclude_dirs"],
        exclude_exts=config["exclude_exts"]
    )