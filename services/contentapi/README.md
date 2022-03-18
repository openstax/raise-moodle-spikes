# Content API

This is a simple `contentapi` to go along with the `content` plugin prototype in this repo. It has a simple templatized HTML snippet that it will return by default provided an input ID at `/contents/{content_id}`. If you want the service to return a specific piece of content, you can place a file `{content_id}.html` in this directory and it will pick it up.