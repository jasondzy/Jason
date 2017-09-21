

# define a functon , this function is standard for wsgi interface
def application(environ, start_response):

    header= ''''''

    urls = [
        ('./index.html', handle_index),
        ('./index11.html', handle_index11)

    ]
    
    start_response('HTTP/1.1 200 ok',header)

    path = environ.get('PATH', '/')

    for name, handler in urls:
        if name == path:
            return handler()

    start_response('HTTP/1.1 404 not found',header)
    return '404 not found'

def handle_index():

    fp = open('./index.html', 'r')
    file_data = fp.read()
    fp.close()

    return file_data

def handle_index11():
    fp = open('./index11.html', 'r')
    file_data = fp.read()
    fp.close()

    return file_data

