import multiprocessing as mp
import time
import random

N_VISITORS = 12
SEATS = 4

def now():
   return time.strftime("%H:%M:%S", time.localtime())

def visitor_proc(pid, visitor_queues, carousel_queue):
   lamport = 0
   requesting = False
   in_cs = False
   waiting_queue = []
   my_ts = 0

   def inc_clock():
      nonlocal lamport
      lamport += 1
      return lamport

   def update_clock(msg_ts):
      nonlocal lamport
      lamport = max(lamport, msg_ts) + 1

   for ride in range(2):
      time.sleep(random.uniform(0.1, 2.0))
      requesting = True
      my_ts = lamport

      for i in range(N_VISITORS):
         if i != pid:
               visitor_queues[i].put(("REQUEST", pid, my_ts))
      print(f"[{now()}] POSJETITELJ-{pid}: poslao REQUEST (ts={my_ts})")

      replies_needed = set(i for i in range(N_VISITORS) if i != pid)

      while replies_needed:
         while not visitor_queues[pid].empty():
               msg = visitor_queues[pid].get()
               mtype, sender, msg_ts = msg
               update_clock(msg_ts)
               print(f"[{now()}] POSJETITELJ-{pid}: PRIMIO {mtype} od POSJETITELJ-{sender} -> local_ts={lamport}")

               if mtype == "REQUEST":
                  if in_cs or (requesting and (my_ts, pid) < (msg_ts, sender)):
                     waiting_queue.append(sender)
                     print(f"[{now()}] POSJETITELJ-{pid}: ODGODIO REPLY za POSJETITELJ-{sender}")
                  else:
                     ts = lamport
                     visitor_queues[sender].put(("REPLY", pid, ts))
                     print(f"[{now()}] POSJETITELJ-{pid}: POSLAO REPLY -> POSJETITELJ-{sender} (ts={ts})")
               elif mtype == "REPLY":
                  if sender in replies_needed:
                     replies_needed.remove(sender)
         time.sleep(0.01)

      in_cs = True
      requesting = False

      ts = lamport
      carousel_queue.put(("READY_TO_RIDE", pid, ts))
      print(f"[{now()}] POSJETITELJ-{pid}: Ušao u CS i šalje READY_TO_RIDE (ts={ts})")

      in_cs = False
      for wpid in waiting_queue:
         ts = lamport
         visitor_queues[wpid].put(("REPLY", pid, ts))
         print(f"[{now()}] POSJETITELJ-{pid}: POSLAO ODGOĐENI REPLY -> POSJETITELJ-{wpid} (ts={ts})")
      waiting_queue.clear()

      riding = True
      while riding:
         msg = visitor_queues[pid].get()
         mtype, sender, msg_ts = msg
         update_clock(msg_ts)
         print(f"[{now()}] POSJETITELJ-{pid}: PRIMIO {mtype} od {sender} -> local_ts={lamport}")

         if mtype == "SJEDI":
               print(f"[{now()}] POSJETITELJ-{pid}: Sjeo i čeka da se vožnja završi.")
         elif mtype == "USTANI":
               print(f"[{now()}] POSJETITELJ-{pid}: Sišao s vrtuljka.")
               riding = False
         elif mtype == "REQUEST":
               ts = lamport
               visitor_queues[sender].put(("REPLY", pid, ts))
               print(f"[{now()}] POSJETITELJ-{pid}: POSLAO REPLY (dok čeka vožnju) -> POSJETITELJ-{sender} (ts={ts})")

   ts = lamport
   carousel_queue.put(("DONE", pid, ts))
   print(f"[{now()}] POSJETITELJ-{pid}: poslao DONE (ts={ts}) i završio.")

def carousel_proc(visitor_queues, carousel_queue):
   lamport = 0

   def inc_clock():
      nonlocal lamport
      lamport += 1
      return lamport

   def update_clock(msg_ts):
      nonlocal lamport
      lamport = max(lamport, msg_ts) + 1

   riding = []
   done_visitors = set()
   total_done_needed = N_VISITORS
   print(f"[{now()}] VRTULJAK: pokrenut i čeka posjetitelje...")

   while len(done_visitors) < total_done_needed:
      if not carousel_queue.empty():
         msg = carousel_queue.get()
         mtype, sender, msg_ts = msg
         update_clock(msg_ts)
         print(f"[{now()}] VRTULJAK: Primio {mtype} od POSJETITELJ-{sender} -> Lamport={lamport}")

         if mtype == "READY_TO_RIDE":
               riding.append((sender, visitor_queues[sender]))
               print(f"[{now()}] VRTULJAK: POSJETITELJ-{sender} spreman ({len(riding)}/{SEATS})")
         elif mtype == "DONE":
               done_visitors.add(sender)
               print(f"[{now()}] VRTULJAK: POSJETITELJ-{sender} završio sve ({len(done_visitors)}/{total_done_needed})")

      if len(riding) == SEATS:
         print(f"[{now()}] VRTULJAK: Pun -> pokreće vožnju { [p for p, _ in riding] }")
         time.sleep(random.uniform(1.0, 3.0))
         print(f"[{now()}] VRTULJAK: Vožnja završena, šaljem USTANI.")

         for pid, v_queue in riding:
               ts = lamport
               v_queue.put(("USTANI", "VRTULJAK", ts))
               print(f"[{now()}] VRTULJAK: POSLAO USTANI -> POSJETITELJ-{pid} (ts={ts})")

         riding = []

      time.sleep(0.05)

   print(f"[{now()}] VRTULJAK: svi posjetitelji završili. Kraj simulacije.")

if __name__ == "__main__":
   mp.set_start_method("spawn")
   manager = mp.Manager()

   visitor_queues = [manager.Queue() for _ in range(N_VISITORS)]
   carousel_queue = manager.Queue()

   carousel = mp.Process(target=carousel_proc, args=(visitor_queues, carousel_queue))
   carousel.start()

   visitors = []
   for i in range(N_VISITORS):
      v = mp.Process(target=visitor_proc, args=(i, visitor_queues, carousel_queue))
      v.start()
      visitors.append(v)

   for v in visitors:
      v.join()
   carousel.join()

   print("Simulacija završena.")