import os
import json
from datetime import datetime
import urllib.parse


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


def hex_to_text():
    desktop_path = get_desktop_path()
    input_file_name = "PC-MilthmData.txt"
    input_file_path = os.path.join(desktop_path, input_file_name)
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            cleaned_content = content.replace("\n", "").replace(" ", "").replace(",", "").replace("\\", "")
            byte_data = bytes.fromhex(cleaned_content)
            text = byte_data.decode('utf-8')
            return text
    except FileNotFoundError:
        print(f"文件 {input_file_path} 不存在，请检查文件路径或文件名是否正确。")
    except ValueError:
        print("文件中的十六进制字符串无法正确转换，请检查文件内容是否符合要求。")


def url_decode_and_json_to_readable_text():
    desktop_path = get_desktop_path()
    input_file_name = "PE-MilthmData.txt"
    input_file_path = os.path.join(desktop_path, input_file_name)
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            encoded_content = file.read()
            decoded_content = urllib.parse.unquote(encoded_content)
            return decoded_content
    except FileNotFoundError:
        print(f"文件 {input_file_path} 不存在，请检查文件路径或文件名是否正确。")
    except:
        print("读取文件或解码过程中出现其他未知错误，请检查相关情况。")
desktop_path = get_desktop_path()
pc_file_path = os.path.join(desktop_path, "PC-MilthmData.txt")
pe_file_path = os.path.join(desktop_path, "PE-MilthmData.txt")
pc_file_exists = os.path.exists(pc_file_path)
pe_file_exists = os.path.exists(pe_file_path)

if pc_file_exists and pe_file_exists:
    choice = input("PC-MilthmData.txt和PE-MilthmData.txt都存在，请选择要转换的文件（输入PC或PE）：")
    if choice.upper() == "PC":
        result = hex_to_text()
    elif choice.upper() == "PE":
        result = url_decode_and_json_to_readable_text()
    else:
        print("输入无效，请重新运行程序并输入正确的选择（PC或PE）。")
        result = None
elif pc_file_exists:
    result = hex_to_text()
elif pe_file_exists:
    result = url_decode_and_json_to_readable_text()
else:
    print("PC-MilthmData.txt和PE-MilthmData.txt都不存在，请检查文件是否存在于桌面路径下或文件名是否正确。")
    result = None

if result:
    desktop_path = get_desktop_path()
    output_file_path = os.path.join(desktop_path, "MilthmData.json")
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(result)
    print(f"转换结果已成功写入文件 {output_file_path}")