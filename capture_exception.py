import traceback
def function1():
    raise RuntimeError('xxx')
def function2():
    function1()
def function3():
    try:
      function2()
    except Exception:
      traceback.print_exc() #captures exception
      print ("hi.....")
      traceback.print_stack()
def function4():
    function3()
def function5():
    function4()
function5()