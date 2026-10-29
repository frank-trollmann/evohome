
class Prediction_Metadata:
    """
    This class contains metadata about one prediction cycle.
    
    Currently, this class records prediction time in milliseconds.
    
    If you want to record other features, you should ...
    - record the feature in your prediction system in function (get_last_prediction_metadata())
    - write a custom data recorder that records the produced data.

    """

    def __init__(self):
        self.prediction_time = None