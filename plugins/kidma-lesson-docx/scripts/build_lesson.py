#!/usr/bin/env python3
"""
Build a Kidma lesson plan .docx by injecting content into the branded template.

Usage:
    python build_lesson.py <template.docx> <content.json> <output.docx>

The script:
1. Unpacks the template .docx
2. Rebuilds document.xml body from the JSON content using the template's styles
3. Repacks into a new .docx preserving headers, footers, logos, fonts
"""

import json
import sys
import os
import shutil
import zipfile
from xml.sax.saxutils import escape

def xml_text(text, rtl=True, bold=False, color=None, space_preserve=False):
    """Generate a w:r (run) element with text."""
    rpr_parts = []
    if bold:
        rpr_parts.append('<w:b w:val="1"/><w:bCs w:val="1"/>')
    if color:
        rpr_parts.append(f'<w:color w:val="{color}"/>')
    rpr_parts.append(f'<w:rtl w:val="{"1" if rtl else "0"}"/>')
    rpr = f'<w:rPr>{"".join(rpr_parts)}</w:rPr>'
    
    space_attr = ' xml:space="preserve"' if space_preserve else ''
    escaped = escape(text)
    return f'<w:r>{rpr}<w:t{space_attr}>{escaped}</w:t></w:r>'


def para(style, runs, bidi=True, extra_ppr=""):
    """Generate a w:p (paragraph) element."""
    bidi_xml = '<w:bidi w:val="1"/>' if bidi else ''
    style_xml = f'<w:pStyle w:val="{style}"/>' if style else ''
    return f'<w:p><w:pPr>{style_xml}{bidi_xml}{extra_ppr}<w:rPr/></w:pPr>{"".join(runs)}</w:p>'


def empty_para():
    """Generate an empty paragraph."""
    return '<w:p><w:pPr><w:bidi w:val="1"/><w:rPr/></w:pPr><w:r><w:rPr><w:rtl w:val="0"/></w:rPr></w:r></w:p>'


def bullet_para(label, text, num_id, ilvl=0):
    """Generate a bullet paragraph with bold label + regular text.
    Element order in pPr: pStyle, numPr, bidi, spacing, ind, jc, rPr."""
    num_xml = f'<w:numPr><w:ilvl w:val="{ilvl}"/><w:numId w:val="{num_id}"/></w:numPr>'
    runs = []
    if label:
        runs.append(xml_text(label, rtl=True, bold=True, space_preserve=True))
        runs.append(xml_text(f" {text}", rtl=True, space_preserve=True))
    else:
        runs.append(xml_text(text, rtl=True))
    return f'<w:p><w:pPr>{num_xml}<w:bidi w:val="1"/><w:rPr/></w:pPr>{"".join(runs)}</w:p>'


def simple_bullet(text, num_id, ilvl=0):
    """Generate a simple bullet paragraph (no bold label).
    Element order in pPr: pStyle, numPr, bidi, spacing, ind, jc, rPr."""
    num_xml = f'<w:numPr><w:ilvl w:val="{ilvl}"/><w:numId w:val="{num_id}"/></w:numPr>'
    return f'<w:p><w:pPr>{num_xml}<w:bidi w:val="1"/><w:rPr/></w:pPr>{xml_text(text, rtl=True)}</w:p>'


def heading4_blue(text):
    """Heading4 with blue color (#2669f6) — used for objective sub-headers."""
    extra = '<w:rPr><w:color w:val="2669f6"/></w:rPr>'
    run = xml_text(text, rtl=True, bold=True, color="2669f6")
    return f'<w:p><w:pPr><w:pStyle w:val="Heading4"/><w:bidi w:val="1"/>{extra}</w:pPr>{run}</w:p>'


def heading4(text):
    """Regular Heading4 — used for phase headers."""
    run = xml_text(text, rtl=True, bold=True, color="292920")
    return f'<w:p><w:pPr><w:pStyle w:val="Heading4"/><w:bidi w:val="1"/><w:rPr/></w:pPr>{run}</w:p>'


def heading6(text):
    """Heading6 (italic gray) — used for descriptions/instructions."""
    run = xml_text(text, rtl=True)
    return f'<w:p><w:pPr><w:pStyle w:val="Heading6"/><w:bidi w:val="1"/><w:rPr/></w:pPr>{run}</w:p>'


