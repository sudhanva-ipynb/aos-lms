import json
import concurrent.futures
import threading
import time

from protos import Lms_pb2,Lms_pb2_grpc
from Database.methods import gen_uuid
from Importers.common_imports import *
from Importers.common_methods import *
from Config.secrets import settings
from collections import Counter
from Helpers.assignments import assignments_map
from Helpers.queries import query_map
from Helpers.materials import materials_map

def apply(operation,args):
    with sqlite3.connect("lms.db") as conn:
        module,func = operation.split('.')
        for k,v in args.items():
            if k == "conn":
                args[k] = conn
        if module == "assignments":
            assignments_map[func](**args)
        elif module == "materials":
            materials_map[func](**args)
        elif module == "queries":
            query_map[func](**args)


def set_nodes():
    with sqlite3.connect("lms.db") as conn:
        cur_node =None
        node_list = []
        query = """SELECT id,host,port FROM node_discovery"""
        cur = conn.cursor()
        cur.execute(query)
        nodes = cur.fetchall()
        for node in nodes:
            node_info = {
                "id":node[0],
                "host":node[1],
                "port":node[2],
            }
            if node_info["id"] == settings.NODE_ID:
                cur_node = node_info
            else:
                node_list.append(node_info)
            print(node_list)
        return cur_node,node_list

def get_nxt_match_index(nodes,num):
    return {node["id"]:num for node in nodes}

def synchronized_method(lock_name):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kwargs)
        return wrapper
    return decorator

