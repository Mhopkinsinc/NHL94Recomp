#!/usr/bin/env python3
"""
vdp_event_capture.py - drain the runner's always-on VDP event ring to a file
while the game runs (connect -> query backward -> analyze; PRINCIPLES #17).

The ring holds the last 16384 VDP register/command/data/DMA events. Polling it
a few times a second and merging by sequence number yields a complete VDP write
history for the session, which the TCP `vdp_events` query alone cannot give
(the ring turns over in a few seconds of gameplay).

Run in a second terminal while NHL94Recomp.exe is up (debug.ini next to it):
    python tools/vdp_event_capture.py --out C:\\temp\\vdp_events.csv
Stop with Ctrl-C. Columns: seq,kind,code,reason,vbl,line,addr,value,inc,len,src,f0,f1,f2
(f0..f2 = the three most recently entered 68K functions at the event)
kind: 1=REG 2=CMD 3=DATA 4=DMA_68K 5=DMA_FILL_ARM 6=DMA_COPY 7=DMA_SKIP
"""
import argparse
import json
import socket
import sys
import time


def query(port: int, payload: dict) -> dict:
    s = socket.create_connection(("127.0.0.1", port), timeout=10)
    s.sendall((json.dumps(payload) + "\n").encode())
    buf = b""
    while not buf.endswith(b"\n"):
        chunk = s.recv(1 << 20)
        if not chunk:
            break
        buf += chunk
    s.close()
    return json.loads(buf.decode(errors="replace"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=4380)
    ap.add_argument("--out", required=True)
    ap.add_argument("--interval", type=float, default=0.25)
    args = ap.parse_args()

    last_seq = -1
    total = 0
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("seq,kind,code,reason,vbl,line,addr,value,inc,len,src,f0,f1,f2\n")
        print("capturing; Ctrl-C to stop", file=sys.stderr)
        try:
            while True:
                try:
                    r = query(args.port, {"id": 1, "cmd": "vdp_events", "count": 16384})
                except (ConnectionRefusedError, socket.timeout, OSError):
                    time.sleep(0.5)
                    continue
                evs = r.get("events", [])
                new = [e for e in evs if e["seq"] > last_seq]
                if new:
                    if last_seq >= 0 and new[0]["seq"] > last_seq + 1:
                        print(f"[gap] lost {new[0]['seq'] - last_seq - 1} events before seq {new[0]['seq']}",
                              file=sys.stderr)
                    for e in new:
                        f.write(f"{e['seq']},{e['kind']},{e['code']},{e['reason']},{e['vbl']},{e['line']},"
                                f"{e['addr']},{e['value']},{e['inc']},{e['len']},{e['src']},"
                                f"{e.get('f0',0)},{e.get('f1',0)},{e.get('f2',0)}\n")
                    last_seq = new[-1]["seq"]
                    total += len(new)
                    f.flush()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            pass
    print(f"wrote {total} events to {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
