from brain.llm import LLM


def test_extract_json_from_prose_and_nested_strings():
    text = 'Result: {"skill":"chat","params":{"message":"use {braces}"}} done'
    assert LLM.extract_json(text) == {
        "skill": "chat",
        "params": {"message": "use {braces}"},
    }


def test_extract_json_repairs_trailing_commas():
    assert LLM.extract_json('```json\n{"skill":"chat",}\n```') == {"skill": "chat"}
