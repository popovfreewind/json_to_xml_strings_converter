import os
import json
import shutil

def clear_output_folder(output_folder):
    """
    Clears the output folder by removing all files and subdirectories.
    """
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

def json_to_xml(json_list, theme_name):
    """
    Converts a list of strings to an XML string where each item is wrapped in a <string> tag.
    Escapes special characters like apostrophes and includes the adventure name in the XML row.
    """
    xml_output = "<resources>\n"
    for index, item in enumerate(json_list, start=1):
        # Escape apostrophes
        escaped_item = item.replace("'", "\\'")
        xml_output += f'    <string name="{theme_name}_text{index}">{escaped_item}</string>\n'
    xml_output += "</resources>"
    return xml_output

def main():
    input_folder = "input"
    output_folder = "output"

    # Clear the output folder before processing.
    clear_output_folder(output_folder)

    # Traverse the entire directory tree of the input folder.
    for root, dirs, files in os.walk(input_folder):
        # Calculate the relative path from the input folder.
        relative_path = os.path.relpath(root, input_folder)
        # Construct the corresponding folder in the output folder.
        output_dir = os.path.join(output_folder, relative_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for filename in files:
            if filename.lower().endswith(".json"):
                input_path = os.path.join(root, filename)
                base_name = os.path.splitext(filename)[0]
                output_filename = base_name + ".xml"
                output_path = os.path.join(output_dir, output_filename)
                
                # Extract the adventure name from the filename (e.g., "strings_adventure").
                theme_name = base_name.split("_")[-1]
                
                # Read JSON data from the file.
                try:
                    with open(input_path, "r", encoding="utf-8") as json_file:
                        data = json.load(json_file)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in {input_path}: {e}")
                    continue
                
                # Check if the JSON data is a list.
                if not isinstance(data, list):
                    print(f"Skipping {input_path} because it does not contain a JSON array.")
                    continue
                
                # Convert the JSON array to XML.
                xml_result = json_to_xml(data, theme_name)
                
                # Write the XML output to the corresponding file in the output directory.
                with open(output_path, "w", encoding="utf-8") as xml_file:
                    xml_file.write(xml_result)
                
                print(f"Converted {input_path} to {output_path}")

if __name__ == '__main__':
    main()