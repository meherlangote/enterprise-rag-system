class ResponseValidator:
    def __init__(self):
        self.refusal_message = (
            "I could not find sufficient "
            "information in the provided documents."
        )

    def validate_answer(self, answer: str):
        answer = answer.strip()

        if len(answer) < 20:
            return False

        hallucination_patterns = [
            "according to general knowledge",
            "typically",
            "in most cases",
            "it is generally known",
            "outside the provided context",
        ]

        lower_answer = answer.lower()

        for pattern in hallucination_patterns:
            if pattern in lower_answer:
                return False

        return True

    def refusal_response(self):
        return self.refusal_message


response_validator = ResponseValidator()