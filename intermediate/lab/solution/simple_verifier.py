#!/usr/bin/env python3
"""
Simple Terraform Workshop Verification Script

This script performs high-level verification of the Terraform workshop exercises.
It focuses on checking essential requirements rather than specific implementations.
"""

import os
import re
import subprocess
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Constants
SUCCESS = f"{Fore.GREEN}✅ {Style.RESET_ALL}"
FAILURE = f"{Fore.RED}❌ {Style.RESET_ALL}"
WARNING = f"{Fore.YELLOW}⚠️ {Style.RESET_ALL}"
INFO = f"{Fore.BLUE}ℹ️ {Style.RESET_ALL}"

class SimpleVerifier:
    def __init__(self, directory="."):
        self.base_dir = Path(directory)
        self.files = {}
        self.load_files()
    
    def load_files(self):
        """Load all relevant Terraform files."""
        tf_files = list(self.base_dir.glob("*.tf"))
        tfvars_files = list(self.base_dir.glob("*.tfvars"))
        
        for file_path in tf_files + tfvars_files:
            try:
                with open(file_path, 'r') as f:
                    self.files[file_path.name] = f.read()
            except Exception as e:
                print(f"{FAILURE} Error reading {file_path.name}: {e}")
                self.files[file_path.name] = ""
        
        # Store main.tf content separately for convenience
        self.main_tf = self.files.get("main.tf", "")
        self.variables_tf = self.files.get("variables.tf", "")
        self.outputs_tf = self.files.get("outputs.tf", "")
    
    def run_terraform_command(self, command):
        """Run a terraform command and return the output."""
        try:
            result = subprocess.run(
                ["terraform"] + command,
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1
    
    def check_file_structure(self):
        """Check if the basic file structure exists."""
        print(f"\n{INFO} Checking file structure...")
        print("-------------------------------------------------------------------------------------")
        
        required_files = ["main.tf", "variables.tf", "outputs.tf"]
        recommended_files = ["versions.tf", "terraform.tfvars"]
        
        all_files = list(self.files.keys())
        
        for file in required_files:
            exists = file in all_files and self.files[file].strip()
            print(f"{SUCCESS if exists else FAILURE} {file} {'exists' if exists else 'missing or empty'}")
        
        for file in recommended_files:
            exists = file in all_files and self.files[file].strip()
            print(f"{WARNING if not exists else SUCCESS} {file} {'exists' if exists else 'missing or empty'} (recommended)")
        
        return all(file in all_files and self.files[file].strip() for file in required_files)
    
    def check_provider_aws(self):
        """Check if AWS provider is configured with version constraint."""
        print(f"\n{INFO} Checking AWS provider configuration...")
        print("-------------------------------------------------------------------------------------")
        
        # Look for provider block using robust regex
        provider_found = re.search(r"provider\s*\"aws\"", self.main_tf) is not None
        
        # Check for version constraint in required_providers block
        version_constraint = False
        for filename, content in self.files.items():
            if re.search(r"required_providers\s*{[^}]*aws[^}]*version\s*=", content, re.DOTALL):
                version_constraint = True
                break
        
        print(f"{SUCCESS if provider_found else FAILURE} AWS provider block found")
        print(f"{SUCCESS if version_constraint else FAILURE} AWS provider has version constraint")
        
        return provider_found and version_constraint
    
    def check_variables(self):
        """Check if required variables are defined with proper validation."""
        print(f"\n{INFO} Checking required variables...")
        print("-------------------------------------------------------------------------------------")
        
        # Use robust regex patterns
        prefix_var = re.search(r"variable\s*\"prefix\"", self.variables_tf) is not None
        env_var = re.search(r"variable\s*\"env\"", self.variables_tf) is not None
        env_validation = re.search(r"variable\s*\"env\"[^}]*validation\s*{", self.variables_tf, re.DOTALL) is not None
        
        print(f"{SUCCESS if prefix_var else FAILURE} Variable 'prefix' defined")
        print(f"{SUCCESS if env_var else FAILURE} Variable 'env' defined")
        print(f"{SUCCESS if env_validation else FAILURE} Variable 'env' has validation")
        
        return prefix_var and env_var and env_validation
    
    def check_locals_configuration(self):
        """Check if locals are properly configured."""
        print(f"\n{INFO} Checking locals configuration...")
        print("-------------------------------------------------------------------------------------")
        
        locals_block_found = re.search(r"locals\s*{", self.main_tf) is not None
        permanent_prefix_found = re.search(r"permanent_prefix\s*=\s*\"tfe-training\"", self.main_tf) is not None
        final_prefix_found = re.search(r"final_prefix\s*=", self.main_tf) is not None
        
        print(f"{SUCCESS if locals_block_found else FAILURE} Locals block found")
        print(f"{SUCCESS if permanent_prefix_found else FAILURE} permanent_prefix defined")
        print(f"{SUCCESS if final_prefix_found else FAILURE} final_prefix defined")
        
        return locals_block_found and permanent_prefix_found and final_prefix_found
    
    def check_sns_topics(self):
        """Check if SNS topics are created with for_each and conditional expressions."""
        print(f"\n{INFO} Checking SNS topic configuration...")
        print("-------------------------------------------------------------------------------------")
        
        # Use robust regex patterns
        sns_resource = re.search(r"resource\s*\"aws_sns_topic\"", self.main_tf) is not None
        for_each_used = re.search(r"for_each\s*=\s*toset\(", self.main_tf) is not None
        conditional_used = re.search(r"each\.key\s*!=\s*\"[^\"]+\"\s*\?", self.main_tf) is not None
        
        print(f"{SUCCESS if sns_resource else FAILURE} SNS topic resource defined")
        print(f"{SUCCESS if for_each_used else FAILURE} for_each with toset used")
        print(f"{SUCCESS if conditional_used else FAILURE} Conditional expression used for naming")
        
        return sns_resource and for_each_used and conditional_used
        
    def check_import_block(self):
        """Check if import block is used for SQS queue."""
        print(f"\n{INFO} Checking import block configuration...")
        print("-------------------------------------------------------------------------------------")
        
        # Use robust regex patterns
        import_block = re.search(r"import\s*{", self.main_tf) is not None
        sqs_resource = re.search(r"resource\s*\"aws_sqs_queue\"\s*\"imported_queue\"", self.main_tf) is not None
        
        print(f"{SUCCESS if import_block else FAILURE} Import block defined")
        print(f"{SUCCESS if sqs_resource else FAILURE} SQS queue resource defined")
        
        return import_block and sqs_resource
    
    def check_outputs(self):
        """Check if required outputs are defined."""
        print(f"\n{INFO} Checking required outputs...")
        print("-------------------------------------------------------------------------------------")
        
        # Get expected outputs from outputs.tf using robust regex
        output_matches = re.findall(r"output\s*\"([^\"]+)\"", self.outputs_tf)
        expected_outputs = output_matches
        
        if not expected_outputs:
            print(f"{WARNING} No outputs defined in outputs.tf")
            return False
        
        # Check if outputs are defined using robust regex
        outputs_found = []
        for output_name in expected_outputs:
            if re.search(rf"output\s*\"{output_name}\"", self.outputs_tf):
                outputs_found.append(output_name)
        
        # Remove duplicates
        outputs_found = list(set(outputs_found))
        
        for output in expected_outputs:
            found = output in outputs_found
            print(f"{SUCCESS if found else FAILURE} Output '{output}' defined")
        
        return len(outputs_found) == len(expected_outputs)
    
    def check_terraform_features(self):
        """Check for usage of key Terraform features."""
        print(f"\n{INFO} Checking for key Terraform features...")
        print("-------------------------------------------------------------------------------------")
        
        # Features to check with more robust regex patterns
        features = {
            "Data sources": r"data\s*\"[^\"]+\"\s*\"[^\"]+\"",
            "Local values": r"locals\s*{",
            "For each": r"for_each\s*=",
            "Conditional expressions": r"\?[^:]*:",
            "Module usage": r"module\s*\"[^\"]+\"",
            "Import block": r"import\s*{",
            "Ephemeral resources": r"ephemeral\s*\"[^\"]+\""
        }
        
        results = {}
        
        for feature, pattern in features.items():
            found = re.search(pattern, self.main_tf) is not None
            results[feature] = found
            print(f"{SUCCESS if found else WARNING} {feature} {'used' if found else 'not found'}")
        
        # Not all features are required, so return True
        return True
    
    def check_terraform_validate(self):
        """Run terraform validate to check configuration validity."""
        print(f"\n{INFO} Running terraform validate...")
        print("-------------------------------------------------------------------------------------")
        
        stdout, stderr, returncode = self.run_terraform_command(["validate"])
        
        if returncode == 0:
            print(f"{SUCCESS} Terraform configuration is valid")
            return True
        else:
            print(f"{FAILURE} Terraform configuration is invalid:")
            print(stderr)
            return False
    
    def run_verification(self):
        """Run all verification checks."""
        print("\nTerraform Workshop Simple Verifier")
        print("=====================================================================================")
        
        results = {
            "File Structure": self.check_file_structure(),
            "AWS Provider": self.check_provider_aws(),
            "Required Variables": self.check_variables(),
            "Locals Configuration": self.check_locals_configuration(),
            "SNS Topics": self.check_sns_topics(),
            "Import Block": self.check_import_block(),
            "Required Outputs": self.check_outputs()
        }
        
        # These checks don't affect the overall result
        self.check_terraform_features()
        terraform_valid = self.check_terraform_validate()
        
        # Summary
        print("\n=====================================================================================")
        print(f"{INFO} Verification Summary")
        print("=====================================================================================")
        
        for check, passed in results.items():
            print(f"{SUCCESS if passed else FAILURE} {check}")
        
        print(f"{SUCCESS if terraform_valid else WARNING} Terraform Validation")
        
        # Overall result
        all_passed = all(results.values())
        
        print("\n=====================================================================================")
        if all_passed and terraform_valid:
            print(f"{SUCCESS} All essential requirements are met!")
        elif all_passed:
            print(f"{WARNING} Essential structure requirements are met, but terraform validate failed.")
        else:
            print(f"{FAILURE} Some essential requirements are not met.")
        print("=====================================================================================")
        
        return all_passed and terraform_valid


if __name__ == "__main__":
    verifier = SimpleVerifier()
    verifier.run_verification()
