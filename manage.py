#!/usr/bin/env python
from migrate.versioning.shell import main
import json

if __name__ == '__main__':
    with open("config/settings.json") as f:
        config = json.loads(f.read())
    mysql_json = config.get("MYSQL", {})
    db_url = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}"
    db_url = db_url.format(user=mysql_json.get("user"), password=mysql_json.get("password"),
                           host=mysql_json.get("host"),
                           port=mysql_json.get("port"), dbname=mysql_json.get("dbname"))

    main(repository='migrations', url=db_url, debug='True')
