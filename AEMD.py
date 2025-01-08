import os
import json
from urllib.parse import quote


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


def text_to_hex():
    desktop_path = get_desktop_path()
    input_file_name = "MilthmData.json"
    input_file_path = os.path.join(desktop_path, input_file_name)
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            byte_data = text.encode('utf-8')
            hex_string = byte_data.hex()
            return hex_string
    except FileNotFoundError:
        print(f"文件 {input_file_path} 不存在，请检查文件路径是否正确。")
    except UnicodeEncodeError:
        print("文件中的内容无法正确编码为字节数据，请检查文件内容是否符合要求。")


def insert_commas(hex_str):
    result = ""
    for i in range(0, len(hex_str), 2):
        result += hex_str[i:i + 2]
        if i + 2 < len(hex_str):
            result += ","
    return result


def insert_newlines(hex_str):
    result = hex_str[:51] + "\n  "
    index = 51
    while index < len(hex_str):
        result += hex_str[index:index + 75]
        index += 75
        if index < len(hex_str):
            result += "\n  "
    return result


def add_backslash_before_newline(text):
    new_text = ""
    for char in text:
        if char == "\n":
            new_text += "\\"
        new_text += char
    return new_text


def text_to_html_url_encoding():
    desktop_path = get_desktop_path()
    input_file_name = "MilthmData.json"
    input_file_path = os.path.join(desktop_path, input_file_name)
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            html_url_encoded_text = quote(text, safe="")
            return html_url_encoded_text
    except FileNotFoundError:
        print(f"文件 {input_file_path} 不存在，请检查文件路径是否正确。")
    except UnicodeEncodeError:
        print("文件中的内容无法正确编码为字节数据，请检查文件内容是否符合要求。")


if __name__ == "__main__":
    choice = input("请输入要进行的转换类型(PC/PE)：")
    if choice == "PC":
        result = text_to_hex()
        if result:
            desktop_path = get_desktop_path()
            output_file_name = "EndMilthmData.json"
            output_file_path = os.path.join(desktop_path, output_file_name)
            if not os.path.exists(desktop_path):
                os.makedirs(desktop_path)
            result_with_commas = insert_commas(result)
            result_with_newlines = insert_newlines(result_with_commas)
            result_with_backslash = add_backslash_before_newline(result_with_newlines)
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(result_with_backslash)
            print(f"转换结果已成功写入文件 {output_file_path}")
    elif choice == "PE":
        result = text_to_html_url_encoding()
        if result:
            desktop_path = get_desktop_path()
            output_file_name = "EndMilthmData.json"
            output_file_path = os.path.join(desktop_path, output_file_name)
            if not os.path.exists(desktop_path):
                os.makedirs(desktop_path)
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(result)
            print(f"转换结果已成功写入文件 {output_file_path}")
    else:
        print("输入的转换类型不合法，请重新输入。")