from app import app
app.jinja_env.auto_reload = True
app.run(host='0.0.0.0', debug=True)
