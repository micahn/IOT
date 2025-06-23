import os
import machine
import time
import network
import json
import asyncio

server_root = '/www'

mimes = {
    '.html' : 'text/html; charset=utf-8',
    '.ico' : 'image/x-icon',
    '.js' : 'application/javascript'}

class Response:
    def __init__(self, body:bytes=b'', status=200, content_type='text/html; charset=utf-8') -> None:
        self.status = status
        self.body = body
        self.content_type = content_type
        self.headers = {}
        
    def encode(self) -> bytes:
        reason = {
            200: 'OK',
            404: 'Not Found',
            500: 'Internal Server Error',
        }.get(self.status, 'Unknown Status')

        body = self.body
        headers = [
            f"HTTP/1.1 {self.status} {reason}",
            f"Content-Type: {self.content_type}",
            f"Content-Length: {len(body)}",
            "Connection: close"
        ]
        for k,v in self.headers.items():
            headers.append(f"{k}: {v}")
        response = '\r\n'.join(headers) + '\r\n\r\n'
        return response.encode() + body
    
class Request:
    def __init__(self, raw: str):
        lines = raw.splitlines()
        request_line = lines[0].split()
        self.method = request_line[0]
        self.path = request_line[1]
        self.http_version = request_line[2] if len(request_line) > 2 else "HTTP/1.1"
        self.headers = {}
        i = 1
        for l in lines[1:]:
            if not l:
                break
            key, value = l.split(':', 1)
            self.headers[key.strip()] = value.strip()
            i += 1
        self.body = '\r\n'.join(lines[i+1:]) if (i+1) < len(lines) else ''



def read_temperature():
    """reads temperature from onboard temperature sensor on pin 4 of the pico W"""
    sensor = machine.ADC(4)
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    celsius = 27 - (volt - 0.706)/0.001721
    return round(celsius,0)

def sanitize_path(path: str) -> tuple[str,str,str]:
    parts = [p for p in path.lstrip("/").split("/") if p and p != "."]
    safe = []
    for p in parts:
        if p == "..":
            if safe: safe.pop()
        else:
            safe.append(p)
    fullpath = "/" + "/".join(safe)
    directory = fullpath[:fullpath.rfind("/")+1]
    filename = fullpath[len(directory):]
    return fullpath,directory,filename

def get_net_info():
    wlan = network.WLAN(network.STA_IF)
    return wlan.ifconfig()

def parse_request(data:str) -> Response:
    request = Request(data)
    response = Response()

    clean_path,directory,filename = sanitize_path(request.path)
    if clean_path == "/":
        if "index.html" in os.listdir(server_root):
            with open(server_root+"/index.html","rb") as f:
                 response.body = f.read()
    elif clean_path == "/info":
        ip, netmask, gateway, dns = get_net_info()
        body = json.dumps({
            "ip":ip,
            "netmask":netmask,
            "gateway":gateway,
            "dns":dns,
            "temp": read_temperature()
        })
        response = Response(body.encode(),content_type="application/json")
    else:
        print(filename,directory)
        if filename in os.listdir(server_root+directory):
            ext = filename[filename.rfind('.'):]
            response.content_type = mimes.get(ext,"application/octet-stream")
            with open(server_root+clean_path,"rb") as f:
                response.body = f.read()
        else:
            response.status = 404

    return response




async def serve_http(reader:asyncio.StreamReader, writer:asyncio.StreamWriter):
    try:
        peername = reader.get_extra_info('peername')
        data = await reader.read(2048)
        request = None
        if data:
            request = data.decode()
            print(request)
            response = parse_request(request)
            response_buffer = response.encode()
            writer.write(response_buffer)
            await writer.drain()
    except Exception as e:
        print(f"Error in serve_http: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

        
        


async def start_http(host: str, port: int):
    server = await asyncio.start_server(serve_http, host, port)
    print(f"Listening on {host}:{port}")
    await server.wait_closed()

    



def run():
    asyncio.run(start_http("0.0.0.0", 80))
