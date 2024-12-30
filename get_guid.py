import xml.etree.ElementTree as ET

def extract_guids(xml_file, output_file):
    try:
        # 解析 XML 文件
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # 打开输出文件
        with open(output_file, 'w', encoding='utf-8') as file:
            # 查找所有的 <noteList> 节点
            for note_list in root.findall(".//noteList"):
                guid = note_list.find("guid")
                if guid is not None and guid.text:
                    file.write(guid.text + '\n')

        print(f"提取完成，所有 GUID 已写入 {output_file}")
    except ET.ParseError as e:
        print(f"解析 XML 文件时出错: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

# 输入 XML 文件和输出文件路径
xml_file = "query.xht"
output_file = "guids.txt"

# 提取 GUID
extract_guids(xml_file, output_file)
