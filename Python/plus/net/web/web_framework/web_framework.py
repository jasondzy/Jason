

class Application(object):

    def __init__(self,urls):
        self.urls = urls

    # define a callable function, so the class can be called
    def __call__(self, environ, start_response):
        return self.application(environ, start_response)


    # define a functon , this function is standard for wsgi interface
    def application(self,environ, start_response):

        header= ''''''

        start_response('HTTP/1.1 200 ok',header)

        path = environ.get('PATH', '/')

        for name, handler in self.urls:
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


urls = [
    ('./index.html', handle_index),
    ('./index11.html', handle_index11)

]

app = Application(urls)

