import io

import logging

from logging import FileHandler, Formatter

from flask import Flask, Response, render_template, request

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from windrouter.gfs import download_latest_gfs
from windrouter.map import add_barbs, add_route, create_map


# App Config.
app = Flask(__name__)
app.config.from_object('config')


# Controllers.
@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/map')
def plot_map():
    try:
        lat1 = request.args['lat1']
        lon1 = request.args['lon1']
        lat2 = request.args['lat2']
        lon2 = request.args['lon2']
    except (KeyError):
        lat1, lon1, lat2, lon2 = app.config['DEFAULT_MAP']
        dpi = app.config['DPI']
        logging.log(logging.WARNING, 'using default coordinates')

    try:
        lat1 = float(lat1)
        lat2 = float(lat2)
        lon1 = float(lon1)
        lon2 = float(lon2)
    except (ValueError):
        logging.log(logging.ERROR, 'expecting real values')
    # generate map
    fig = create_map(lat1, lon1, lat2, lon2, dpi)

    # plot weather
    try:
        latest = request.args['latest']
    except KeyError:
        latest = False

    if latest:
        weather_file = download_latest_gfs(0)
    else:
        weather_file = app.config['DEFAULT_GFS_FILE']

    fig = add_barbs(fig, weather_file, lat1, lon1, lat2, lon2)

    # plot route
    r_la1, r_lo1, r_la2, r_lo2 = app.config['DEFAULT_ROUTE']
    fig = add_route(fig, r_la1, r_lo1, r_la2, r_lo2)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    # Write the file as well
    with open('screenshots/map.png', 'wb') as f:
        f.write(output.getbuffer())

    return Response(output.getvalue(), mimetype='image/png')


# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
