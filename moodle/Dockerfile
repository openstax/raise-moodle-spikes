FROM moodlehq/moodle-php-apache:8.0

ARG MOODLE_VERSION=v3.11.4

RUN rmdir /var/www/html
RUN git clone --depth 1 https://github.com/moodle/moodle --branch $MOODLE_VERSION /var/www/html
RUN rm -rf /var/www/html/.git
RUN chown -R www-data:www-data /var/www/html/

RUN apt-get update && apt-get install -y cron

COPY moodle/moodle-config.php /var/www/html/config.php
COPY moodle/php.ini-development /usr/local/etc/php/php.ini
COPY moodle/cron.moodle /etc/cron.d/moodle
RUN chmod 644 /etc/cron.d/moodle

COPY plugins/events /var/www/html/admin/tool/events
COPY plugins/study /var/www/html/mod/study
