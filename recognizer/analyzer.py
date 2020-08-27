class UnAnalyzedTranscriptionException(Exception):
    pass


class UnsupportedStageException(Exception):
    pass


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
        self.transcription, self.duration = self.read_response(response)
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
        for yes_is_it in self.ANSWERPHONE:
            if yes_is_it in self.transcription:
                return 0
        return 1

    def is_comfort(self):
        if not self.is_human():
            raise ImpossibleStageException("Analyzer cannot determinate answer, "
                                           "because previous stage is failed")
        for negative_phrase in self.COMFORT[False]:
            if negative_phrase in self.transcription:
                return 0
        for positive_phrase in self.COMFORT[True]:
            if positive_phrase in self.transcription:
                return 1
        raise UnAnalyzedTranscriptionException("Analyzer cannot determinate answer, because "
                                               "transcription does'nt contain any known phrases")

    def get_transcription(self):
        return self.transcription

    def get_duration(self):
        return self.duration
