import threading

def set_interval(func, sec, args=None, daemon=False):
  def func_wrapper():
    set_interval(func, sec, args)
    func()
  t = threading.Timer(sec, func_wrapper)
  if daemon:
    t.setDaemon(True)
  t.start()
  return t