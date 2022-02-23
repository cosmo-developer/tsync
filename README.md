
# [TSync](https://github.com/cosmo-developer/tsync.git)

A Thread Synchronization API built for python. This allow Intercommunication between Threads via special Name.

## Usage/Examples

```python
from tsync.tsync import TSync,Pipeline
sync=TSync()
'''A chat between two threads alice and bob'''

'''
 @flow argument list of thread name (Helps to connect to them)
'''

#Alice can connect to bob
@sync.bind(name='alice',flow=['bob'])
def alice(pipe:Pipeline):
    print('From Other',pipe.read('other'))
    pipe.write('bob',b'Hello How are you?')
    print("From bob:",pipe.read('bob').decode())
    pipe.write('bob',b'I am also fine!')
    print("From bob:",pipe.read('bob').decode())
    pipe.write('bob',b'Good Bye')

#And Bob can connect to alice 
@sync.bind(name='bob',flow=['alice'])
def bob(pipe:Pipeline):
    print('From Other', pipe.read('other'))
    print("From Alice:",pipe.read('alice').decode())
    pipe.write('alice',b'I am fine! and You?')
    print("From Alice:",pipe.read('alice').decode())
    pipe.write('alice',b'Good Bye')
    print("From Alice:",pipe.read('alice').decode())

#This is for test purpose this connected with both alice and bob
@sync.bind(name='other',flow=['alice','bob'])
def other(pipe:Pipeline,some):
    pipe.write('alice',some)
    pipe.write('bob',some)

#Prepare all threads by default parameteres except other function
sync.prepare_thread_default(excepts=['other'])
#Prepare other function with argument b'Hi!'
sync.prepare_thread('other',args=[b'Hi!'])
#Start all threads 
sync.fire_threads()
#Wait to join each threads
sync.join_threads()
#Return the communication line between threads
print(sync.get_pumps())
```


## 🚀 About Me
I'm a Software Developer devloping open source software on Github.
