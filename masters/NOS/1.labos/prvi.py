import multiprocessing as mp
import time
import random

NUM_SMOKERS = 3
INGREDIENTS = ["PAPER", "TOBACCO", "MATCHES"]

def now_str():
   return time.strftime("%H:%M:%S", time.localtime())

def send_msg(q, msg):
   q.put(msg)

def trader_process(smoker_queues, trader_queue, seed=None):
    if seed is not None:
        random.seed(seed)
    pid = "TRADER"
    while True:
        a = random.randrange(3)
        b = random.randrange(3)
        while b == a:
            b = random.randrange(3)
        items = sorted([a, b])
        msg = {
            "type": "ITEMS",
            "from": pid,
            "items": items,
            "ts": None
        }
        print(f"[{now_str()}] TRADER: stavlja na stol {INGREDIENTS[items[0]]} + {INGREDIENTS[items[1]]}")
        for i, q in enumerate(smoker_queues):
            msg_to_send = dict(msg)
            msg_to_send["to"] = f"SMOKER-{i}"
            print(f"[{now_str()}] TRADER: šalje ITEMS -> SMOKER-{i}: {INGREDIENTS[items[0]]} + {INGREDIENTS[items[1]]}")
            send_msg(q, msg_to_send)
        try:
            taken_msg = trader_queue.get(timeout=10)
        except Exception:
            print(f"[{now_str()}] TRADER: timeout čekanja TAKEN, završavam.")
            break

        if taken_msg.get("type") == "TAKEN":
            who = taken_msg.get("from")
            print(f"[{now_str()}] TRADER: primio TAKEN od {who}. Sljedeći krug.\n")
        else:
            print(f"[{now_str()}] TRADER: primio neočekivanu poruku: {taken_msg}")
        time.sleep(0.5)

def smoker_process(my_id, my_ingredient, in_queue, other_queues, trader_queue, total_smokers=3):
    pid = f"SMOKER-{my_id}"
    lamport = 0
    req_queue = []
    waiting_replies_from = set()
    my_request_ts = None

    def on_receive(msg):
        nonlocal lamport, req_queue, waiting_replies_from
        msg_ts = msg.get("ts")
        if msg_ts is not None:
            lamport = max(lamport, msg_ts) + 1

        mtype = msg.get("type")
        sender = msg.get("from")
        print(f"[{now_str()}] {pid} PRIMIO {mtype} od {sender} (msg_ts={msg_ts}) -> local_ts={lamport}")

        if mtype == "REQUEST":
            r_ts = msg.get("req_ts")
            req_queue.append((r_ts, sender))
            req_queue.sort(key=lambda x: (x[0], x[1]))
            reply_msg = {"type": "REPLY", "from": pid, "to": sender, "ts": lamport}
            idx = int(sender.split("-")[1])
            send_msg(other_queues[idx], reply_msg)
            print(f"[{now_str()}] {pid} POSLAO REPLY -> {sender} (ts={lamport})")

        elif mtype == "REPLY":
            waiting_replies_from.discard(sender)

        elif mtype == "RELEASE":
            r_ts = msg.get("req_ts")
            req_queue = [r for r in req_queue if not (r[0] == r_ts and r[1] == sender)]
            waiting_replies_from.discard(sender)

    def can_enter_cs(ts):
        if not req_queue:
            return False
        first = req_queue[0]
        if first[0] != ts or first[1] != pid:
            return False
        if waiting_replies_from:
            return False
        return True

    while True:
        try:
            msg = in_queue.get(timeout=0.5)
        except Exception:
            msg = None

        if msg:
            if msg.get("type") == "ITEMS":
                items = msg.get("items")
                missing = [i for i in range(3) if i not in items][0]
                if my_ingredient == missing:
                    my_request_ts = lamport
                    req_queue.append((my_request_ts, pid))
                    req_queue.sort(key=lambda x: (x[0], x[1]))
                    waiting_replies_from.update({f"SMOKER-{i}" for i in range(total_smokers) if i != my_id})
                    req_msg = {"type": "REQUEST", "from": pid, "req_ts": my_request_ts, "ts": lamport}
                    for i, q in enumerate(other_queues):
                        if i != my_id:
                            m = dict(req_msg)
                            m["to"] = f"SMOKER-{i}"
                            send_msg(q, m)
                    print(f"[{now_str()}] {pid}: šaljem REQUEST za ulazak u kritični odsječak (ts={my_request_ts})")
            else:
                on_receive(msg)

        my_reqs = [r for r in req_queue if r[1] == pid]
        if my_reqs:
            ts = my_reqs[0][0]
            if can_enter_cs(ts):
                print(f"[{now_str()}] {pid} (local_ts={lamport}) -> ULAZIM u kritični odsječak (uzimam sastojke).")
                time.sleep(0.6)

                taken_msg = {"type": "TAKEN", "from": pid, "ts": lamport}
                send_msg(trader_queue, taken_msg)

                print(f"[{now_str()}] {pid} IZLAZIM iz kritičnog odsječka, motam cigaretu...")
                time.sleep(0.8)

                req_queue = [r for r in req_queue if not (r[0] == ts and r[1] == pid)]

                release_msg = {"type": "RELEASE", "from": pid, "req_ts": ts, "ts": lamport}
                for i, q in enumerate(other_queues):
                    if i != my_id:
                        m = dict(release_msg)
                        send_msg(q, m)

                my_request_ts = None
        time.sleep(0.05)

if __name__ == "__main__":
    mp.set_start_method("spawn")
    smoker_queues = [mp.Queue() for _ in range(NUM_SMOKERS)]
    trader_queue = mp.Queue()

    trader = mp.Process(target=trader_process, args=(smoker_queues, trader_queue), name="TRADER")
    trader.start()

    smokers = []
    for i in range(NUM_SMOKERS):
        p = mp.Process(target=smoker_process, args=(i, i, smoker_queues[i], smoker_queues, trader_queue, NUM_SMOKERS), name=f"SMOKER-{i}")
        p.start()
        smokers.append(p)

    for p in smokers:
        p.join()

    trader.join(timeout=2)
    print("Simulacija završena.")