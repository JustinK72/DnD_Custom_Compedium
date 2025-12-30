import os
import json
import xml.etree.ElementTree as ET

# --- CONFIGURATION ---
SOURCE_ROOT = 'Sources'
OUTPUT_FC5 = '1_XML_Compendium.xml'
OUTPUT_BLASTER = '2_Companion_Repo.json'

# --- HELPERS ---
def get_text(element, tag, default=""):
    child = element.find(tag)
    return child.text if child is not None else default

def clean_xml_line(line):
    s = line.strip()
    if s.startswith("<?xml") or s.startswith("<compendium") or s.startswith("</compendium"):
        return None
    return line.rstrip()

# --- JSON TRANSLATORS ---

def xml_to_blaster_monster(xml_root):
    items = []
    for m in xml_root.findall(".//monster"):
        try:
            obj = {
                "name": get_text(m, 'name'),
                "size": get_text(m, 'size'),
                "type": get_text(m, 'type'),
                "alignment": get_text(m, 'alignment'),
                "ac": get_text(m, 'ac'),
                "hp": get_text(m, 'hp'),
                "cr": get_text(m, 'cr'),
                "traits": [{"name": get_text(t, 'name'), "desc": get_text(t, 'text')} for t in m.findall('trait')],
                "actions": [{"name": get_text(a, 'name'), "desc": get_text(a, 'text')} for a in m.findall('action')]
            }
            items.append(obj)
        except: continue
    return items

def xml_to_blaster_feat(xml_root):
    items = []
    for f in xml_root.findall(".//feat"):
        try:
            desc_lines = [t.text for t in f.findall('text') if t.text]
            obj = {
                "name": get_text(f, 'name'),
                "description": "\n".join(desc_lines),
                "source": get_text(f, 'source')
            }
            items.append(obj)
        except: continue
    return items

def xml_to_blaster_race(xml_root):
    items = []
    for r in xml_root.findall(".//race"):
        try:
            obj = {
                "name": get_text(r, 'name'),
                "speed": get_text(r, 'speed'),
                "size": get_text(r, 'size'),
                "traits": [{"name": get_text(t, 'name'), "desc": get_text(t, 'text')} for t in r.findall('trait')]
            }
            items.append(obj)
        except: continue
    return items

def xml_to_blaster_background(xml_root):
    items = []
    for b in xml_root.findall(".//background"):
        try:
            traits = [{"name": get_text(t, 'name'), "desc": get_text(t, 'text')} for t in b.findall('trait')]
            obj = {
                "name": get_text(b, 'name'),
                "traits": traits
            }
            items.append(obj)
        except: continue
    return items

# --- NEW TRANSLATORS ADDED BELOW ---

def xml_to_blaster_spell(xml_root):
    items = []
    for s in xml_root.findall(".//spell"):
        try:
            desc_lines = [t.text for t in s.findall('text') if t.text]
            obj = {
                "name": get_text(s, 'name'),
                "level": get_text(s, 'level'), # App expects integer usually, but string often works
                "school": get_text(s, 'school'),
                "time": get_text(s, 'time'),
                "range": get_text(s, 'range'),
                "components": get_text(s, 'components'),
                "duration": get_text(s, 'duration'),
                "description": "\n".join(desc_lines),
                "classes": get_text(s, 'classes') # e.g. "Wizard, Sorcerer"
            }
            items.append(obj)
        except: continue
    return items

def xml_to_blaster_item(xml_root):
    items = []
    for i in xml_root.findall(".//item"):
        try:
            desc_lines = [t.text for t in i.findall('text') if t.text]
            obj = {
                "name": get_text(i, 'name'),
                "type": get_text(i, 'type'), # e.g. "W" for weapon
                "rarity": get_text(i, 'rarity'),
                "weight": get_text(i, 'weight'),
                "value": get_text(i, 'value'),
                "description": "\n".join(desc_lines)
            }
            # Optional: Add damage fields if it's a weapon
            dmg = get_text(i, 'dmg1')
            if dmg:
                obj["damage"] = dmg
                obj["damage_type"] = get_text(i, 'dmgType')
            
            items.append(obj)
        except: continue
    return items

def xml_to_blaster_class(xml_root):
    classes = []
    for c in xml_root.findall(".//class"):
        try:
            # 1. Basic Class Info
            class_obj = {
                "name": get_text(c, 'name'),
                "hit_dice": get_text(c, 'hd'),
                "features": []
            }
            
            # 2. Extract Features from Autolevels
            # We must flatten the structure: <autolevel level="1"><feature> -> {level: 1, feature...}
            for al in c.findall('autolevel'):
                lvl = al.get('level')
                
                # Check for subclass definition
                subclass_tag = al.find('subclass')
                subclass_name = subclass_tag.text if subclass_tag is not None else None
                
                for feat in al.findall('feature'):
                    feat_name = get_text(feat, 'name')
                    feat_text = get_text(feat, 'text')
                    
                    # If this feature belongs to a subclass, append name to title
                    # to prevent confusion in the app
                    if subclass_name:
                        feat_name = f"{feat_name} ({subclass_name})"
                    
                    feature_obj = {
                        "name": feat_name,
                        "description": feat_text,
                        "level": int(lvl) if lvl.isdigit() else 1
                    }
                    class_obj["features"].append(feature_obj)
            
            classes.append(class_obj)
        except Exception as e:
            # Print error to help debug which class failed
            print(f"Skipping class {get_text(c, 'name')}: {e}")
            continue
            
    return classes

# --- MAIN ---
def main():
    print("🚀 Starting Full Suite Build (v4.0)...")
    
    # 1. BUILD XML MASTER
    fc5_content = ['<?xml version="1.0" encoding="UTF-8"?>', '<compendium version="5">']
    raw_xml_string = ""

    for root, dirs, files in os.walk(SOURCE_ROOT):
        for filename in files:
            if filename.endswith(".xml"):
                path = os.path.join(root, filename)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for line in lines:
                            cleaned = clean_xml_line(line)
                            if cleaned:
                                fc5_content.append(cleaned)
                                raw_xml_string += cleaned + "\n"
                except Exception as e:
                    print(f"⚠️ Error reading {filename}: {e}")

    fc5_content.append('</compendium>')
    with open(OUTPUT_FC5, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fc5_content))
    print(f"✅ XML Compendium Built: {OUTPUT_FC5}")

    # 2. BUILD JSON REPO
    print("🔄 Translating to Companion App JSON...")
    try:
        # Wrap raw string to make it valid XML for parsing
        fake_root_xml = f"<root>{raw_xml_string}</root>"
        root_element = ET.fromstring(fake_root_xml)
        
        final_json = {
            "source": "My Custom Repo",
            "homebrew": True,
            "monsters": xml_to_blaster_monster(root_element),
            "feats": xml_to_blaster_feat(root_element),
            "races": xml_to_blaster_race(root_element),
            "backgrounds": xml_to_blaster_background(root_element),
            "spells": xml_to_blaster_spell(root_element),    # NEW
            "items": xml_to_blaster_item(root_element),      # NEW
            "classes": xml_to_blaster_class(root_element)    # NEW
        }
        
        with open(OUTPUT_BLASTER, 'w', encoding='utf-8') as f:
            json.dump(final_json, f, indent=4)
        print(f"✅ JSON Repository Built: {OUTPUT_BLASTER}")
        
    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")

if __name__ == "__main__":
    main()