class Node:
    def __init__(self):
        self.cur_node, self.nodes = set_nodes()
        self.commited_index = 0
        self.last_applied = 0
        self.state = "F"  # Follower by default
        self.leader_node = None
        self.next_index = get_nxt_match_index(self.nodes, 1)
        self.match_index = get_nxt_match_index(self.nodes, 0)
        self._lock = threading.RLock()


    # ----------- LEADER FUNCTIONS --------------
    # def candidate_request_vote(self):
    #     """
    #     set state -> C
    #     term + 1
    #     -> requestVoteRPC
    #     wait for majority
    #     if majority:
    #         set state -> L
    #         set leader_node = cur
    #         initial next_ind
    #         ini match idx
    #         last_applied
    #     no majority:
    #         set state -> F
    #
    #     """
    #     state = self.get_state_info()
    #     self.set_state("C")
    #     self.set_term(state["term"]+1)
    #     with sqlite3.connect("lms.db") as conn:
    #         cur = conn.cursor()
    #         query = """
    #         SELECT idx,term FROM raft_logs ORDER By idx DESC LIMIT 1;
    #         """
    #         cur.execute(query)
    #         res = cur.fetchone()
    #         last_index,last_term = res[0],res[1]
    #         args = {
    #             "term" : state["term"]+1,
    #             "node_id":self.cur_node["id"],
    #             "last_log_idx":last_index,
    #             "last_log_term":last_term
    #
    #         }
    #         for node in self.nodes:
    #             # Implement RPC Call
    #             term,vote_granted = state["term"]+1,True
    #
    #         if vote_granted:
    #             self.set_state("L")
    #             self.leader_node =self.cur_node["id"]
    #             self.next_index = get_nxt_match_index(self.nodes,last_index+1)
    #             self.match_index = get_nxt_match_index(self.nodes,0)
    #             self.leader_append_entries()






    def leader_append_log(self, operation, args):
       try:
           state = self.get_state_info()
           with sqlite3.connect("lms.db") as conn:
               cur = conn.cursor()
               query = """
                      INSERT INTO raft_logs(id, operation, args, term, idx, created_at) VALUES(?,?,?,?,?,CURRENT_TIMESTAMP)
                      """
               cur.execute(query, (gen_uuid(), operation, json.dumps(args), state["term"], state["idx"] + 1,))
               conn.commit()
               idx = self.increment_idx(state["idx"])
               cur.close()
               result = self.leader_append_entries()
               if result:
                   self.leader_set_commited_index(idx)
               self.leader_set_last_applied(idx)
               return idx
       except Exception as error:
           print(error)


    def append_entries_to_node(self, node_info):
        """
        Mocked RPC logic for sending AppendEntries to a follower node.
        Simulates a successful log replication or failure based on random behavior.
        """
        try:
            with sqlite3.connect("lms.db") as conn:
                cur = conn.cursor()
                query = """
                    SELECT idx,term from raft_logs WHERE idx = ? - 1 ORDER BY idx 
                """
                cur.execute(query, (node_info["idx"],))
                res = cur.fetchone()
                if res is None:
                    prev_idx = 0
                    prev_term = 0
                else:
                    prev_idx = res[0]
                    prev_term = res[1]
                query = """
                             SELECT idx,term,operation,args from raft_logs WHERE idx >=?  ORDER BY idx 
                             """
                cur.execute(query, (node_info["idx"],))
                res = cur.fetchall()

                entries = []

                last_idx = None
                for entry in res:

                    fmt_log = {
                        "idx": entry[0],
                        "term": entry[1],
                        "operation": entry[2],
                        "args": entry[3],
                    }
                    """
                    {
                    \"idx\":1,
                    \"term\":1,
                    \"operation\":\"queries.create_query\",
                    \"args\":"{\"conn\": \"conn\", \"course\": \"8d313659-2360-44a2-9ab0-57dbd1ddc201\", \"query\": \"Can I use erlang?\", \"user_id\": \"d53e0c0b-d0a8-4ff7-85c1-fb68030ef577\"}"
                    """
                    last_idx = entry[0]
                    entries.append(fmt_log)
                if len(entries) > 1:
                    print(entries)
                log = {
                    "term": node_info["term"],
                    "leader_id": node_info["leader_node"],
                    "leader_commit_idx": node_info["commited_index"],
                    "prev_log_idx": prev_idx,
                    "prev_log_term": prev_term,
                    "entries": json.dumps({"entries": entries}),
                }
                try:
                    with grpc.insecure_channel(f"{node_info['host']}:{node_info['port']}") as channel:
                        # Create a stub (client)
                        stub = Lms_pb2_grpc.RaftStub(channel)

                        # Send the AppendEntries request
                        response = stub.appendEntries(Lms_pb2.AppendEntriesRequest(**log))
                    success, term = response.success, response.term
                except Exception as error:
                    print(error)
                    return False,None
                if success:
                    if last_idx:
                        self.leader_set_next_index(node_info["id"], last_idx + 1)
                        self.leader_set_match_index(node_info["id"], node_info["idx"])
                    return True,last_idx
                else:
                    print("Failed AppendEntry")
                    if term == node_info["term"]:
                        if prev_idx == 0:
                            self.leader_set_next_index(node_info["id"], 1)

                        else:
                            self.leader_set_next_index(node_info["id"], prev_idx)

                        return True,None

                    else:
                        self.set_state("F")
                    return False,None
        except Exception as error:
            print(error)

    # @synchronized_method("_lock")
    def leader_append_entries(self):
        """
        Handles log replication for the leader. Sends AppendEntries RPCs to all followers.
        Returns early if the majority acknowledges.
        """
        try:
            with sqlite3.connect("lms.db") as conn:
                state = self.get_state_info()
                nodes = self.nodes

                for node in nodes:
                    node["term"] = state["term"]
                    node["commited_index"] = self.leader_get_commited_index()
                    node["leader_node"] = self.leader_node
                    node["idx"] = self.leader_get_next_index(node["id"])

                acks = 1
                commit = False
                commit_idx = 0
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                    future_append_entries = {
                        executor.submit(self.append_entries_to_node, node): node for node in nodes
                    }

                    for future in concurrent.futures.as_completed(future_append_entries):
                        response = future_append_entries[future]
                        try:
                            data,commit_idx = future.result()

                        except Exception as exc:
                            print(f'{response} generated an exception: {exc}')
                        else:
                            if data:  # If log replication succeeded
                                acks += 1

                            # Check if majority is reached
                            if acks >= (len(nodes) + 1) // 2:
                                commit = True
                                break

                if commit:
                    self.leader_set_commited_index(commit_idx)
                    return True  # Log replication succeeded with majority
                else:
                    time.sleep(0.1)
                    return self.leader_append_entries()  # Retry if no majority
        except Exception as error:
            print(error)

    # ----------- FOLLOWER FUNCTIONS --------------
    def follower_append_entries(self, log_message):
        """
        Handles AppendEntries RPC on the follower side.
        Updates follower's log and commits entries if they pass consistency checks.
        """
        entries = json.loads(log_message["entries"])["entries"]

        with sqlite3.connect("lms.db") as conn:
            state = self.get_state_info()
            print(f"{state}")
            # Step down if the leader's term is higher
            if log_message["term"] > state["term"]:
                self.set_term(log_message["term"])
                self.state = "F"  # Become follower

            # Reject the request if the term is outdated
            elif log_message["term"] < state["term"]:
                print("Term is old")
                return False, state["term"]
            if not entries and log_message["prev_log_idx"] == 0:
                print("first empty entry")
                return True, log_message["term"]
            # Check if the follower's log contains the previous log entry
            cur = conn.cursor()
            if log_message["prev_log_idx"] != 0:

                query = "SELECT idx, term FROM raft_logs WHERE idx = ? AND term = ?"
                cur.execute(query, (log_message["prev_log_idx"], log_message["prev_log_term"]))
                prev_exists = cur.fetchone()

                if not prev_exists:
                    print("Missing previous entry")
                    # If the follower's log is inconsistent with the leader's log, return false
                    return False, state["term"]

            """  Handling wrong entries ?"""
            # Append the new entries if the logs match

            for entry in entries:
                cur.execute(
                    "INSERT INTO raft_logs (idx, term, operation, args) VALUES (?, ?, ?, ?) ON CONFLICT(idx,term) DO NOTHING ",
                    (entry["idx"], entry["term"], entry["operation"], entry["args"]),
                )

            conn.commit()

            query = """SELECT idx FROM raft_logs ORDER BY idx DESC LIMIT 1"""
            cur.execute(query)
            res = cur.fetchone()
            if not res:
                return True, state["term"]
            # Update the follower's commit index and apply the log entries
            if log_message["leader_commit_idx"] > self.commited_index:
                self.commited_index = min(log_message["leader_commit_idx"], res[0])

                self.apply_committed_entries()
            print("successful")
            return True, state["term"]

    def apply_committed_entries(self):
        """
        Apply all committed log entries to the state machine.
        """
        with sqlite3.connect("lms.db") as conn:
            cur = conn.cursor()
            query = "SELECT idx, operation, args FROM raft_logs WHERE idx <= ? and idx > ? and term = ?"
            cur.execute(query, (self.commited_index, self.last_applied, self.get_state_info()["term"]))
            committed_entries = cur.fetchall()

            for entry in committed_entries:
                operation = entry[1]
                args = json.loads(entry[2])
                apply(operation, args)
                self.last_applied = entry[0]
            conn.commit()
            cur.close()

    # ----------- STATE MANAGEMENT FUNCTIONS --------------
    # @synchronized_method("_lock")
    def get_state_info(self):
        with sqlite3.connect("lms.db") as conn:
            cur = conn.cursor()
            query = """
            SELECT  term,idx,voted_for FROM state_info LIMIT 1
            """
            cur.execute(query)
            res = cur.fetchone()
            state_info = {
                "term": res[0],
                "idx": res[1],
                "voted_for": res[2],
                "state": self.state
            }
            cur.close()
            return state_info

    # @synchronized_method("_lock")
    def set_term(self, term):
        with sqlite3.connect("lms.db") as conn:
            cur = conn.cursor()
            query = """
            UPDATE state_info SET term=?
            """
            cur.execute(query, (term,))
            conn.commit()
            cur.close()
            return term

    # @synchronized_method("_lock")
    def set_voted_for(self, voted_for):
        with sqlite3.connect("lms.db") as conn:
            cur = conn.cursor()
            query = """
            UPDATE state_info SET voted_for=?"""
            cur.execute(query, (voted_for,))
            conn.commit()
            cur.close()
            return voted_for

    # @synchronized_method("_lock")
    def set_state(self, state):
        self.state = state
        return state

    # @synchronized_method("_lock")
    def increment_idx(self, idx):
        with sqlite3.connect("lms.db") as conn:
            cur = conn.cursor()
            query = """
            UPDATE state_info SET idx=idx+1"""
            cur.execute(query)
            conn.commit()
            cur.close()
            return idx + 1

    # @synchronized_method("_lock")
    def leader_set_next_index(self, node_id, idx):
        self.next_index[node_id] = idx
        return idx

    # @synchronized_method("_lock")
    def leader_set_match_index(self, node_id, idx):
        self.match_index[node_id] = idx
        return idx

    # @synchronized_method("_lock")
    def leader_get_next_index(self, node_id):
        return self.next_index[node_id]

    # @synchronized_method("_lock")
    def leader_get_match_index(self, node_id):
        return self.match_index[node_id]

    # @synchronized_method("_lock")
    def leader_set_last_applied(self, applied):
        self.last_applied = applied
        return applied

    # @synchronized_method("_lock")
    def leader_get_last_applied(self):
        return self.last_applied

    # @synchronized_method("_lock")
    def leader_set_commited_index(self, commited_index):
        self.commited_index = commited_index
        return commited_index

    # @synchronized_method("_lock")
    def leader_get_commited_index(self):
        return self.commited_index

    # @synchronized_method("_lock")
    def get_leader_info(self, id):
        with sqlite3.connect("lms.db") as conn:
            cur = conn.cursor()
            query = """
            SELECT id,host,port FROM node_discovery WHERE id=?
            """
            cur.execute(query, (id,))
            res = cur.fetchone()
            leader_info = {
                "id": res[0],
                "host": res[1],
                "port": res[2]
            }
            cur.close()
            return leader_info
node  = Node()

