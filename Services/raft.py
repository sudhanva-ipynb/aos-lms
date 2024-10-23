from Importers.common_imports import *
from protos import Lms_pb2,Lms_pb2_grpc
from Raft.node import node



class RaftService(Lms_pb2_grpc.RaftServicer):
    def appendEntries(self, request, context):
        try:

            log_message = {
                "term":request.term,
                "leader_id":request.leader_id,
                "prev_log_idx":request.prev_log_idx,
                "prev_log_term":request.prev_log_term,
                "entries":request.entries,
                "leader_commit_idx":request.leader_commit_idx,
            }
            success,term = node.follower_append_entries(log_message)
            return Lms_pb2.AppendEntriesResponse(term=term,success=success)
        except Exception as error:
            return Lms_pb2.AppendEntriesResponse(success=False)
