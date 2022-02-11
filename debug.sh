docker-compose exec moodle pecl install xdebug
docker-compose exec moodle /bin/bash -c 'echo "xdebug.mode = debug" > /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini'
docker-compose exec moodle /bin/bash -c 'echo "xdebug.client_host = host.docker.internal" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini'
docker-compose exec moodle /bin/bash -c 'echo "xdebug.start_with_request = yes" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini'
docker-compose exec moodle docker-php-ext-enable xdebug
docker-compose restart moodle
