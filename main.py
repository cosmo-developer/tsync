from tsync.tsync import TSync,Pipeline
sync=TSync()
'''A chat between two threads alice and bob'''
@sync.bind(name='alice',flow=['bob'])
def alice(pipe:Pipeline):
    print('From Other',pipe.read('other'))
    pipe.write('bob',b'Hello How are you?')
    print("From bob:",pipe.read('bob').decode())
    pipe.write('bob',b'I am also fine!')
    print("From bob:",pipe.read('bob').decode())
    pipe.write('bob',b'Good Bye')

@sync.bind(name='bob',flow=['alice'])
def bob(pipe:Pipeline):
    print('From Other', pipe.read('other'))
    print("From Alice:",pipe.read('alice').decode())
    pipe.write('alice',b'I am fine! and You?')
    print("From Alice:",pipe.read('alice').decode())
    pipe.write('alice',b'Good Bye')
    print("From Alice:",pipe.read('alice').decode())
@sync.bind(name='other',flow=['alice','bob'])
def other(pipe:Pipeline,some):
    pipe.write('alice',some)
    pipe.write('bob',some)

sync.prepare_thread_default(excepts=['other'])
sync.prepare_thread('other',args=[b'Hi!'])
sync.fire_threads()
sync.join_threads()
print(sync.get_pumps())