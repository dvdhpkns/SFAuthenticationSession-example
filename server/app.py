from flask import Flask, request, jsonify, redirect
from haikunator import Haikunator
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return 'Simple flask app to create and get cookies. Can redirect to a callbackUrl to deep link into app.' \
           '<br><br>Example using cookie "user" - replace with any cookie of your choice:' \
           + get_endpoints_description("user")


@app.route('/create-cookie/<cookie_key>')
def set_cookie(cookie_key):
    cookie_val = Haikunator().haikunate()
    rsp_text = 'Cookie "' + cookie_key + '" set to <b>' + cookie_val + '</b>'
    rsp_text += get_endpoints_description(cookie_key)
    response = app.make_response(rsp_text)
    # set the cookie with an expirty date / "max-age" / "expires" param per this SO answer
    # https://stackoverflow.com/questions/46569570/sfauthenticationsession-isnt-sharing-cookies-on-the-real-devices
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=90)
    response.set_cookie(cookie_key, value=cookie_val, expires=expire_date)
    return response


@app.route('/delete-cookie/<cookie_key>')
def delete_cookie(cookie_key):
    rsp_text = 'Cookie "' + cookie_key + '" removed'
    rsp_text += get_endpoints_description(cookie_key)
    response = app.make_response(rsp_text)
    response.set_cookie(cookie_key, '', expires=0)
    return response


@app.route('/get-cookie/<cookie_key>')
def get_cookie(cookie_key):
    cookie_val = request.cookies.get(cookie_key, None)
    callback_url = request.args.get("callbackUrl", None)
    if callback_url:
        redirect_url = callback_url + "?" + cookie_key + "=" + str(cookie_val)
        print "Redirecting to:"
        print redirect_url
        return redirect(redirect_url)
    else:
        rsp_text = 'Cookie "' + cookie_key + '" is ' + ('<b>' + cookie_val + '</b>' if cookie_val else 'not set')
        rsp_text += get_endpoints_description(cookie_key)
        return rsp_text


def get_endpoints_description(key):
    create_text = '<a href="/create-cookie/' + key + '">/create-cookie/' + key + '</a>'
    create_text += ' - sets random cookie val for "' + key + '"'
    get_text = '<a href="/get-cookie/' + key + '">/get-cookie/' + key + '</a>'
    get_text += ' - gets cookie val for "' + key + '" with optional query param "callbackUrl" to be redirected to with cookie appended as query param'
    delete_text = '<a href="/delete-cookie/' + key + '">/delete-cookie/' + key + '</a>'
    delete_text += ' - expires cookie for "' + key + '"'
    print_cookies = '<script>document.getElementsByTagName("p")[0].append(document.createElement("div").innerHTML = document.cookie)</script>'
    return '<ul><li>' + create_text + '</li><li>' + get_text + '</li><li>' + delete_text + '</li></ul><h3>Current cookies set are:</h3><p>' + print_cookies + '</p>'

if __name__ == '__main__':
    app.run(host="0.0.0.0")
