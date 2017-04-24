


"""MOVED TO ./app/views.py
@app.route('/')
def index():
   
    return app.send_static_file('index.html')
    
@app.route('/api/user/register', methods=['POST'])
def signup():
    
    
@app.route('/api/user/login', methods=["POST"])
def login():
    
    
@app.route('/api/user/logout',methods=["POST"])
def logout():
    
    
@app.route('/api/user/<userid>/wishlist',methods=["GET","POST"])
def wishes(userid):
    
    
@app.route('/api/thumbnail', methods=['GET'])
def get_images():
    """