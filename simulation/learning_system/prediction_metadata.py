
class Prediction_Metadata:
    """
    This class contains metadata about one prediction cycle.
    As default, the metadata only contains the prediction time. 
    This class is here to be extended in case you want to record other metadata.

    """

    def __init__(self):
        self.prediction_time = None