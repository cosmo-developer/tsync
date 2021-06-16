from tsync.tsync import TSync,Pipeline
sync=TSync()
'''A chat between two threads alice and bob'''
@sync.bind(name='alice',flow=['bob'])
def alice(pipe:Pipeline):
    pipe.write('bob',b'Hello How are you?')
    print("From bob:",pipe.read('bob').decode())
    pipe.write('bob',b'I am also fine!')
    print("From bob:",pipe.read('bob').decode())
    pipe.write('bob',b'Good Bye')

@sync.bind(name='bob',flow=['alice'])
def bob(pipe:Pipeline):
    print("From Alice:",pipe.read('alice').decode())
    pipe.write('alice',b'I am fine! and You?')
    print("From Alice:",pipe.read('alice').decode())
    pipe.write('alice',b'Good Bye')
    print("From Alice:",pipe.read('alice').decode())


sync.prepare_thread_default()
sync.fire_threads()
sync.join_threads()
print(sync.get_pumps())