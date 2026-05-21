class StorageEngine:

    def persist(self, state):

        return {

            "storage": "STATE_PERSISTED",

            "data": state,

            "status": "SAVED"
        }
