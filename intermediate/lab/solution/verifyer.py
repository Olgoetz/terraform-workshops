
import hcl2
from pathlib import Path


def parse_all_tf_files(directory: Path):
    combined = {}
    for tf_file in directory.glob("*.tf"):
        try:
            with tf_file.open("r") as f:
                content = hcl2.load(f)
                for key in content:
                    if key not in combined:
                        combined[key] = []
                    combined[key].extend(content[key])
        except Exception as e:
            print(f"❌ Error reading {tf_file.name}: {e}")
    return combined


def check_resource_names_with_prefix(data, prefix):
    results = []
    for resource in data.get("resource", []):
        for resource_type, instances in resource.items():
            for instance in instances:
                name = instance.get("name")
                if name and name.startswith(prefix):
                    results.append((resource_type, name))
    return results


def parse_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return hcl2.load(f)
    except Exception as e:
       # print(f"❌ Error reading {file_path}: {e}")
        return {}
    
def check_provider_exists(data, name):
    for provider in data.get("provider", []):
        if name in provider:
            return True
    return False


def check_provider_version(data, provider):
    for block in data.get("terraform", []):
        required_providers = block.get("required_providers", {})
        for item in required_providers:
            if provider in item:
                for entry in item[provider]:
                    if entry.get("version") == "~> 6.4":
                        return True
    return False

def check_variable(data, name):
    return any(name in var for var in data.get("variable", []))

def check_output(data, name):
    return any(name in out for out in data.get("output", []))

def check_modules(data):
    return "module" in data and len(data["module"]) > 0

def check_resources(data):
    return "resource" in data and len(data["resource"]) > 0

def main():
    base = Path(".")
    all_data = parse_all_tf_files(base)
    main_data = parse_file(base / "main.tf")
    variables_data = parse_file(base / "variables.tf")
    outputs_data = parse_file(base / "outputs.tf")
    versions_data = parse_file(base / "versions.tf")

    print("\nChecking file recommended file structure...")
    print("-------------------------------------------------------------------------------------")
    print("✅ main.tf found" if (base / "main.tf").exists() else "❌ main.tf missing")
    print("✅ variables.tf found" if (base / "variables.tf").exists() else "❌ variables.tf missing")
    print("✅ outputs.tf found" if (base / "outputs.tf").exists() else "❌ outputs.tf missing")
    print("✅ versions.tf found" if (base / "versions.tf").exists() else "❌ versions.tf missing")

    print("\nChecking provider version...")
    print("-------------------------------------------------------------------------------------")
    print("✅ Provider 'aws' block found" if check_provider_exists(all_data, "aws") else "❌ No aws provider block found")
    print("✅ Correct provider version" if check_provider_version(versions_data, "aws") else "❌ Incorrect or missing provider version in versions.tf")
    print("✅ Variable 'region' defined" if check_variable(variables_data, "region") else "❌ Variable 'region' missing")
    print("✅ Variable 'env' defined" if check_variable(variables_data, "env") else "❌ Variable 'env' missing")
    print("✅ Output 'instance_id' defined" if check_output(outputs_data, "instance_id") else "❌ Output 'instance_id' missing")

    # Check all resources for name starting with var.prefix
    prefix = "${var.prefix}"  # or set to your actual prefix value
    matches = check_resource_names_with_prefix(main_data, prefix)
    print("\nChecking resource names for prefix:")
    print("-------------------------------------------------------------------------------------")
    if matches:
        for rtype, name in matches:
            print(f"✅ Resource '{rtype}' has name '{name}' starting with prefix '{prefix}'")
    else:
        print(f"❌ No resource names start with prefix '{prefix}'")
if __name__ == "__main__":
    main()