def subtitle(text):
    """Subtitle style — used for section headers."""
    run = xml_text(text, rtl=True)
    return f'<w:p><w:pPr><w:pStyle w:val="Subtitle"/><w:bidi w:val="1"/><w:rPr/></w:pPr>{run}</w:p>'


def title_para(lesson_number, topic):
    """Generate the title paragraph: 'שיעור XX - נושא השיעור'."""
    runs = [
        xml_text("שיעור ", rtl=True, space_preserve=True),
        xml_text(str(lesson_number), rtl=False),
        xml_text(f" - {topic}", rtl=True, space_preserve=True),
    ]
    return f'<w:p><w:pPr><w:pStyle w:val="Title"/><w:bidi w:val="1"/><w:rPr/></w:pPr>{"".join(runs)}</w:p>'


def normal_para(text):
    """Normal paragraph with text."""
    run = xml_text(text, rtl=True)
    return f'<w:p><w:pPr><w:bidi w:val="1"/><w:rPr/></w:pPr>{run}</w:p>'


def build_document_body(content):
    """Build the full document body XML from content JSON."""
    # Find the bullet numId from the template's numbering.xml
    # The template uses numId="1" for bullets
    BULLET_NUM_ID = "1"
    
    parts = []
    
    # === TITLE ===
    parts.append(title_para(content["lesson_number"], content["title"]))
    parts.append(empty_para())  # spacer after title
    
    # === מטרות השיעור ===
    parts.append(subtitle("מטרות השיעור"))
    
    # הבנה
    parts.append(heading4_blue("הבנה"))
    for bullet in content["objectives"]["understanding"]:
        parts.append(simple_bullet(bullet, BULLET_NUM_ID))
    parts.append(empty_para())
    
    # התנסות
    parts.append(heading4_blue("התנסות"))
    for bullet in content["objectives"]["experimentation"]:
        parts.append(simple_bullet(bullet, BULLET_NUM_ID))
    parts.append(empty_para())
    
    # יצירה
    parts.append(heading4_blue("יצירה"))
    for bullet in content["objectives"]["creation"]:
        parts.append(simple_bullet(bullet, BULLET_NUM_ID))
    parts.append(empty_para())
    
    # === עזרים והכנה לשיעור ===
    parts.append(subtitle("עזרים והכנה לשיעור"))
    for item in content["materials"]:
        parts.append(simple_bullet(item, BULLET_NUM_ID))
    parts.append(empty_para())
    
    # === חומרים ללמידה ===
    parts.append(subtitle("חומרים ללמידה"))
    if content.get("learning_materials"):
        parts.append(normal_para(content["learning_materials"]))
    parts.append(empty_para())
    
    # === מבנה השיעור (90 דקות) ===
    parts.append(subtitle("מבנה השיעור (90 דקות)"))
    
    # הקדמה
    parts.append(heading4("הקדמה (כ-5 דקות)"))
    structure = content["structure"]
    if structure["introduction"].get("description"):
        parts.append(heading6(structure["introduction"]["description"]))
    parts.append(empty_para())
    for b in structure["introduction"].get("bullets", []):
        parts.append(bullet_para(b.get("label", ""), b.get("text", ""), BULLET_NUM_ID))
    
    # הבנה
    parts.append(heading4("ההבנה (כ-20 דקות)"))
    if structure["understanding"].get("description"):
        parts.append(heading6(structure["understanding"]["description"]))
    parts.append(empty_para())
    for b in structure["understanding"].get("bullets", []):
        parts.append(bullet_para(b.get("label", ""), b.get("text", ""), BULLET_NUM_ID))
    
    # התנסות
    parts.append(heading4("התנסות (כ-20 דקות)"))
    if structure["experimentation"].get("description"):
        parts.append(heading6(structure["experimentation"]["description"]))
    parts.append(empty_para())
    for b in structure["experimentation"].get("bullets", []):
        parts.append(bullet_para(b.get("label", ""), b.get("text", ""), BULLET_NUM_ID))
    
    # יצירה
    parts.append(heading4("יצירה (כ-35 דקות)"))
    if structure["creation"].get("description"):
        parts.append(heading6(structure["creation"]["description"]))
    parts.append(empty_para())
    for b in structure["creation"].get("bullets", []):
        parts.append(bullet_para(b.get("label", ""), b.get("text", ""), BULLET_NUM_ID))
    
    # סיכום
    parts.append(heading4("סיכום (כ-5 דקות)"))
    if structure["summary"].get("description"):
        parts.append(heading6(structure["summary"]["description"]))
    parts.append(empty_para())
    for b in structure["summary"].get("bullets", []):
        parts.append(bullet_para(b.get("label", ""), b.get("text", ""), BULLET_NUM_ID))
    parts.append(empty_para())
    
    # === זמנים מתים ===
    parts.append(subtitle("זמנים מתים"))
    if content.get("dead_time"):
        parts.append(normal_para(content["dead_time"]))
    parts.append(empty_para())
    
    # === הערכה ===
    parts.append(subtitle("הערכה"))
    if content.get("assessment"):
        parts.append(normal_para(content["assessment"]))
    parts.append(empty_para())
    
    # === הערות למדריך ===
    parts.append(subtitle("הערות למדריך"))
    if content.get("instructor_notes"):
        parts.append(normal_para(content["instructor_notes"]))
    
    return "\n    ".join(parts)


