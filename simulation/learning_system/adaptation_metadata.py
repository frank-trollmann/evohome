
class Adaptation_Metadata:
    """
        This class contains metadata about one prediction cycle.

        It can be used to collect additional metrics about the adaptation and to record these in the produced dataset.

        Currently, this class records adaptation time in milliseconds.

        If you want to record other features, you should ...
        - record the feature in your adaptation controller in function (get_last_adaptation_metadata())
        - write a custom data recorder that records the produced data.
    """

    def __init__(self):
        self.adaptation_time = None