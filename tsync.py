from threading import Thread

class Pipeline:
    def __init__(self,name):
        self.__name=name
    def write(self,_to,data=b''):
        TSync.write(self.__name,_to,data)
    def read(self,_from):
        return TSync.read(self.__name,_from)
class Buffer:
    def __init__(self):
        self.data=b''
        self.w_lock=False #Write lock
        self.r_lock=True # Read lock

class TSync:
    _thread_functions={}
    _data_flow_pumps={}
    _thread_list=[]
    @staticmethod
    def bind(name,flow:list):
        def internal_bind(z):
            TSync._thread_functions.update({name:z})
            for flow_dir in flow:
                TSync._data_flow_pumps.update({'->'.join([name,flow_dir]):Buffer()})
        return internal_bind
    @staticmethod
    def get_all_functions():
        return TSync._thread_functions
    @staticmethod
    def prepare_thread(name,args=[]):
        args.reverse()
        args.append(Pipeline(name))
        args.reverse()
        t:Thread=Thread(target=TSync._thread_functions[name],args=tuple(args))
        TSync._thread_list.append(t)
    @staticmethod
    def fire_threads():
        for t in TSync._thread_list:
            t.start()
    @staticmethod
    def join_threads():
        for t in TSync._thread_list:
            t.join()
    @staticmethod
    def get_pumps():
        return TSync._data_flow_pumps
    @staticmethod
    def read(name:str,other:str):
        while TSync._data_flow_pumps['->'.join([other,name])].r_lock:
            pass
        TSync._data_flow_pumps['->'.join([other,name])].r_lock=True
        TSync._data_flow_pumps['->'.join([other,name])].w_lock=False
        return TSync._data_flow_pumps['->'.join([other,name])].data
    @staticmethod
    def write(name:str,other:str,data=b''):
        while TSync._data_flow_pumps['->'.join([name,other])].w_lock:
            pass
        TSync._data_flow_pumps['->'.join([name,other])].r_lock = False
        TSync._data_flow_pumps['->'.join([name,other])].w_lock = True
        TSync._data_flow_pumps['->'.join([name,other])].data=data
    @staticmethod
    def prepare_thread_default():
        for name in TSync._thread_functions:
            TSync.prepare_thread(name,[])