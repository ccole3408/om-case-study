import json
import sys

def check_plan(plan_file):
    with open(plan_file, 'r') as file:
        plan = json.load(file)

    for resource_change in plan.get('resource_changes', []):
        action = resource_change.get('change', {}).get('actions', [])
        
        if 'delete' in action:
            print(f"Plan contains a delete action for resource: {resource_change['address']}. Apply should not proceed.")
            return False
        
        if 'create' in action:
            continue
        
        if 'update' in action:
            before = resource_change.get('change', {}).get('before', {})
            after = resource_change.get('change', {}).get('after', {})
            if before.keys() != after.keys() or 'tags' not in before or 'tags' not in 

after:
                print(f"Plan contains an update action for resource: {resource_change['address']} that modifies attributes other than tags. Apply should not proceed.")
                return False
            
            if before['tags'].keys() != after['tags'].keys() or 'GitCommitHash' not in before['tags'] or 'GitCommitHash' not in after['tags']:
                print(f"Plan contains an update action for resource: {resource_change['address']} that modifies tags other than GitCommitHash. Apply should not proceed.")
                return False

    print("Plan is valid. Apply can proceed.")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_tfplan.json>")
        sys.exit(1)

