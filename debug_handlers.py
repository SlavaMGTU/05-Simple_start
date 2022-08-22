from flask import Flask
from flask import request
import json
from ui_global import setup_db
import ui_global
from pony.orm.core import db_session
from pony import orm
from pony.orm import Database, Required, Set, select, commit
import json






import copy

from pony import orm as pony_orm

# from global_module import _CUSTOM_TABLE as TABLE
# from global_module import setup_db, Measure, Tag, Product, ProductTag


app = Flask(__name__)


def create_db(hashMap, _files=None, _data=None):
    """
    Creates tables in the internal db
    """
    setup_db()

    return hashMap


create_db(hashMap=None)
#
#
# @pony_orm.db_session
# def create_measure(*args, **kwargs):
#     """
#     Creates the Measure instance
#     """
#
#     measure_new = Measure(**kwargs)
#
#     return measure_new
#
#
# @pony_orm.db_session
# def get_measure(*args, **kwargs):
#     """
#     Retrieves the Measure instance
#     """
#
#     measure = Measure.get(**kwargs)
#
#     return measure
#
#
# @pony_orm.db_session
# def get_measure_list(*args, **kwargs):
#     """
#     Retrieves the list of Measure instances
#     """
#
#     measure_list_query = pony_orm.select(measure for measure in Measure).fetch()
#     measure_list = list(measure_list_query)
#
#     return measure_list
#
#
# @pony_orm.db_session
# def create_tag(*args, **kwargs):
#     """
#     Creates the Tag instance
#     """
#
#     tag_new = Tag(**kwargs)
#
#     return tag_new
#
#
# @pony_orm.db_session
# def get_tag(*args, **kwargs):
#     """
#     Retrieves the Tag instance
#     """
#
#     tag = Tag.get(**kwargs)
#
#     return tag
#
#
# @pony_orm.db_session
# def create_product(*args, **kwargs):
#     """
#     Creates the Product instance
#     """
#
#     product_new = Product(**kwargs)
#
#     return product_new
#
#
# @pony_orm.db_session
# def get_product(*args, **kwargs):
#     """
#     Retrieves the Tag instance
#     """
#
#     product = Product.get(**kwargs)
#
#     return product
#
#
# @pony_orm.db_session
# def get_product_list(*args, **kwargs):
#     """
#     Retrieves the list of Product instances
#     """
#
#     product_list_query = pony_orm.select(product for product in Product).fetch()
#
#     return product_list_query
#
#
# @pony_orm.db_session
# def create_product_tag(*args, **kwargs):
#     """
#     Creates the ProductTag instance
#     """
#
#     product_tag_new = ProductTag(**kwargs)
#
#     return product_tag_new
#
#
# @pony_orm.db_session
# def delete_product_tag(*args, **kwargs):
#     """
#     Deletes the ProductTag instance
#     """
#
#     product_tag = ProductTag.get(**kwargs)
#     product_tag.delete()


# -BEGIN CUSTOM HANDLERS

def _sample1_on_create(hashMap, _files=None, _data=None):
    if not hashMap.containsKey("a"):
        hashMap.put("a", "")
    if not hashMap.containsKey("b"):
        hashMap.put("b", "")
    return hashMap


def _sample1_on_input(hashMap, _files=None, _data=None):
    if hashMap.get("listener") == "btn_res":
        hashMap.put("toast", str(int(hashMap.get("a")) - int(hashMap.get("b"))))

    return hashMap


def _init_on_start(hashMap, _files=None, _data=None):
    ui_global.init()
    return hashMap


def _input_qty(hashMap, _files=None, _data=None):
    with db_session:
        p = ui_global.Record(barcode=hashMap.get('barcode'), name=hashMap.get('nom'), qty=int(hashMap.get('qty')))
        commit()

    hashMap.put("ShowScreen", "Сканирование штрихкода")
    hashMap.put("toast", "Добавлено")
    return hashMap


def _on_start_barcode(hashMap, _files=None, _data=None):
    table = {
        "type": "table",
        "textsize": "20",

        "columns": [
            {
                "name": "barcode",
                "header": "Barcode",
                "weight": "2"
            },
            {
                "name": "name",
                "header": "Name",
                "weight": "2"
            },
            {
                "name": "qty",
                "header": "Qty.",
                "weight": "1"
            }
        ]
    }
    # work with SQL via Pony ORM
    query = select(c for c in ui_global.Record)
    rows = []
    for record in query:
        rows.append({"barcode": record.barcode, "name": record.name, "qty": record.qty})

    table['rows'] = rows
    hashMap.put("table", json.dumps(table))

    return hashMap


def _on_start_active_cv(hashMap, _files=None, _data=None):
    import sqlite3  # This is another way to work with SQL
    from sqlite3.dbapi2 import Error
    import json

    # create connection with database
    conn = None
    try:
        conn = sqlite3.connect('//data/data/ru.travelfood.simple_ui/databases/SimpleWMS')
    except Error as e:
        raise ValueError('Нет соединения с базой!')

    cursor = conn.cursor()
    cursor.execute("SELECT barcode,name,qty FROM Record")

    results = cursor.fetchall()

    green_list = []
    red_list = []
    info_list = []
    for link in results:
        job = {"object": str(link[0]), "info": str(link[1]) + " </n> Остаток: <big>" + str(link[2]) + "</big>"}
        info_list.append(job)
        green_list.append(link[0])

    conn.close()

    hashMap.put("object_info_list", json.dumps(info_list, ensure_ascii=False))
    hashMap.put("green_list", ';'.join(green_list))

    return hashMap


# under construction
def _sample1_setscreenshot(hashMap, _files=None, _data=None):
    if hashMap.get("listener") == "btn_set":
        hashMap.put("setScreenshotURL", "http://192.168.1.143:2075/post_screenshot")
    elif hashMap.get("listener") == "btn_send":
        hashMap.put("sendScreenshots", "3")

    return hashMap

# -END CUSTOM HANDLERS

@app.route('/set_input_direct/<method>', methods=['POST'])
def set_input(method):
    func = method
    jdata = json.loads(request.data.decode("utf-8"))
    f = globals()[func]
    hashMap.d = jdata['hashmap']
    f(hashMap)
    jdata['hashmap'] = hashMap.export()
    jdata['stop'] = False
    jdata['ErrorMessage'] = ""
    jdata['Rows'] = []

    return json.dumps(jdata)


@app.route('/post_screenshot', methods=['POST'])
def post_screenshot():
    d = request.data
    return "1"


class hashMap:
    d = {}

    def put(key, val):
        hashMap.d[key] = val

    def get(key):
        return hashMap.d.get(key)

    def remove(key):
        if key in hashMap.d:
            hashMap.d.pop(key)

    def containsKey(key):
        return key in hashMap.d

    def export(key):
        ex_hashMap = []
        for key in hashMap.d.keys():
            ex_hashMap.append({"key": key, "value": hashMap.d[key]})
        return ex_hashMap


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2075, debug=True)