#!/usr/bin/env python3
"""
Inspect the structure of all_pr_data.json to understand its format
"""

import json
import sys

def inspect_json_structure():
    """Inspect the structure of all_pr_data.json"""
    try:
        # Open the JSON file and read a small portion to examine structure
        with open('all_pr_data.json', 'r') as f:
            # Read first few lines to get the opening structure
            first_lines = ""
            for i in range(20):
                line = f.readline()
                if not line:
                    break
                first_lines += line
            
            # Try to parse the beginning structure
            try:
                # Check if it's an array
                if first_lines.strip().startswith('['):
                    print("Data appears to be a JSON array")
                    
                    # Read a single complete entry
                    f.seek(0)
                    # Skip the opening bracket
                    f.readline()
                    
                    # Read until we find a complete object (matching braces)
                    entry_text = ""
                    brace_count = 0
                    in_object = False
                    
                    for line in f:
                        entry_text += line
                        
                        for char in line:
                            if char == '{':
                                brace_count += 1
                                in_object = True
                            elif char == '}':
                                brace_count -= 1
                        
                        if in_object and brace_count == 0:
                            # We've found a complete object
                            break
                    
                    # Clean up the entry (remove trailing comma if present)
                    entry_text = entry_text.strip()
                    if entry_text.endswith(','):
                        entry_text = entry_text[:-1]
                    
                    # Parse the entry
                    try:
                        entry = json.loads(entry_text)
                        print("\nSample entry structure:")
                        print(f"Keys: {list(entry.keys())}")
                        
                        # Check for created_at and merged_at fields
                        if 'created_at' in entry:
                            print(f"\nExample created_at: {entry['created_at']}")
                        elif 'basic_info' in entry and 'created_at' in entry['basic_info']:
                            print(f"\nExample created_at: {entry['basic_info']['created_at']}")
                        
                        if 'merged_at' in entry:
                            print(f"\nExample merged_at: {entry['merged_at']}")
                        elif 'basic_info' in entry and 'merged_at' in entry['basic_info']:
                            print(f"\nExample merged_at: {entry['basic_info']['merged_at']}")
                            
                        # Print a sample of the entry structure
                        print("\nSample entry (truncated):")
                        print(json.dumps(entry, indent=2, ensure_ascii=False)[:1000])
                        
                    except json.JSONDecodeError as e:
                        print(f"Error parsing sample entry: {e}")
                        print("Sample entry text (first 500 chars):")
                        print(entry_text[:500])
                else:
                    print("Data does not appear to be a JSON array")
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON structure: {e}")
                print("First few lines:")
                print(first_lines)
    
    except Exception as e:
        print(f"Error inspecting JSON structure: {e}")

if __name__ == "__main__":
    inspect_json_structure()
