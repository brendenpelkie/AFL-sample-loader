from flask import Flask, render_template
from flask import request, jsonify, Markup

import datetime,requests, subprocess,shlex,os

#app = Flask('NistoRoboto') #okay this breaks the templating apparently
app = Flask(__name__)
app.config['ENV'] = 'development'
experiment = 'Development'
contactinfo = 'tbm@nist.gov'
# app.config['ENV'] = 'production'

# initialize auth module
from flask_jwt_extended import JWTManager, jwt_required 
from flask_jwt_extended import create_access_token, get_jwt_identity
app.config['JWT_SECRET_KEY'] = '03570' #hide the secret?
jwt = JWTManager(app)

import logging
app.logger.setLevel(level=logging.DEBUG)


# this is necessary to use the default debug reloading functionality 
if app.config['ENV']=='production' or os.environ.get("WERKZEUG_RUN_MAIN") =='true':
    import queue
    task_queue = queue.Queue()
    
    import opentrons
    from NistoRoboto.OT2App.OT2Daemon import OT2Daemon
    OT2_daemon = OT2Daemon(app,task_queue,debug_mode=True)
    OT2_daemon.start()# start server thread

@app.route('/')
def index():
    '''Live, status page of the robot'''
    kw = status_dict()

    response = requests.post('http://localhost:5000/update_img')
    print(response.status_code,response.content)

    return render_template('index.html',**kw),200

@app.route('/ajax_test')
def ajax_index():
    '''Live, status page of the robot'''
    kw = status_dict()

    #request image and save to static directory

    # TO SET UP STREAM IN FUTURE:
    # ffmpeg -y -f video4linux2 -s 640x480 -i /dev/video0 'udp://239.0.0.1:1234?ttl=2'

    # this will UDP multicast stream to 239.0.0.1:1234, pick this stream up on control server and repackage it.
    
    response = requests.post('http://localhost:31950/camera/picture')
    with open('static/deck.jpeg','wb') as f:
        f.write(response.content)

    return render_template('index-ajax.html',**kw),200


def _nbsp(instr):
    return Markup(instr.replace(' ','&nbsp;'))

def status_dict():
    kw = {}
    kw['pipettes'] = OT2_daemon.protocol.protocol.loaded_instruments
    kw['labware']  = OT2_daemon.protocol.protocol.loaded_labwares
    kw['statuscolor'] = OT2_daemon.doorDaemon.button_color
    kw['updatetime'] = _nbsp(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    kw['robotstatus']      = _nbsp(_queue_status(task_queue))
    kw['currentexperiment'] = _nbsp(experiment)
    kw['contactinfo']       = _nbsp(contactinfo)
    if OT2_daemon.debug_mode:
        kw['queuemode'] = 'DEBUG'
    else:
        kw['queuemode'] = 'ACTIVE'

    queue_str  = '<ol id="queue">\n'
    for task in task_queue.queue:
        queue_str  += f'\t<li>{task}</li>\n'
    queue_str  += '</ol>\n'
    kw['queue'] = Markup(queue_str)

    return kw

def _nbsp(instr):
    return Markup(instr.replace(' ','&nbsp;'))

@app.route('/ajax-data')
def ajax_data():
    kw = status_dict()
    return jsonify(status_dict),200

@app.route('/update_img',methods=['POST'])
def update_img():
    #copy new take img code from above here once pushed from NR.
    # TO SET UP STREAM IN FUTURE:
    # ffmpeg -y -f video4linux2 -s 640x480 -i /dev/video0 'udp://239.0.0.1:1234?ttl=2'
    # this will UDP multicast stream to 239.0.0.1:1234, pick this stream up on
    # control server and repackage it.

    subprocess.Popen(
            shlex.split(
                'ffmpeg -y -f video4linux2 -s 640x480 -i /dev/video0 -ss 0:0:0.01 -frames 1 static/deck.jpeg'
                ),
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
            )
    return 'Success',200

@app.route('/login',methods=['GET','POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if password != 'domo_arigato':
        return jsonify({"msg": "Bad password"}), 401

    experiment = request.json.get('experiment',experiment)
    contactinfo = request.json.get('contactinfo',contactinfo)

    # Identity can be any data that is json serializable
    #expires = datetime.timedelta(days=1)
    app.logger.info(f'Creating login token for user {username}')
    token = create_access_token(identity=username)#,expires=expires)
    return jsonify(token=token), 200

def _queue_status(q):
    if q.empty():
        return "Idle"
    else:
        return f"Running, {q.qsize()} pending tasks."

@app.route('/enqueue',methods=['POST'])
@jwt_required
def enqueue():
    task_queue.put(request.json)
    return 'Success',200

@app.route('/clear_queue',methods=['POST'])
def clear_queue():
    app.logger.info(f'Removing all items from OT-2 queue')
    task_queue.queue.clear()
    return 'Success',200

@app.route('/halt',methods=['POST'])
def halt():
    opentrons.robot.halt()
    return 'Success',200

@app.route('/login_test',methods=['POST'])
@jwt_required
def login_test():
    username = get_jwt_identity()
    app.logger.info(f'Login test for {username} successful')
    return 'Success',200

if __name__ == '__main__':
    if app.config['ENV'] == 'development':
        debug = True
    else:
        debug = False
    app.run(host='0.0.0.0',debug=debug)

