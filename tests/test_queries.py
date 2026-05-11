TEST_QUERIES = [

    # -------------------------
    # CONCEPTUAL
    # -------------------------

    {
        "question": "What is gradient descent?",
        "expected": "concept"
    },

    {
        "question": "Explain overfitting.",
        "expected": "concept"
    },

    # -------------------------
    # FORMULA
    # -------------------------

    {
        "question": "What is the formula for linear regression?",
        "expected": "formula"
    },

    # -------------------------
    # COMPARISON
    # -------------------------

    {
        "question": "Difference between CNN and RNN?",
        "expected": "comparison"
    },

    # -------------------------
    # CODING
    # -------------------------

    {
        "question": "Show Python code for gradient descent.",
        "expected": "code"
    },

    # -------------------------
    # OUTSIDE CONTEXT
    # -------------------------

    {
        "question": "Who won FIFA World Cup 2022?",
        "expected": "refusal"
    },

    {
        "question": "What is quantum entanglement?",
        "expected": "refusal"
    }
]