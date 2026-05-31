from kubernetes import client, config, watch
from ai_agent import explain_event

# Load kube config
config.load_kube_config()

# Kubernetes API client
v1 = client.CoreV1Api()

# Watch object
w = watch.Watch()

# Important events only
IMPORTANT_REASONS = {
    "Failed",
    "BackOff",
    "ErrImagePull",
    "ImagePullBackOff",
    "CrashLoopBackOff",
    "OOMKilled",
    "Unhealthy"
}

print("Watching important Kubernetes events...\n")

for event in w.stream(v1.list_event_for_all_namespaces):

    obj = event["object"]

    reason = obj.reason

    # Skip unimportant events
    if reason not in IMPORTANT_REASONS:
        continue

    event_data = {
        "namespace": obj.metadata.namespace,
        "type": obj.type,
        "reason": obj.reason,
        "object": obj.involved_object.kind,
        "message": obj.message
    }

    print("=" * 60)
    print("RAW EVENT")
    print(event_data)

    print("\nAI ANALYSIS\n")

    explanation = explain_event(event_data)

    print(explanation)
