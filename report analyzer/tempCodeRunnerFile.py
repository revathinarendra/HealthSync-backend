
                json_end = response.text.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    json_string = response.text[json_start:json_end]
                    return json.loads(json_string)
                else:
                    return {"error": "Could not find valid JSON in the model's response.", "raw_response": response.text}
            except json.JSONDecodeError as e:
                return {"error": f"Failed to parse JSON from LLM response: {e}", "raw_response": response.text}
        else:
            return {"error": "No response text from LLM."}

    except Exception as e:
        return {"error": f"An error occurred during PDF analysis: {e}"}
# Configure Google Generative AI API
# In a real Django application, you would get this from dja