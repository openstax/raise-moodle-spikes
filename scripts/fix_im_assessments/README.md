# Fix assessments in IM content

The content we receive from IM has issues with the assessment data including:

* The manifest does not reference assessments in a way that will trigger Moodle to convert / import questions / quizzes
* The XML includes embedded HTML which is not escaped resulting in issues when importing into Moodle

The `fix_im_assessments.py` script here can be used to fix both of these items (:warning: The script was written as a quick fix and may still have issues):

```bash
$ pip install -r requirements.txt
$ python fix_im_assessments.py <path_to_catridge_extract>/imsmanifest.xml <path_to_catridge_extract>/imsmanifest.xml
```
