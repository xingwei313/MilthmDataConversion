import os
import json


def get_desktop_path():
    appdata_file = "appdata.json"
    if os.path.exists(appdata_file):
        with open(appdata_file, 'r') as file:
            data = json.load(file)
            return data.get('desktop_path')
    else:
        desktop_path = input("请输入桌面路径（例如：C:\\Users\\用户名\\Desktop\\）：")
        data = {'desktop_path': desktop_path}
        with open(appdata_file, 'w') as file:
            json.dump(data, file)
        return desktop_path


def update_specific_arrays(target_data, source_data):
    if isinstance(target_data, dict):
        new_data = {}
        for key, value in target_data.items():
            if key in ["Agreements", "Offsets"]:
                new_data[key] = source_data.get(key, [])
            else:
                new_data[key] = value
        return new_data
    return target_data


def process_json_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    desktop_path = get_desktop_path()
    file_choice = input("请选择要读取的数据源文件（输入 'PC' 选择PC-AO Data.json，输入 'PE' 选择PE-AO Data.json）：")
    source_file_path = ""
    if file_choice.upper() == "PC":
        source_file_path = os.path.join(current_dir, "PC-AO Data.json")
    elif file_choice.upper() == "PE":
        source_file_path = os.path.join(current_dir, "PE-AO Data.json")
    else:
        print("无效的选择，请重新运行程序并正确选择数据源文件。")
        return

    target_file_path = os.path.join(desktop_path, "MilthmData.json")
    if os.path.exists(source_file_path):
        try:
            with open(source_file_path, 'r', encoding='utf-8') as source_file:
                source_data = json.load(source_file)
            if os.path.exists(target_file_path):
                try:
                    with open(target_file_path, 'r', encoding='utf-8') as target_file:
                        target_data = json.load(target_file)
                        updated_data = update_specific_arrays(target_data, source_data)
                    with open(target_file_path, 'w', encoding='utf-8') as target_file:
                        json.dump(updated_data, target_file, separators=(',', ':'))
                    print(f"已成功更新 {target_file_path} 文件中Agreements和Offsets数组的内容。")
                except json.JSONDecodeError:
                    print(f"{target_file_path} 文件中的内容不是合法的JSON格式，请检查文件内容。")
            else:
                print(f"文件 {target_file_path} 不存在，请确保MilthmData.json在桌面路径下。")
        except json.JSONDecodeError:
            print(f"{source_file_path} 文件中的内容不是合法的JSON格式，请检查文件内容。")
    else:
        print(f"文件 {source_file_path} 不存在，请确保选择的数据源文件在程序同级目录下。")


if __name__ == "__main__":
    process_json_file()