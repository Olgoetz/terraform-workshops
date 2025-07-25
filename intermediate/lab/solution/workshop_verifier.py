#!/usr/bin/env python3
"""
Terraform Workshop Verification Script

This script verifies the completion of exercises in the Terraform workshop.
It checks for the presence and correctness of various Terraform resources and configurations.
"""

import os
import re
import subprocess
from pathlib import Path

# Constants
SUCCESS = f"✅ "
FAILURE = f"❌ "
WARNING = f"⚠️ "
INFO = f"ℹ️ "

class TerraformVerifier:
    def __init__(self, directory="."):
        self.base_dir = Path(directory)
        self.main_tf = self._read_file("main.tf")
        self.variables_tf = self._read_file("variables.tf")
        self.outputs_tf = self._read_file("outputs.tf")
        self.versions_tf = self._read_file("versions.tf")
        self.tfvars = self._read_file("terraform.tfvars")
        
        # Get the prefix and env from tfvars or use defaults
        self.prefix = self._extract_tfvars_value("prefix", "unknown-prefix")
        self.env = self._extract_tfvars_value("env", "dev")
        
    def _read_file(self, filename):
        """Read a file and return its content."""
        try:
            with open(self.base_dir / filename, 'r') as f:
                return f.read()
        except Exception:
            return ""
    
    def _extract_tfvars_value(self, key, default=""):
        """Extract a value from terraform.tfvars."""
        pattern = rf'{key}\s*=\s*"?([^"\n]+)"?'
        match = re.search(pattern, self.tfvars)
        if match:
            return match.group(1)
        return default
    
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
    
    def check_terraform_cloud_config(self):
        """Check Exercise 1: Terraform Cloud Configuration."""
        print(f"\n{INFO} Checking Exercise 1: Terraform Cloud Configuration...")
        print("-------------------------------------------------------------------------------------")
        
        cloud_config_found = "cloud {" in self.main_tf
        hostname_found = re.search(r'hostname\s*=\s*"tfe\.axa-cloud\.com"', self.main_tf)
        organization_found = re.search(r'organization\s*=\s*"TFE-Training"', self.main_tf)
        workspace_name_found = "workspaces {" in self.main_tf and "name =" in self.main_tf
        
        print(f"{SUCCESS if cloud_config_found else FAILURE} Terraform Cloud block found")
        print(f"{SUCCESS if hostname_found else FAILURE} Hostname set to 'tfe.axa-cloud.com'")
        print(f"{SUCCESS if organization_found else FAILURE} Organization set to 'TFE-Training'")
        print(f"{SUCCESS if workspace_name_found else FAILURE} Workspace name configured")
        
        return cloud_config_found and hostname_found and organization_found and workspace_name_found
    
    def check_provider_config(self):
        """Check Exercise 2: Provider Configuration with Default Tags."""
        print(f"\n{INFO} Checking Exercise 2: Provider Configuration with Default Tags...")
        print("-------------------------------------------------------------------------------------")
        
        provider_found = "provider \"aws\"" in self.main_tf
        region_correct = "region = \"eu-central-1\"" in self.main_tf or "region = 'eu-central-1'" in self.main_tf
        tags_found = "default_tags" in self.main_tf and "tags" in self.main_tf
        tfe_tag_found = "\"tfe-training\" = \"true\"" in self.main_tf or "'tfe-training' = 'true'" in self.main_tf
        owner_tag_found = "\"owner\"" in self.main_tf and "var.prefix" in self.main_tf
        
        print(f"{SUCCESS if provider_found else FAILURE} AWS provider block found")
        print(f"{SUCCESS if region_correct else FAILURE} Region set to 'eu-central-1'")
        print(f"{SUCCESS if tags_found else FAILURE} Default tags block found")
        print(f"{SUCCESS if tfe_tag_found else FAILURE} Default tag 'tfe-training=true' found")
        print(f"{SUCCESS if owner_tag_found else FAILURE} Default tag 'owner=${{var.prefix}}' found")

        return provider_found and region_correct and tags_found and tfe_tag_found and owner_tag_found
    
    def check_variables(self):
        """Check Exercise 3: Variables with Validation."""
        print(f"\n{INFO} Checking Exercise 3: Variables with Validation...")
        print("-------------------------------------------------------------------------------------")
        
        prefix_var_found = "variable \"prefix\"" in self.variables_tf
        env_var_found = "variable \"env\"" in self.variables_tf
        env_validation_found = "validation" in self.variables_tf and "contains" in self.variables_tf and all(env in self.variables_tf for env in ["dev", "test", "prod"])
        tfvars_file_found = Path(self.base_dir / "terraform.tfvars").exists()
        env_value_correct = self.env in ["dev", "test", "prod"]
        
        print(f"{SUCCESS if prefix_var_found else FAILURE} Variable 'prefix' defined")
        print(f"{SUCCESS if env_var_found else FAILURE} Variable 'env' defined")
        print(f"{SUCCESS if env_validation_found else FAILURE} Validation for 'env' variable found")
        print(f"{SUCCESS if tfvars_file_found else FAILURE} terraform.tfvars file exists")
        print(f"{SUCCESS if env_value_correct else FAILURE} Environment value is valid ('dev', 'test', or 'prod')")
        
        return prefix_var_found and env_var_found and env_validation_found and tfvars_file_found and env_value_correct
    
    def check_data_sources(self):
        """Check Exercise 4: Working with Data Sources."""
        print(f"\n{INFO} Checking Exercise 4: Working with Data Sources...")
        print("-------------------------------------------------------------------------------------")
        
        caller_identity_found = "data \"aws_caller_identity\"" in self.main_tf
        vpc_found = "data \"aws_vpc\"" in self.main_tf
        vpc_filter_correct = "name=\"tag:tfe-training\"" in self.main_tf.replace(" ", "") and "values=[\"true\"]" in self.main_tf.replace(" ", "")
        subnets_found = "data \"aws_subnets\"" in self.main_tf
        subnets_filter_correct = "name=\"vpc-id\"" in self.main_tf.replace(" ", "") and "values=[data.aws_vpc.selected.id]" in self.main_tf.replace(" ", "")
        
        print(f"{SUCCESS if caller_identity_found else FAILURE} AWS caller identity data source found")
        print(f"{SUCCESS if vpc_found else FAILURE} VPC data source found")
        print(f"{SUCCESS if vpc_filter_correct else FAILURE} VPC filter for tag:tfe-training=true found")
        print(f"{SUCCESS if subnets_found else FAILURE} Subnets data source found")
        print(f"{SUCCESS if subnets_filter_correct else FAILURE} Subnets filter for vpc-id found")
        
        return caller_identity_found and vpc_found and vpc_filter_correct and subnets_found and subnets_filter_correct
    
    def check_locals(self):
        """Check Exercise 5: Using Locals for Naming Conventions."""
        print(f"\n{INFO} Checking Exercise 5: Using Locals for Naming Conventions...")
        print("-------------------------------------------------------------------------------------")
        
        locals_found = "locals {" in self.main_tf
        permanent_prefix_found = "permanent_prefix = \"tfe-training\"" in self.main_tf or "permanent_prefix = 'tfe-training'" in self.main_tf
        final_prefix_found = re.search(r"final_prefix\s*=\s*", self.main_tf)
        final_prefix_correct = all(part in self.main_tf for part in ["tfe-training", "var.env", "var.prefix"])
        
        print(f"{SUCCESS if locals_found else FAILURE} Locals block found")
        print(f"{SUCCESS if permanent_prefix_found else FAILURE} Local 'permanent_prefix' defined as 'tfe-training'")
        print(f"{SUCCESS if final_prefix_found else FAILURE} Local 'final_prefix' defined")
        print(f"{SUCCESS if final_prefix_correct else FAILURE} 'final_prefix' combines permanent_prefix, env, and prefix")
        
        return locals_found and permanent_prefix_found and final_prefix_found and final_prefix_correct
    
    def check_sns_topics(self):
        """Check Exercise 6: Resource Creation with For Each and Conditional Expressions."""
        print(f"\n{INFO} Checking Exercise 6: Resource Creation with For Each and Conditional Expressions...")
        print("-------------------------------------------------------------------------------------")

        sns_resource_found = re.search(r"resource\s*\"aws_sns_topic\"", self.main_tf)
        for_each_used = re.search(r"for_each\s*=\s*", self.main_tf) and all(topic in self.main_tf for topic in ["sns-1", "sns-2", "sns-3"])
        conditional_naming = "each.key" in self.main_tf and "?" in self.main_tf and ":" in self.main_tf
        
        print(f"{SUCCESS if sns_resource_found else FAILURE} SNS topic resource found")
        print(f"{SUCCESS if for_each_used else FAILURE} for_each used with topics sns-1, sns-2, sns-3")
        print(f"{SUCCESS if conditional_naming else FAILURE} Conditional expression used for naming")
        
        return sns_resource_found and for_each_used and conditional_naming
    
    def check_import_block(self):
        """Check Exercise 7: Resource Importing with the Import Block."""
        print(f"\n{INFO} Checking Exercise 7: Resource Importing with the Import Block...")
        print("-------------------------------------------------------------------------------------")
        
        import_block_found = "import {" in self.main_tf
        sqs_resource_found = "resource \"aws_sqs_queue\" \"imported_queue\"" in self.main_tf
 
        print(f"{SUCCESS if import_block_found else FAILURE} Import block found")
        print(f"{SUCCESS if sqs_resource_found else FAILURE} SQS queue resource defined")
    
        
        return import_block_found and sqs_resource_found
    
    def check_s3_module(self):
        """Check Exercise 8: Working with Modules."""
        print(f"\n{INFO} Checking Exercise 8: Working with Modules...")
        print("-------------------------------------------------------------------------------------")

        module_found = re.search(r"module\s*\"s3_bucket\"", self.main_tf)
        correct_source = re.search(r"source\s*=\s*\"tfe.axa-cloud.com/Global-Module-Sharing/s3-bucket-synced/aws\"", self.main_tf)
        correct_version = re.search(r"version\s*=\s*\"5.2.0\"", self.main_tf)
        bucket_name_correct = re.search(r'bucket\s*=\s*"\$\{local\.final_prefix\}.*"', self.main_tf)
        versioning_enabled = re.search(r"versioning\s*=\s*{[^}]*enabled\s*=\s*true", self.main_tf)

        print(f"{SUCCESS if module_found else FAILURE} S3 bucket module found")
        print(f"{SUCCESS if correct_source else FAILURE} Correct module source used")
        print(f"{SUCCESS if correct_version else FAILURE} Module version 5.2.0 specified")
        print(f"{SUCCESS if bucket_name_correct else FAILURE} Bucket name uses final_prefix")
        print(f"{SUCCESS if versioning_enabled else FAILURE} Versioning enabled for bucket")
        
        return module_found and correct_source and correct_version and bucket_name_correct and versioning_enabled
    
    def check_s3_object(self):
        """Check Exercise 9: File Operations with S3 Objects."""
        print(f"\n{INFO} Checking Exercise 9: File Operations with S3 Objects...")
        print("-------------------------------------------------------------------------------------")
        
        s3_object_found = bool(re.search(r'resource\s+"aws_s3_object"', self.main_tf))
        correct_bucket = bool(re.search(r'module\.s3_bucket\.s3_bucket_id', self.main_tf.replace(" ", "")))
        correct_key = bool(re.search(r'key\s*=\s*"s3_object\.txt"', self.main_tf))
        file_content_used = bool(re.search(r'content\s*=\s*file\(', self.main_tf)) and "s3_object.txt" in self.main_tf
        file_exists = Path(self.base_dir / "s3_object.txt").exists()
        
        print(f"{SUCCESS if s3_object_found else FAILURE} S3 object resource found")
        print(f"{SUCCESS if correct_bucket else FAILURE} S3 object uses bucket from module")
        print(f"{SUCCESS if correct_key else FAILURE} S3 object key set to 's3_object.txt'")
        print(f"{SUCCESS if file_content_used else FAILURE} S3 object uses file() function for content")
        print(f"{SUCCESS if file_exists else FAILURE} s3_object.txt file exists")
        
        return s3_object_found and correct_bucket and correct_key and file_content_used and file_exists
    
    def check_ephemeral_resources(self):
        """Check Exercise 10: Working with Ephemeral Resources."""
        print(f"\n{INFO} Checking Exercise 10: Working with Ephemeral Resources...")
        print("-------------------------------------------------------------------------------------")
        
        random_password_found = "ephemeral \"aws_secretsmanager_random_password\"" in self.main_tf
        secret_found = "resource \"aws_secretsmanager_secret\"" in self.main_tf
        secret_version_found = "resource \"aws_secretsmanager_secret_version\"" in self.main_tf
        ephemeral_secret_version_found = "ephemeral \"aws_secretsmanager_secret_version\"" in self.main_tf
        
        print(f"{SUCCESS if random_password_found else FAILURE} Ephemeral random password resource found")
        print(f"{SUCCESS if secret_found else FAILURE} Secrets Manager secret resource found")
        print(f"{SUCCESS if secret_version_found else FAILURE} Secret version resource found")
        print(f"{SUCCESS if ephemeral_secret_version_found else FAILURE} Ephemeral secret version resource found")
        
        return random_password_found and secret_found and secret_version_found and ephemeral_secret_version_found
    
    def check_database_setup(self):
        """Check Exercise 11: Database Setup with Security Groups."""
        print(f"\n{INFO} Checking Exercise 11: Database Setup with Security Groups...")
        print("-------------------------------------------------------------------------------------")
        
        security_group_found = "resource \"aws_security_group\"" in self.main_tf
        sg_ingress_correct = "ingress" in self.main_tf and "from_port" in self.main_tf and "to_port" in self.main_tf and "protocol" in self.main_tf and "5432" in self.main_tf
        db_subnet_group_found = "resource \"aws_db_subnet_group\"" in self.main_tf
        db_instance_found = "resource \"aws_db_instance\"" in self.main_tf
        db_password_correct = "password_wo" in self.main_tf and "ephemeral" in self.main_tf
        
        print(f"{SUCCESS if security_group_found else FAILURE} Database security group found")
        print(f"{SUCCESS if sg_ingress_correct else FAILURE} Security group allows PostgreSQL traffic (port 5432)")
        print(f"{SUCCESS if db_subnet_group_found else FAILURE} DB subnet group found")
        print(f"{SUCCESS if db_instance_found else FAILURE} RDS instance found")
        print(f"{SUCCESS if db_password_correct else FAILURE} RDS instance uses password from ephemeral resource")
        
        return security_group_found and sg_ingress_correct and db_subnet_group_found and db_instance_found and db_password_correct
    
    def check_outputs(self):
        """Check Exercise 12: Creating Outputs."""
        print(f"\n{INFO} Checking Exercise 12: Creating Outputs...")
        print("-------------------------------------------------------------------------------------")
        
        vpc_id_output = "output \"vpc_id\"" in self.outputs_tf
        subnet_ids_output = "output \"subnet_ids\"" in self.outputs_tf
        sns_topic_arns_output = "output \"sns_topic_arns\"" in self.outputs_tf
        for_expression_used = "for" in self.outputs_tf and "aws_sns_topic.sns_topic" in self.outputs_tf
        
        print(f"{SUCCESS if vpc_id_output else FAILURE} VPC ID output found")
        print(f"{SUCCESS if subnet_ids_output else FAILURE} Subnet IDs output found")
        print(f"{SUCCESS if sns_topic_arns_output else FAILURE} SNS topic ARNs output found")
        print(f"{SUCCESS if for_expression_used else FAILURE} For expression used in outputs")
        
        return vpc_id_output and subnet_ids_output and sns_topic_arns_output and for_expression_used
    
    def run_all_checks(self):
        """Run all verification checks and return overall results."""
        print(f"\n{INFO} Starting Terraform Workshop Verification...")
        print("=====================================================================================")
        
                
        # Run terraform validate if terraform is available
        print(f"\n{INFO} Running terraform fmt...")
        print("-------------------------------------------------------------------------------------")
        stdout, stderr, returncode = self.run_terraform_command(["fmt", "."])
        if returncode == 0:
            print(f"{SUCCESS} Terraform files formattted")
        else:
            print(f"{FAILURE} Terraform formatting failed")
            print(stderr)
        
        
        # File structure check
        print(f"\n{INFO} Checking file structure...")
        print("-------------------------------------------------------------------------------------")
        main_exists = Path(self.base_dir / "main.tf").exists()
        variables_exists = Path(self.base_dir / "variables.tf").exists()
        outputs_exists = Path(self.base_dir / "outputs.tf").exists()
        versions_exists = Path(self.base_dir / "versions.tf").exists()
        tfvars_exists = Path(self.base_dir / "terraform.tfvars").exists()
        
        print(f"{SUCCESS if main_exists else FAILURE} main.tf found")
        print(f"{SUCCESS if variables_exists else FAILURE} variables.tf found")
        print(f"{SUCCESS if outputs_exists else FAILURE} outputs.tf found")
        print(f"{SUCCESS if versions_exists else FAILURE} versions.tf found")
        print(f"{SUCCESS if tfvars_exists else FAILURE} terraform.tfvars found")
        
        # Run all checks
        results = {
            "Exercise 1: Terraform Cloud Configuration": self.check_terraform_cloud_config(),
            "Exercise 2: Provider Configuration": self.check_provider_config(),
            "Exercise 3: Variables with Validation": self.check_variables(),
            "Exercise 4: Data Sources": self.check_data_sources(),
            "Exercise 5: Locals for Naming": self.check_locals(),
            "Exercise 6: For Each and Conditionals": self.check_sns_topics(),
            "Exercise 7: Import Block": self.check_import_block(),
            "Exercise 8: S3 Module": self.check_s3_module(),
            "Exercise 9: S3 Object": self.check_s3_object(),
            "Exercise 10: Ephemeral Resources": self.check_ephemeral_resources(),
            "Exercise 11: Database Setup": self.check_database_setup(),
            "Exercise 12: Outputs": self.check_outputs()
        }
        
        # Run terraform validate if terraform is available
        print(f"\n{INFO} Running terraform validate...")
        print("-------------------------------------------------------------------------------------")
        stdout, stderr, returncode = self.run_terraform_command(["validate"])
        if returncode == 0:
            print(f"{SUCCESS} Terraform configuration is valid")
        else:
            print(f"{FAILURE} Terraform configuration is invalid:")
            print(stderr)
        
        # Summary
        print("\n=====================================================================================")
        print(f"{INFO} Verification Summary")
        print("=====================================================================================")
        
        completed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for exercise, passed in results.items():
            print(f"{SUCCESS if passed else FAILURE} {exercise}")
        
        print("\n=====================================================================================")
        print(f"{INFO} Overall Progress: {completed}/{total} exercises completed successfully ({completed/total*100:.1f}%)")
        print("=====================================================================================")
        
        if completed == total:
            print(f"\n{SUCCESS} Congratulations! You have successfully completed all exercises!")
        else:
            print(f"\n{WARNING} You still have {total - completed} exercise(s) to complete or fix.")
        
        return completed, total


def main():
    """Main function to run the verification script."""
    print("\nTerraform Workshop Verifier")
    print("=====================================================================================")
    print("This script will verify your progress through the Terraform workshop exercises.")
    print("It checks for the presence and correctness of various Terraform resources and configurations.")
    
    # Get the directory to check (default is current directory)
    directory = "."
    
    # Create the verifier and run all checks
    verifier = TerraformVerifier(directory)
    verifier.run_all_checks()


if __name__ == "__main__":
    main()
