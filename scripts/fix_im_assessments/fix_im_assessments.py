import sys
from pathlib import Path
from lxml import etree
from functools import partial

NS_IMSCP = "http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1"
NS_IMSCC = "http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest"
NAMESPACES = {
    "lomimscc": NS_IMSCC,
    "imscp": NS_IMSCP
}


def manifest_xpath(tree, namespaces, query):
    return tree.xpath(query, namespaces=namespaces)


def get_assignment_title(assessment_meta_path):
    metadata = etree.parse(str(assessment_meta_path))
    return metadata.find(
        "{http://canvas.instructure.com/xsd/cccv1p0}title"
    ).text


def patch_qti_mattext(assessment_qti_path):
    def _localize_namespace(elem):
        for subelem in elem.iter():
            try:
                subelem.tag = etree.QName(subelem).localname
            except ValueError:
                # This can occur on embedded comments and perhaps other things
                # so we'll log for human review to catch unexpected issues
                print(
                    "Unable to localize the following content in "
                    f"{assessment_qti_path}: {subelem.text}"
                )

        etree.cleanup_namespaces(elem)

    tree = etree.parse(str(assessment_qti_path))
    mattext_nodes = tree.getroot().findall(
        ".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}"
        "mattext[@texttype='text/html']")

    for mattext in mattext_nodes:
        tmp_mattext = etree.fromstring(etree.tostring(mattext))
        # We need to localize namespaces as part of fixing the embedded HTML
        # in the XML
        _localize_namespace(tmp_mattext)

        newtext = ""
        for child in tmp_mattext.getchildren():
            newtext += etree.tostring(child, encoding="unicode")
            # Sanity check that the namespaces have been cleaned up and do not
            # appear in the HTML content
            if "xmlns" in newtext:
                raise Exception(
                    "Namespaced elements found when processing "
                    f"{assessment_qti_path}"
                )

        for child in mattext.getchildren():
            mattext.remove(child)
        mattext.text = newtext
    tree.write(
        str(assessment_qti_path),
        encoding="utf-8",
        xml_declaration=True
    )


def main():
    manifest_file = Path(sys.argv[1]).resolve(strict=True)
    updated_manifest_file = sys.argv[2]
    manifest_tree = etree.parse(str(manifest_file))
    xpath = partial(manifest_xpath, manifest_tree, NAMESPACES)
    items_parent = xpath('//imscp:organization/imscp:item')[0]

    assessment_nodes = xpath(
        "//imscp:resource[@type='imsqti_xmlv1p2/imscc_xmlv1p1/assessment']"
    )
    for assessment in assessment_nodes:
        assessment_id = assessment.get('identifier')
        assessment_qti_href = assessment.find(
            './/imscp:file',
            namespaces=NAMESPACES
        ).get("href")
        assessment_dependency_id = assessment.find(
            './/imscp:dependency', namespaces=NAMESPACES
        ).get("identifierref")
        dependency_node = xpath(
            f"//imscp:resource[@identifier='{assessment_dependency_id}']"
        )[0]
        assessment_qti_path = manifest_file.parent.joinpath(
            assessment_qti_href
        )
        patch_qti_mattext(assessment_qti_path)
        assessment_meta_path = manifest_file.parent.joinpath(
            dependency_node.get("href")
        )
        assessment_title = get_assignment_title(assessment_meta_path)

        # Add entry to the manifest
        elem_string = f'''
<item identifier="item-{assessment_id}" identifierref="{assessment_id}">
    <title>{assessment_title}</title>
</item>
        '''.replace("&", "&amp;")
        new_item_elem = etree.fromstring(elem_string)
        items_parent.append(new_item_elem)

    manifest_tree.write(
        updated_manifest_file,
        encoding="utf-8",
        xml_declaration=True
    )


if __name__ == "__main__":
    main()
