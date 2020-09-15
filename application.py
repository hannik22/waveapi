# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify
from flask_caching import Cache
from wavedata import wavedata
import json

cache = Cache()
#Shops
chishops = [{"id": 0, "name": "Lake Effect", "city": "Shorewood, WI", "url": "https://www.lakeeffectsurfshop.com/"},{"id": 1, "name": "Third Coast", "city": "New Buffalo, MI", "url": "https://www.thirdcoastsurfshop.com/"}]
mkeshops = [{"id": 0, "name": "Lake Effect", "city": "Shorewood, WI", "url": "https://www.lakeeffectsurfshop.com/"}, {"id": 1, "name": "EOS", "city": "Sheboygan, WI", "url": "https://eossurf.com/"}]
shebshops = [{"id": 0, "name": "EOS", "city": "Sheboygan, WI", "https://eossurf.com/": "True"}, {"id": 1, "name": "Lake Effect", "city": "Shorewood, WI", "url": "https://www.lakeeffectsurfshop.com/"}]
stjshops = [{"id": 0, "name": "Third Coast", "city": "Saint Joseph, MI", "url": "https://www.lakeeffectsurfshop.com/"}]
micityshops = [{"id": 0, "name": "Third Coast", "city": "New Buffalo", "url": "https://www.lakeeffectsurfshop.com/"}, {"id": 1, "name": "Third Coast", "city": "Saint Joseph", "url": "https://www.lakeeffectsurfshop.com/"}] 

def create_app():
    application = app = Flask(__name__)

    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    app.config['CACHE_TYPE'] = 'simple'

    cache.init_app(app)

    @app.route('/')
    @cache.cached(timeout=1200)
    def home():
        return jsonify({"Hello World": "Hello"})

    @app.route('/Chicago')
    @cache.cached(timeout=1200)
    def chicago():
        waves = wavedata('https://api.weather.gov/gridpoints/LOT/76,76',
                             'https://api.weather.gov/gridpoints/LOT/73,80', 'https://api.weather.gov/gridpoints/LOT/74,77')
        return jsonify({"city": "Chicago, IL", "properties": waves, "shops": chishops})

    @app.route('/Milwaukee')
    @cache.cached(timeout=1200)
    def milwaukee():
            waves = wavedata('https://api.weather.gov/gridpoints/MKX/88,68',
                            'https://api.weather.gov/gridpoints/MKX/93,54', 'https://api.weather.gov/gridpoints/MKX/88,72')
            return jsonify({"city": "Milwaukee, WI", "properties": waves, "shops": mkeshops})

    @app.route('/Sheboygan')
    @cache.cached(timeout=1200)
    def sheboygan():
            waves = wavedata('https://api.weather.gov/gridpoints/MKX/93,96',
                            'https://api.weather.gov/gridpoints/MKX/93,98', 'https://api.weather.gov/gridpoints/MKX/93,98')
            return jsonify({"city": "Sheboygan, WI", "properties": waves, "shops": shebshops})

    @app.route('/MichiganCity')
    @cache.cached(timeout=1200)
    def micity():
            waves = wavedata('https://api.weather.gov/gridpoints/IWX/6,63',
                            'https://api.weather.gov/gridpoints/LOT/99,66', 'https://api.weather.gov/gridpoints/IWX/7,64')
            return jsonify({"city": "Michigan City, IN", "properties": waves, "shops": micityshops})

    @app.route('/SaintJoseph')
    @cache.cached(timeout=1200)
    def stjoe():
            waves = wavedata('https://api.weather.gov/gridpoints/GRR/15,6',
                            'https://api.weather.gov/gridpoints/IWX/18,80', 'https://api.weather.gov/gridpoints/IWX/18,79')
            return jsonify({"city": "Saint Joseph, MI", "properties": waves, "shops": stjshops})

    return app

