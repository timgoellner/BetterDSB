import requests
from parser import parse

BASE_URL = 'https://mobileapi.dsbcontrol.de/'


def auth(user: int, password: str) -> dict:
    result = requests.get(
        BASE_URL + f"authid?bundleid=de.heinekingmedia.dsbmobile&appversion=35&osversion=22&pushid&user={user}&password={password}")

    if not result.json():
        return {'error': 'invalid login credentials'}
    elif not result.ok:
        return {'error': 'request to the dsb server did not succeed'}
    else:
        return {'authid': result.json()}


def get(auth_id: str, table_id: str) -> dict:
    result = requests.get(BASE_URL + f"dsbtimetables?authid={auth_id}")

    if result.status_code == 500:
        return {'error': 'internal error on the dsb server (invalid authid?)'}
    elif not result.ok:
        return {'error': 'request to the dsb server did not succeed'}
    elif result.json() == []:
        return {'error': 'invalid authid'}

    result = result.json()

    if table_id.isdigit():
        if len(result) <= int(table_id): return {'error': 'invalid table id'}

        tables = []

        try:
            for table_child in result[int(table_id)]['Childs']:
                table = requests.get(table_child['Detail'])
                if not table.ok: return {'error': 'request to the dsb server did not succeed'}

                tables.append(table.text)
        except Exception as error:
            return {'error': 'unexpected structure of the dsb server response'}

        return parse(tables)

    else:
        global_tables = []

        for table_id, _ in enumerate(result):
            tables = []

            try:
                for table_child in result[table_id]['Childs']:
                    table = requests.get(table_child['Detail'])
                    if not table.ok: return {'error': 'request to the dsb server did not succeed'}

                    tables.append(table.text)
            except Exception as error:
                return {'error': 'unexpected structure of the dsb server response'}

            global_tables.append(parse(tables))

        return global_tables
