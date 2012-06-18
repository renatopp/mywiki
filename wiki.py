import os
from lib import markup
from lib import db
import flask
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

#configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

#==============================================================================
# VIEWS
#==============================================================================

# INDEX -----------------------------------------------------------------------
@app.route('/')
def index():
    return flask.redirect(url_for('list'))
# -----------------------------------------------------------------------------

# LIST ------------------------------------------------------------------------
@app.route('/list/', defaults={'path': ''})
@app.route('/list/<path:path>')
def list(path):
    config = db.load_config()
    resource = db.Resource(config['source_dir'], path)

    if not resource.is_dir(): abort(404)

    return render_template('index.jinja2', resource=resource)
# -----------------------------------------------------------------------------

# VIEW ------------------------------------------------------------------------
@app.route('/view/', defaults={'path': ''})
@app.route('/view/<path:path>')
def view(path):
    config = db.load_config()
    resource = db.Resource(config['source_dir'], path)

    if not resource.is_file(): abort(404)

    filter = markup.markup_by_filename(resource.cur_file)
    content = filter.render(db.load_file(resource.os_path))

    return render_template('view.jinja2', content=content, resource=resource)
# -----------------------------------------------------------------------------

# EDIT ------------------------------------------------------------------------
@app.route('/edit/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/edit/<path:path>', methods=['GET', 'POST'])
def edit(path):
    if request.args.get('f') == 'config':
        config = db.load_config()
        return_resource = db.Resource(config['source_dir'], path)
        return_path = return_resource.path

        resource = db.Resource(move_path=db.CONFIG)
        internal = True
    else:
        config = db.load_config()
        resource = db.Resource(config['source_dir'], path)
        return_path = resource.path
        return_resource = resource
        internal = False

    if not resource.is_file(): abort(404)

    if request.form:
        db.save_file(resource.os_path, request.form['content'])
        if internal:
            if return_resource.is_file():
                return flask.redirect(url_for('view', path=return_resource.path))
            else:
                return flask.redirect(url_for('list', path=return_resource.path))
        else:
            return flask.redirect(url_for('view', path=resource.path))

    content = db.load_file(resource.os_path)
    return render_template('edit.jinja2',
        return_path=return_path,
        return_resource=return_resource,
        content=content,
        resource=resource,
        internal=internal
    )
# -----------------------------------------------------------------------------

# ERROR -----------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.jinja2',
        error_title='404 Page Not Found',
        error_content='Sorry!'
    ), 404
# -----------------------------------------------------------------------------

# AJAX ------------------------------------------------------------------------
@app.route('/_create_folder')
def _create_folder():
    result = 'ok'
    motive = ''

    name = request.args.get('name', '')
    path = request.args.get('path', '')

    if not name:
        result = 'error'
        motive = 'Must set a name for the new folder'
    else:
        config = db.load_config()
        resource = db.Resource(config['source_dir'], path)
        resource.move(name)

        try:
            os.mkdir(resource.os_path)
        except Exception as e:
            result = 'error'
            motive = e.message
    
    return jsonify(result=result, motive=motive)

@app.route('/_rename_folder')
def _rename_folder():
    result = 'ok'
    motive = ''

    old_name = request.args.get('old_name', '')
    new_name = request.args.get('new_name', '')
    path = request.args.get('path', '')

    if not new_name:
        result = 'error'
        motive = 'Must set a new name for the folder'
    else:
        config = db.load_config()
        resource = db.Resource(config['source_dir'], path)

        try:
            os.rename(resource.os_join(old_name), resource.os_join(new_name))
        except Exception as e:
            result = 'error'
            motive = e.message
    
    return jsonify(result=result, motive=motive)

@app.route('/_remove_folder')
def _remove_folder():
    result = 'ok'
    motive = ''

    name = request.args.get('name', '')
    path = request.args.get('path', '')
    config = db.load_config()
    resource = db.Resource(config['source_dir'], path)

    try:
        import shutil
        shutil.rmtree(resource.os_join(name))
    except Exception as e:
        result = 'error'
        motive = e.message

    return jsonify(result=result, motive=motive)

@app.route('/_create_file')
def _create_file():
    result = 'ok'
    motive = ''

    name = request.args.get('name', '')
    path = request.args.get('path', '')

    if not name:
        result = 'error'
        motive = 'Must set a name for the new document'
    else:
        config = db.load_config()
        resource = db.Resource(config['source_dir'], path)
        resource.move(name)

        try:
            db.save_file(resource.os_path, '')
        except Exception as e:
            result = 'error'
            motive = e.message
    
    return jsonify(result=result, motive=motive)

@app.route('/_rename_file')
def _rename_file():
    result = 'ok'
    motive = ''

    old_name = request.args.get('old_name', '')
    new_name = request.args.get('new_name', '')
    path = request.args.get('path', '')

    if not new_name:
        result = 'error'
        motive = 'Must set a new name for the folder'
    else:
        config = db.load_config()
        resource = db.Resource(config['source_dir'], path)

        try:
            os.rename(resource.os_join(old_name), resource.os_join(new_name))
        except Exception as e:
            result = 'error'
            motive = e.message
    
    return jsonify(result=result, motive=motive)

@app.route('/_remove_file')
def _remove_file():
    result = 'ok'
    motive = ''

    name = request.args.get('name', '')
    path = request.args.get('path', '')
    config = db.load_config()
    resource = db.Resource(config['source_dir'], path)

    try:
        os.remove(resource.os_join(name))
    except Exception as e:
        result = 'error'
        motive = e.message

    return jsonify(result=result, motive=motive)

@app.route('/_open_folder')
def _open_folder():
    name = request.args.get('name', '.')
    path = request.args.get('path', '')
    config = db.load_config()
    resource = db.Resource(config['source_dir'], path)
    resource.move(name)

    import subprocess
    subprocess.Popen('explorer /root, "%s"'%resource.os_path)

    return jsonify()

@app.route('/_open_file')
def _open_folder():
    name = request.args.get('name', '.')
    path = request.args.get('path', '')
    config = db.load_config()
    resource = db.Resource(config['source_dir'], path)
    resource.move(name)

    os.startfile(resource.os_path)

    return jsonify()
# -----------------------------------------------------------------------------


#==============================================================================
# UTILS
#==============================================================================

@app.template_filter('css')
def css(s):
    mask = '<link rel="stylesheet" type="text/css" href="%s">'
    url = flask.url_for('static', filename='css/'+s)
    return mask%url

@app.template_filter('js')
def js(s):
    mask = '<script src="%s"></script>'
    url = flask.url_for('static', filename='js/'+s)
    return mask%url

@app.template_filter('static')
def static(s):
    mask = '%s'
    url = flask.url_for('static', filename=s)
    return mask%url


if __name__ == '__main__':
    app.run()
