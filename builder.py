import os
import json
import xml.etree.ElementTree as ET

# CONFIGURATION
SOURCE_DIR = 'Sources'
OUTPUT_XML = 'Master_Compendium.xml'
OUTPUT_JSON = 'Blaster_Repository.json'

def get_text(element, tag, default=""):
    """Helper to safely get text from XML tags"""
    child = element.find(tag)
    return child.text if child is not None else default

def xml_to_blaster_monster(xml_root):
    """Converts a Lion's Den Monster XML element to Blastervla JSON format"""
    monsters = []
    
    for m in xml_root.findall('monster'):
        # Basic mapping - precise field names derived from community reverse engineering
        monster_obj = {
            "name": get_text(m, 'name'),
            "size": get_text(m, 'size'),
            "type": get_text(m, 'type'),
            "alignment": get_text(m, 'alignment'),
            "ac": get_text(m, 'ac'),
            "hp": get_text(m, 'hp'),
            "speed": get_text(m, 'speed'),
            "str": get_text(m, 'str'),
            "dex": get_text(m, 'dex'),
            "con": get_text(m, 'con'),
            "int": get_text(m, 'int'),
            "wis": get_text(m, 'wis'),
            "cha": get_text(m, 'cha'),
            "cr": get_text(m, 'cr'),
            "xp": get_text(m, 'xp'),
            "traits": [],
            "actions": []
        }

        # Handle Traits
        for t in m.findall('trait'):
            monster_obj["traits"].append({
                "name": get_text(t, 'name'),
                "desc": get_text(t, 'text')
            })

        # Handle Actions
        for a in m.findall('action'):
            monster_obj["actions"].append({
                "name": get_text(a, 'name'),
                "desc": get_text(a, 'text')
            })

        monsters.append(monster_obj)
    
    return monsters

def main():
    # --- PART 1: BUILD XML MASTER ---
    print("Building XML Master...")
    master_content = ['<?xml version="1.0" encoding="UTF-8"?>', '<compendium version="5">']
    
    full_xml_string = "" # We need this for the JSON conversion later

    if not os.path.exists(SOURCE_DIR):
        print(f"Error: Folder '{SOURCE_DIR}' not found.")
        return

    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith(".xml"):
            file_path = os.path.join(SOURCE_DIR, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        s_line = line.strip()
                        # Skip wrappers for the merge
                        if s_line.startswith("<?xml") or s_line.startswith("<compendium") or s_line.startswith("</compendium"):
                            continue
                        master_content.append(line.rstrip())
                        full_xml_string += line.rstrip() + "\n"
            except Exception as e:
                print(f"Failed to read {filename}: {e}")

    master_content.append('</compendium>')
    
    with open(OUTPUT_XML, 'w', encoding='utf-8') as f:
        f.write('\n'.join(master_content))
    print(f"XML Done: {OUTPUT_XML}")

    # --- PART 2: CONVERT TO JSON ---
    print("Converting to JSON for 5e Companion...")
    
    # We wrap the raw content in a root tag so ElementTree can parse it
    fake_root = f"<root>{full_xml_string}</root>"
    try:
        root = ET.fromstring(fake_root)
        monsters_json = xml_to_blaster_monster(root)
        
        # Blastervla usually expects a specific wrapper. 
        # This is a generic "repository" structure.
        final_json = {
            "monsters": monsters_json,
            "homebrew": True
        }

        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(final_json, f, indent=4)
        print(f"JSON Done: {OUTPUT_JSON}")
        
    except ET.ParseError as e:
        print(f"XML Parse Error (Check your syntax): {e}")

if __name__ == "__main__":
    main()