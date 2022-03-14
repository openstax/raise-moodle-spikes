<?php
class filter_content extends moodle_text_filter {
    public function filter($text, array $options = array()) {
        global $PAGE;

        $matches = array();
        $pattern = '/\[osx-raise id="([0-9]*)"\]/';
        preg_match_all($pattern, $text, $matches);

        $load_fe_content = false;
        $filter_be = getenv('FILTER_CONTENT_BE');

        $new_html = $text;
        foreach ($matches[1] as $id) {
            $key = "/\[osx-raise id=\"" . $id . "\"\]/";
            if ($filter_be != false) {
                $c = new curl;
                $object = $c->get("http://contentapi/contents/{$id}");
                $content = ((array)json_decode($object))['content'];
                $new_html = preg_replace($key, $content, $new_html);
            } else {
                $load_fe_content = true;
                $content = "<div class=\"osx-raise-content\" data-id=\"{$id}\"></div>";
                $new_html = preg_replace($key, $content, $new_html);
            }

        }
        if ($load_fe_content) {
            $PAGE->requires->js_call_amd('filter_content/loader', 'load');
        }
        return $new_html;
    }
}
