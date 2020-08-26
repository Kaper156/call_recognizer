class TranscriptionAnalyzer:
    ANSWERPHONE = (
        'автоответчик',
        'оставьте сообщение',
        'после сигнала',
    )

    # TODO as regex or simple nn
    COMFORT = {
        False: ('до свидания', 'не удобно', 'занят',),
        True: ('удобно', 'говорите', 'слушаю', 'да заинтересован', 'да интересно')
    }

    def __init__(self, response):
        self.transcription = ''
        # TODO refactor this

        for part in response:
            max_confidence = float('-inf')
            better_transcript = ''
            for alternative in part['alternatives']:
                if alternative['confidence'] > max_confidence:
                    max_confidence = alternative['confidence']
                    better_transcript = alternative['transcript']
            self.transcription += better_transcript

    def analyze_by_stage(self, stage):
        if stage == 1:
            return self.is_human()
        elif stage == 2:
            return self.is_comfort()
        else:
            raise ValueError(f"Unsupported stage: {stage}")

    def is_human(self):
        for yes_is_it in self.ANSWERPHONE:
            if yes_is_it in self.transcription:
                return 0
        return 1

    def is_comfort(self):
        for negative_phrase in self.COMFORT[False]:
            if negative_phrase in self.transcription:
                return 0
        return 1