def build_document_xml(body_content, sect_pr):
    """Wrap body content in the full document XML with namespaces and sectPr."""
    namespaces = (
        'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:w10="urn:schemas-microsoft-com:office:word" '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
        'xmlns:sl="http://schemas.openxmlformats.org/schemaLibrary/2006/main" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
        'xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" '
        'xmlns:lc="http://schemas.openxmlformats.org/drawingml/2006/lockedCanvas" '
        'xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram" '
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
        'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
        'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" '
        'xmlns:w16="http://schemas.microsoft.com/office/word/2018/wordml" '
        'xmlns:w16cex="http://schemas.microsoft.com/office/word/2018/wordml/cex" '
        'xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid"'
    )
    
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<w:document {namespaces}>
  <w:body>
    {body_content}
    {sect_pr}
  </w:body>
</w:document>'''


def extract_sect_pr(document_xml_path):
    """Extract the <w:sectPr>...</w:sectPr> block from the template document.xml.
    Also fixes margin values (converts floats to ints) and adds gutter if missing."""
    import re
    with open(document_xml_path, 'r', encoding='utf-8') as f:
        content = f.read()
    start = content.rfind('<w:sectPr>')
    end = content.find('</w:sectPr>', start) + len('</w:sectPr>')
    if start == -1 or end < len('</w:sectPr>'):
        raise ValueError("Could not find <w:sectPr> in template document.xml")
    sect_pr = content[start:end]
    
    # Fix float values in pgMar attributes → integers
    def fix_float_attr(match):
        attr_name = match.group(1)
        value = match.group(2)
        try:
            int_value = str(int(float(value)))
            return f'w:{attr_name}="{int_value}"'
        except ValueError:
            return match.group(0)
    
    sect_pr = re.sub(r'w:(bottom|top|left|right|header|footer|gutter)="([^"]+)"', fix_float_attr, sect_pr)
    
    # Add gutter="0" if missing
    if 'w:gutter' not in sect_pr:
        sect_pr = sect_pr.replace('w:footer=', 'w:gutter="0" w:footer=')
    
    return sect_pr


def unpack_docx(docx_path, output_dir):
    """Unpack a .docx file into a directory."""
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    with zipfile.ZipFile(docx_path, 'r') as z:
        z.extractall(output_dir)


def repack_docx(source_dir, output_path):
    """Repack a directory into a .docx file."""
    if os.path.exists(output_path):
        os.remove(output_path)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                z.write(file_path, arcname)


def main():
    if len(sys.argv) != 4:
        print("Usage: python build_lesson.py <template.docx> <content.json> <output.docx>")
        sys.exit(1)
    
    template_path = sys.argv[1]
    content_path = sys.argv[2]
    output_path = sys.argv[3]
    
    # Load content
    with open(content_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    # Unpack template
    work_dir = '/tmp/lesson_docx_work'
    unpack_docx(template_path, work_dir)
    
    # Extract sectPr (preserves header/footer references, page size, margins)
    sect_pr = extract_sect_pr(os.path.join(work_dir, 'word', 'document.xml'))
    
    # Build new document body
    body = build_document_body(content)
    doc_xml = build_document_xml(body, sect_pr)
    
    # Write new document.xml
    with open(os.path.join(work_dir, 'word', 'document.xml'), 'w', encoding='utf-8') as f:
        f.write(doc_xml)
    
    # Repack
    repack_docx(work_dir, output_path)
    
    # Cleanup
    shutil.rmtree(work_dir, ignore_errors=True)
    
    print(f"✅ Lesson plan saved to: {output_path}")


if __name__ == '__main__':
    main()
