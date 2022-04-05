#!/usr/bin/env bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

usage="gitify_mbz -i <inputfile> -o <outputfile>"

while getopts i:o:h flag
do
  case "${flag}" in
    i) input_file=${OPTARG} ;;
    o) output_file=${OPTARG} ;;
    h) echo "$usage"; exit 0 ;;
    *) echo "Unknown flag '${flag}'"; exit 1 ;;
  esac
done

if [ -z "$input_file" ] || [ -z "$output_file" ]; then
    echo "$usage"
    exit 1
fi

if [ ! -e "$input_file" ]; then
    echo "Input file '${input_file}' does not exist!"
    exit 1
fi

TMP_MBZ="${DIR}/../tmp.mbz"

cp "$input_file" "$TMP_MBZ"
docker-compose down -v
docker-compose up -d
docker-compose exec moodle php admin/cli/install_database.php --agree-license --fullname="Local Dev" --shortname="Local Dev" --summary="Local Dev" --adminpass="admin" --adminemail="admin@acmeinc.com"
# Run our slightly modified backup script instead of the one included with Moodle
docker-compose exec moodle php /repo/scripts/restore_backup_as_admin.php --file=/repo/tmp.mbz --categoryid=1
rm "$TMP_MBZ"
# Run our slightly modified backup script instead of the one included with Moodle
docker-compose exec moodle php /repo/scripts/backup_course.php --courseid=2 --destination=/repo/
find . -name "backup-moodle2-course-2-*.mbz" -print0 | xargs -0 -I filename mv filename "$output_file"
