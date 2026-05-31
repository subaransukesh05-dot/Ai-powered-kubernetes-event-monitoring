import ollama


def explain_event(event_data):
    prompt = f"""
You are a Kubernetes SRE assistant.

Analyze this Kubernetes event and explain:

1. What happened
2. Why it happened
3. Severity (Low/Medium/High)
4. Suggested fix

Event Details:

Namespace: {event_data.get("namespace")}
Type: {event_data.get("type")}
Reason: {event_data.get("reason")}
Object: {event_data.get("object")}
Message: {event_data.get("message")}

Keep the answer concise and beginner-friendly.
"""

    response = ollama.chat(
        model="gemma:2b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]
