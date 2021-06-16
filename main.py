from tsync.tsync import TSync,Pipeline

@TSync.bind(name='alice',flow=['bob','minister'])
def alice(pipe:Pipeline):
    half_word=pipe.read(_from='minister').decode()
    half_word+=" John"
    pipe.write(_to='minister', data=half_word.encode())

@TSync.bind(name='bob',flow=['alice','minister'])
def bob(pipe:Pipeline):
    half_word=pipe.read(_from='minister').decode()
    half_word+=" Doe"
    pipe.write(_to='minister',data=half_word.encode())

@TSync.bind(name='minister',flow=['bob','alice'])
def minister(pipe:Pipeline):
    pipe.write(_to='alice',data=b'Aesop')
    pipe.write(_to='bob',data=b'was')
    print("From Alice:",pipe.read(_from='alice'))
    print("From Bob:",pipe.read(_from='bob'))

TSync.prepare_thread_default()
TSync.fire_threads()
TSync.join_threads()

print(TSync.get_pumps())
