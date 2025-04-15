# ADD CODE HERE
# change script to whatever language you are comfortable with
import json

def should_proceed_with_apply(tfplan):
    for resource_change in tfplan.get('resource_changes', []):
        action = resource_change.get('change', {}).get('actions', [])
        
        # Check if the action is not create or update
        if not all(a in ['create', 'update'] for a in action):
            return False, f"Action {action} is not allowed."
        
        # If the action is update, check if only the tags attribute is modified
        if 'update' in action:
            before = resource_change.get('change', {}).get('before', {})
            after = resource_change.get('change', {}).get('after', {})
            
            # Check if only tags are modified
            modified_keys = [key for key in before if before[key] != after[key]]
            if modified_keys != ['tags']:
                return False, f"Modification of {modified_keys} is not allowed."
            
            # Check if only GitCommitHash tag is modified
            before_tags = before.get('tags', {})
            after_tags = after.get('tags', {})
            modified_tags = [key for key in before_tags if before_tags[key] != after_tags[key]]
            if modified_tags != ['GitCommitHash']:
                return False, f"Modification of tags {modified_tags} is not allowed."
    
    return True, "The plan can proceed."

# Load the tfplan.json file
with open('tfplan.json') as f:
    tfplan = json.load(f)

# Determine if the apply should proceed
proceed, message = should_proceed_with_apply(tfplan)
print(message)
