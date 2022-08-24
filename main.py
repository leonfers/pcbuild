import datetime
from datetime import timedelta
import sqlite3
import requests_cache
from modelos import Product
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


con = sqlite3.connect("buildhistory.db")
root_url = 'https://pcbuildwizard.com/api/products'
session = requests_cache.CachedSession('cache',
                                       use_cache_dir=True,  # Save files in the default user cache dir
                                       cache_control=True,  # Use Cache-Control headers for expiration, if available
                                       expire_after=timedelta(hours=12),  # Otherwise expire responses after one day
                                       allowable_methods=['GET', 'POST'],
                                       # Cache POST requests to avoid sending the same data twice
                                       allowable_codes=[200, 400],
                                       # Cache 400 responses as a solemn reminder of your failures
                                       ignored_parameters=['api_key'],  # Don't match this param or save it in the cache
                                       match_headers=True,  # Match all request headers
                                       stale_if_error=True, )


def get_all_products(route, *args):
    keywords = list(args)
    url = f'{root_url}/{route}/'
    products = []
    result = session.get(url).json()
    for p in result:
        product = Product()
        product.build(p)
        products.append(product)
    products.sort(key=lambda x: x.avista, reverse=False)
    products = list(filter(lambda y: all(x in y.descricao for x in keywords), products))

    if len(products) > 0:
        return products[0]
    else:
        product = Product()
        product.avista = 0
        product.parcelado = 0
        product.nome = 'Não encontrado'
        product.descricao = 'Não encontrado'
        product.url = 'Não encontrado'
        return product


def search_cheapest_processor(*args):
    route = 'cpus'
    return get_all_products(route, *args)


def search_cheapest_video_card(*args):
    route = 'video-cards'
    return get_all_products(route, *args)


def search_cheapest_monitor(*args):
    route = 'monitors'
    return get_all_products(route, *args)


def search_cheapest_motherboard(*args):
    route = 'motherboards'
    return get_all_products(route, *args)


def search_cheapest_psu(*args):
    route = 'power-supplies'
    return get_all_products(route, *args)


def search_cheapest_psu(*args):
    route = 'power-supplies'
    return get_all_products(route, *args)


def search_cheapest_storage(*args):
    route = 'storage-devices'
    return get_all_products(route, *args)


def search_cheapest_ram(*args):
    route = 'memories'
    return get_all_products(route, *args)


def search_cheapest_cpu_cooler(*args):
    route = 'cpu-coolers'
    return get_all_products(route, *args)


def search_cheapest_case(*args):
    route = 'cases'
    return get_all_products(route, *args)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    build = []


    #DEFINIR PARAMETROS DA BUILD, O PROGRAMA BUSCA EM TODOS OS REGISTROS O MAIS BARATO QUE CONTENHA NA DESCRICAO AS STRINGS

    build.append(search_cheapest_video_card('3070'))
    build.append(search_cheapest_processor('12700'))
    build.append(search_cheapest_monitor('4K', '32'))
    build.append(search_cheapest_motherboard('B660'))
    build.append(search_cheapest_psu('850W', 'Gold'))
    build.append(search_cheapest_storage('SN350 1 TB'))
    build.append(search_cheapest_ram('DDR4-3200 CL16', '2 x 16 GB'))
    build.append(search_cheapest_cpu_cooler('Hyper 212'))
    build.append(search_cheapest_case('HX100'))









    total_avista = 0
    total_parcelado = 0
    buildresult = ""
    buildresult += '\n\n'
    buildresult += '\n--------------------------------------------'
    for index, item in enumerate(build):
        total_avista += item.avista
        total_parcelado += item.parcelado
        buildresult += f'\n{index + 1} - {item.descricao} - {item.loja} - R$ {item.avista}'
    buildresult += '\n--------------------------------------------'
    buildresult += f'\nTOTAL: R${total_avista}'
    buildresult += f'\nPARCELADO: R${total_parcelado}'
    cur = con.cursor()
    data = [
        (None, buildresult, str(total_avista), str(datetime.datetime.now()))
    ]
    cur.execute('INSERT INTO build(id, description, price, data) VALUES(?,?,?,?)', data[0])
    con.commit()
    print(buildresult)

    query = "select price, data from build;"
    df = pd.read_sql_query(query, con)
    df["data"] = pd.to_datetime(df["data"])
    df["price"] = df["price"].astype(float)
    date = df["data"]
    price = df["price"]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(date, price)
    plt.show()