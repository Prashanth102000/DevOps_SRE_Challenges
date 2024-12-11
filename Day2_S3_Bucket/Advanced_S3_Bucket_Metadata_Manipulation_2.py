import json
from datetime import datetime, timedelta

with open('buckets.json','r') as file:
    data = json.load(file)

print("\n---  Summary of each bucket ---\n")
#Task 1: Print a summary of each bucket: Name, region, size (in GB), and versioning status
for bucket in data["buckets"]:
    size = bucket['sizeGB']
    name = bucket['name']
    version = bucket['versioning']
    region = bucket['region']
    print(f'Name={name},Region={region},Size={size},versioning={version}')


print("\n---  Identify buckets larger than 80 GB ---\n")
#Task 2: Identify buckets larger than 80 GB from every region which are unused for 90+ days.
# Highlight buckets with:
# Size > 50 GB: Recommend cleanup operations.
#Size > 100 GB and not accessed in 20+ days: Add these to a deletion queue.
deletion_queue = []
archival_candidates = []

for bucket in data["buckets"]:
    size = bucket['sizeGB']
    s = datetime.now() - datetime.strptime(bucket['createdOn'], "%Y-%m-%d")
    days_last_access = s.days
    region = bucket["region"]
    
    if size > 80 and days_last_access>90:
         print(f"Unused Bucket (>80GB): {bucket['name']} in {region} not accessed in 90+ days.")
            
    if size > 100 and days_last_access > 20:
        deletion_queue.append(bucket["name"])
    elif days_last_access > 50:
        archival_candidates.append(bucket["name"])

#Task 4. Provide a final list of buckets to delete (from the deletion queue). For archival candidates, suggest moving to Glacier.
print("\n=== Final Actions ===")
print("Buckets to Delete:")
for bucket_name in deletion_queue:
    print(f"- {bucket_name}")

print("\nBuckets to Archive:")
for bucket_name in archival_candidates:
    print(f"- {bucket_name}")


#Task 3: Generate a cost report: total s3 buckets cost grouped by region and department.

COST_STANDARD = 0.023
COST_GLACIER = 0.004
region_cost = {}
team_cost = {}


for bucket in data["buckets"]:
    region = bucket["region"]
    team = bucket["tags"]["team"]
    region_cost[region] = region_cost.get(region, 0) + size * COST_STANDARD
    team_cost[team] = team_cost.get(team, 0) + size * COST_STANDARD

print("\n--- Cost by Region ---")
for region, cost in region_cost.items():
    print(f"Region: {region}, Total Cost: ${cost:.2f}")

print("\n--- Cost by Team ---")
for team, cost in team_cost.items():
    print(f"Team: {team}, Total Cost: ${cost:.2f}")
    


    