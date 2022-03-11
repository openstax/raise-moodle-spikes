<?php
class filter_content extends moodle_text_filter {
    public function filter($text, array $options = array()) {
        $matches = array();
        $pattern = '/\[osx-raise id="([0-9]*)"\]/';
        preg_match_all($pattern, $text, $matches);

        $new_html = $text;
        foreach ($matches[1] as $id) {
            $c = new curl;
            $object = $c->get("http://contentapi/contents/{$id}");
            $content = ((array)json_decode($object))['content'];

            $key = "/\[osx-raise id=\"" . $id . "\"\]/";
            $new_html = preg_replace($key, $content, $new_html);
        }
        return $new_html;
    }
}
