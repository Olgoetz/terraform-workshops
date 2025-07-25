# Terraform Workshop Verifier

This script helps you verify your progress through the Terraform workshop exercises. It checks your Terraform configuration files for the presence and correctness of various resources and configurations.

## Prerequisites

- Python 3.6+
- pip (Python package manager)

## Installation

1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the script from the directory containing your Terraform files:

```bash
./workshop_verifier.py
```

The script will check each exercise and provide feedback on what's correct and what needs attention.

## What the Script Checks

The script verifies the following aspects of your Terraform configuration:

1. **File Structure**: Checks if all required files exist (main.tf, variables.tf, outputs.tf, etc.)
2. **Terraform Cloud Configuration**: Verifies the Terraform Cloud backend setup
3. **Provider Configuration**: Checks AWS provider settings and default tags
4. **Variables**: Validates variable definitions and validation rules
5. **Data Sources**: Verifies AWS data sources for VPC, subnets, and caller identity
6. **Locals**: Checks local value definitions for naming conventions
7. **For Each and Conditionals**: Validates SNS topic creation with for_each and conditional expressions
8. **Import Block**: Checks the import block for SQS queue
9. **S3 Module**: Verifies S3 bucket module configuration
10. **S3 Object**: Checks S3 object creation from local file
11. **Ephemeral Resources**: Validates ephemeral resources for secret management
12. **Database Setup**: Checks RDS instance, security group, and subnet group configuration
13. **Outputs**: Verifies output definitions

## Troubleshooting

If the script reports issues with your configuration:

1. Read the error messages carefully
2. Compare your code with the examples in the instructions
3. Make the necessary corrections
4. Run the script again to verify your changes

## Note

This script is designed to help you learn and doesn't replace understanding the concepts. Make sure you understand why each configuration is needed rather than just making the script pass.
