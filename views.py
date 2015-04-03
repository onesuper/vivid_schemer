from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.utils import simplejson

import scheme.universe as u
#import scheme.highlighter as h
from scheme.parser import parse
from scheme.eval import eval, add_globals
from scheme.utils import to_string
from scheme.env import Env

def talk(request):
    
    if request.method == 'POST':
        if request.POST.get('code', ''):
            code = request.POST['code']
            result = ""
            u.hole = []
            try:
                val = eval(parse(code), add_globals(Env()))
                if val is not None: result = to_string(val)
                else: result = "NIL"
            except AttributeError:
                result = "invalid sentence"
            except ValueError, e:
                result = "invalid sentence"
            except TypeError, e:
                result = "invalid sentence"
            except IndexError:
                result = "check the parentheses"
            except ZeroDivisionError:
                result = "divide zero"

            t = get_template('output.html')
            js_output = simplejson.dumps(u.hole)

            html = t.render(Context({'output': js_output, 'result': result, "code": code}))
            return HttpResponse(html)
        else:
            return HttpResponse("The answer is blowin' in the wind...")




def embed(request):
    
    if request.method == 'GET':
        if request.GET.get('code', ''):
            
            code = request.GET['code']
            result = ""
            u.hole = []
            try:
                val = eval(parse(code), add_globals(Env())) # new env each time
                if val is not None: result = to_string(val)
                else: result = "NIL"
            except AttributeError:
                result = "invalid sentence"
            except ValueError, e:
                result = "invalid sentence"
            except TypeError, e:
                result = "invalid sentence"
            except IndexError:
                result = "check the parentheses"
            except ZeroDivisionError:
                result = "divide zero"

            t = get_template('embed.html')
            js_output = simplejson.dumps(u.hole)

            html = t.render(Context({'output': js_output, 'result': result, "code": code}))
            return HttpResponse(html)
        else:
            return HttpResponse("The answer is blowin' in the wind...")
