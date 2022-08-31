from snorrenapp import app
import os


if __name__ == '__main__':
    from waitress import serve
    port = int(os.environ.get('PORT', 5000))
    serve(app, host="0.0.0.0", port=port)
    # app.run(debug=True, host='0.0.0.0', port=port)
