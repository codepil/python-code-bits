
# Why Python
At startup, in idea phase, one has some sense of destination and direction but does not know exactly what to build. That clarity emerges only through iterations and experimentations. We were no different, so we had to pick a programming language and microservice framework suitable for rapid prototyping. These were our key considerations:

Rapid Development: high velocity of experimentations for quick implementation and evaluation of ideas.
Performance: lightweight yet mature microservice framework, efficient for mostly IO-bound application, scales to high throughput for concurrent requests.
Tools Infrastructure: for automated testing, cloud deployment, monitoring.
Machine Learning (ML): easy availability of libraries and frameworks.
Hiring: access to talent and expertise.
There is no perfect choice for the programming language that ticks all of the above. It finally boils down to Python vs. Java/Scala because these are the only feasible languages for machine learning work. While Java has better performance and tooling, Python is apt for rapid prototyping. At that stage, we favoured rapid development and machine learning over other considerations, therefore picked Python.

# microservice
Microservice architecture facilitates each service to independently choose the programming language and framework, and there is no need to standardize on one. However, a heterogeneous system adds DevOps and infra overheads, which we wanted to avoid as we were just a couple of guys hacking the system. With time, our team and platform grew and now has microservices in Go-lang and JavaScript too.

With Python, came its infamous Global Interpreter Lock. In brief, a thread can execute only if it has acquired the Python interpreter lock. Since it is a global lock, only one thread of the program can acquire it and therefore run at a time, even if the hardware has multiple CPUs. It effectively renders Python programs limited to single-threaded performance.

While GIL is a serious limitation for CPU-bound concurrent Python apps, for IO-bound apps, cooperative multitasking of AsyncIO offers good performance (more about it later). For performance, we desired a web framework which is lightweight yet mature, and has AsyncIO APIs.

We evaluated three Python Web Frameworks: Django, Flask, and Tornado.

Django follows “batteries included” approach, it has everything you will need and more. While that eliminates integration compatibility blues, it also makes it bulky. It does not have AsyncIO APIs.
Flask, on the other hand, is super lightweight and has a simple way of defining service endpoints through annotation. It does not have AsyncIO APIs.
Tornado is somewhere between Django and Flask, it is neither as barebone as Flask nor as heavy as Django. It has quite a number of configurations, hooks, and nice testing framework. It had been having event-loop for scheduling cooperative tasks for much before AsyncIO, and had started supporting AsyncIO event loop and syntax.

# device-logging
Writeup pending .. it's a standalone program

# first-steps
Get started with Python coding &amp; best practices

Get the latest version from https://www.python.org/downloads/ & install the python shell. Btw which version to get ? there was a significant update to Python several years ago that created a big split between Python versions. So you have to choose either Python 2 or Python 3 latest version

If you have choosen to install Python 3 then default installation happens at C:\Users\[username]\AppData\Local\Programs\Python\Python36 

Next step is install IDE from https://www.jetbrains.com/pycharm/, its my choice of IDE btw.

Btw you can still learm without local installation of python, from www.learnpython.org


what is pythonic, once you learned the basics of langaguge, refer to https://www.youtube.com/playlist?list=PLTq2xnd7xp--L5E6B_BNiyzrtGs5FwCCa

Other nice references
http://book.pythontips.com/en/latest/index.html 
