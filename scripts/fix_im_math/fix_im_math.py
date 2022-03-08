import sys
from glob import glob
from lxml import etree, html


def replace_math_image(element):
    latex_math = element.attrib["data-equation-content"]
    new_content = f'\\( {latex_math} \\)'
    parent_element = element.getparent()
    parent_element.remove(element)
    parent_element.text = new_content


def repair_html(html_filename):
    parser = etree.HTMLParser(encoding='utf-8')
    tree = html.parse(html_filename, parser)

    broken_images = tree.xpath("//img[@data-equation-content]")
    if not broken_images:
        return
    print(f"Found {len(broken_images)} broken images in {html_filename}")
    for image in broken_images:
        replace_math_image(image)

    tree.write(html_filename, encoding="utf-8", method="html")


def repair_xml(xml_filename):
    parser = etree.XMLParser(encoding='utf-8')
    tree = etree.parse(xml_filename, parser)

    broken_images = tree.xpath(
        "//x:img[@data-equation-content]",
        namespaces={
            "x": "http://www.imsglobal.org/xsd/ims_qtiasiv1p2"
        }
    )
    if not broken_images:
        return
    print(f"Found {len(broken_images)} broken images in {xml_filename}")
    for image in broken_images:
        replace_math_image(image)

    tree.write(xml_filename, encoding="utf-8", xml_declaration=True)


def repair_qti(xml_filename):
    parser = etree.XMLParser(encoding='utf-8')
    tree = etree.parse(xml_filename, parser)

    broken_images = tree.xpath(
        "//img[@data-equation-content]"
    )
    if not broken_images:
        return
    print(f"Found {len(broken_images)} broken images in {xml_filename}")
    for image in broken_images:
        replace_math_image(image)

    tree.write(xml_filename, encoding="utf-8", xml_declaration=True)


def main():
    content_path = sys.argv[1]
    html_files = glob(f"{content_path}/**/*.html", recursive=True)
    xml_files = glob(f"{content_path}/**/*.xml", recursive=True)
    qti_files = glob(f"{content_path}/**/*.qti", recursive=True)

    for html_filename in html_files:
        repair_html(html_filename)

    for xml_filename in xml_files:
        repair_xml(xml_filename)

    for qti_filename in qti_files:
        repair_qti(qti_filename)


if __name__ == "__main__":
    main()
