# Raise when analyzer cannot give an exact answer
class UnAnalyzedTranscriptionException(Exception):
    pass


# Raise when given stage which not supported now
class UnsupportedStageException(Exception):
    pass


# Raise when call cannot be at this stage.
# For ex.: doesn't matter is comfort to talk or not if previous stage determinate that is answerphone
class ImpossibleStageException(Exception):
    pass


class TranscriptionAnalyzer:
    ANSWERPHONE = (
        'автоответчик',
        'оставьте сообщение',
        'после сигнала',
    )

    COMFORT = {
        False: ('до свидания', 'до встречи', 'пока',
                'не удобно', 'занят', 'не заинтересован', 'не интересно', 'не готов'),
        True: ('удобно', 'говорите', 'слушаю',
               'заинтересован', 'интересно', 'готов')
    }

    def __init__(self, response):
        '''
        Analyze response
        :param response: response from api
        '''
        # Read response and get transcription and duration
        self.transcription, self.duration = self.read_response(response)

        # Tuple of method to perform transcription into answer at stage
        self.stage_performers = (
            self.is_human,
            self.is_comfort,
        )

    def read_response(self, response):
        transcription = ''
        duration = 0
        for part in response:
            max_confidence = float('-inf')
            better_transcript = ''
            for alternative in part['alternatives']:
                if alternative['confidence'] > max_confidence:
                    max_confidence = alternative['confidence']
                    better_transcript = alternative['transcript']
            transcription += better_transcript
            duration = float(part['end_time'].replace('s', ''))
        return transcription, duration

    def analyze_by_stage(self, stage):
        if stage > len(self.stage_performers):
            raise NotImplementedError(f"Unsupported stage: {stage}")
        else:
            stage -= 1
            # Call the corresponding stage method
            return self.stage_performers[stage]()

    def is_human(self):
        # If transcription contain any phrases which trigger it is answerphone
        for yes_is_it in self.ANSWERPHONE:
            if yes_is_it in self.transcription:
                # It is answerphone
                return 0
        # Else
        # It is human
        return 1

    def is_comfort(self):
        # If it is answerphone doesn't matter what it says
        if not self.is_human():
            raise ImpossibleStageException("Analyzer cannot determinate answer, "
                                           "because previous stage is failed")
        for negative_phrase in self.COMFORT[False]:
            if negative_phrase in self.transcription:
                return 0
        for positive_phrase in self.COMFORT[True]:
            if positive_phrase in self.transcription:
                return 1
        # To control and learn analyzer
        raise UnAnalyzedTranscriptionException("Analyzer cannot determinate answer, because "
                                               "transcription does'nt contain any known phrases")

    def get_transcription(self):
        return self.transcription

    def get_duration(self):
        return self.duration
