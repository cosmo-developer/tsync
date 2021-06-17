from threading import Thread

class Pipeline:
    def __init__(self,name,syncer):
        self.__name=name
        self.__tsync:TSync=syncer
    def write(self,_to,data=b''):
        self.__tsync.write(self.__name,_to,data)
    def read(self,_from):
        return self.__tsync.read(self.__name,_from)
class Buffer:
    def __init__(self):
        self.data=b''
        self.w_lock=False #Write lock
        self.r_lock=True # Read lock
    def __repr__(self):
        return str((self.data,self.r_lock,self.w_lock))

class TSync:
    def __init__(self):
        self._thread_functions = {}
        self._data_flow_pumps = {}
        self._thread_list = []

    def bind(self,name,flow:list):
        def internal_bind(z):
            self._thread_functions.update({name:z})
            for flow_dir in flow:
                self._data_flow_pumps.update({'->'.join([name,flow_dir]):Buffer()})
        return internal_bind
    def get_all_functions(self):
        return self._thread_functions
    def prepare_thread(self,name,args=[]):
        args.reverse()
        args.append(Pipeline(name,self))
        args.reverse()
        t:Thread=Thread(target=self._thread_functions[name],args=tuple(args))
        self._thread_list.append(t)
    def fire_threads(self):
        for t in self._thread_list:
            t.start()
    def join_threads(self):
        for t in self._thread_list:
            t.join()
    def get_pumps(self):
        return self._data_flow_pumps
    def read(self,name:str,other:str):
        while self._data_flow_pumps['->'.join([other,name])].r_lock:
            pass
        self._data_flow_pumps['->'.join([other,name])].r_lock=True
        self._data_flow_pumps['->'.join([other,name])].w_lock=False
        return self._data_flow_pumps['->'.join([other,name])].data
    def write(self,name:str,other:str,data=b''):
        while self._data_flow_pumps['->'.join([name,other])].w_lock:
            pass
        self._data_flow_pumps['->'.join([name,other])].r_lock = False
        self._data_flow_pumps['->'.join([name,other])].w_lock = True
        self._data_flow_pumps['->'.join([name,other])].data=data
    def prepare_thread_default(self,excepts=[]):
        for name in self._thread_functions:
            if name not in excepts:
                self.prepare_thread(name,[])