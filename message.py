class Message:
    def __init__(header, body ):
        if header is None:
            header = ''
        if body is None:
            body = ''
        self.header = header
        self.body = body
    
    def displayMessagetext():
        print('header is', header)
        print('body is ', body)
    