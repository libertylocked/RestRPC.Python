import websocket
import json
from time import gmtime, strftime
from base64 import b64encode

rpc_dict = {}


def new_rrpc_ws(component_name, uri, username, password, procedures):
    global rpc_dict
    rpc_dict = procedures
    # Add pluginlist to procedures (it's a default procedure)
    rpc_dict["pluginlist"] = _plugin_list

    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp(uri,
                                cookie="svcName=" + component_name + "; ",
                                on_open=_on_open,
                                on_message=_on_message,
                                on_error=_on_error,
                                on_close=_on_close)
    ws.header = ["Authorization: Basic " + b64encode(username + ":" + password)]
    return ws


def _plugin_list(args):
    global rpc_dict
    return list(rpc_dict.keys())


def _on_open(ws):
    print "WS opened"
    ws.send(json.dumps(_out_message("c", _cache_request_object("Time", strftime("%Y-%m-%d %H:%M:%S", gmtime())))))


def _on_message(ws, message):
    print message
    j_object = json.loads(message)
    _handle_request(ws, j_object["Data"])


def _on_error(ws, error):
    print error


def _on_close(ws):
    print "WS closed"


def _handle_request(ws, request_obj):
    global rpc_dict
    method = request_obj["Method"]
    params = request_obj["Params"]
    id = request_obj["ID"]
    out_message = None
    try:
        # Execute the procedure
        result = rpc_dict[method](params)
        # Compose an out message
        out_message = _out_message("", _response_object(result , None, request_obj))
        # Send out message only if the ID is not null or empty
        if id:
            ws.send(json.dumps(out_message))
    except:
        # TODO: Send an error object
        print "Error!"


def _response_object(result, error_obj, request_obj):
    response_obj = {"Result":result, "Error":error_obj, "ID":request_obj["ID"], "RID":request_obj["RID"]}
    return response_obj


def _out_message(header, data):
    out_obj = {"Header":header, "Data":data}
    return out_obj


def _cache_request_object(key, value):
    cache_request_obj = {"Key":key, "Value":value}
    return cache_request_obj
