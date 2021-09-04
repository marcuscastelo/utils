import pickle

class Serializable:
    def serialize(self):
        selfDict = self.__dict__.copy()
        for attr in selfDict:
            if isinstance(getattr(self, attr), Serializable):
                selfDict[attr] = getattr(self, attr).serialize()
        return pickle.dumps(selfDict)

    def deserialize(self, data: bytes):
        incomingDict = pickle.loads(data)
        for attr in incomingDict:
            if isinstance(getattr(self, attr), Serializable):
                setattr(self, attr, getattr(self, attr).deserialize(incomingDict[attr]))
            else:
                setattr(self, attr, incomingDict[attr])

        return self

    @staticmethod
    def from_pickle(filepath, default=None):
        with open(filepath, "rb") as f:
            serialized = pickle.loads(f)
            return (default or Serializable()).deserialize(serialized)