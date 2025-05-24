"""
Simple setup and test script for Claude 4 Autonomous Code Review
"""
import os
from pathlib import Path

def setup_project():
    """Setup the project with API key"""
    project_root = Path(__file__).parent.parent.parent
    env_file = project_root / ".env"
    
    print("Claude 4 Autonomous Code Review Setup")
    print("=" * 40)
    
    if env_file.exists():
        print(f"✅ Found .env file at: {env_file}")
    else:
        print(f"❌ No .env file found at: {env_file}")
        print("\nTo get your Anthropic API key:")
        print("1. Go to https://console.anthropic.com/")
        print("2. Sign up/login and create an API key")
        print("3. Copy the key and paste it below")
        print("")
        
        api_key = input("Enter your Anthropic API key: ").strip()
        if api_key:
            with open(env_file, 'w') as f:
                f.write(f"ANTHROPIC_API_KEY={api_key}\n")
            print(f"✅ Created .env file with API key")
        else:
            print("❌ No API key provided")
            return False
    
    return True

def test_basic_functionality():
    """Test basic functionality with a simple query"""
    print("\nTesting basic functionality...")
    
    try:
        # Set environment variable for this test
        from dotenv import load_dotenv
        load_dotenv()
        
        from claude4_autonomous_code_review.claude4_client import Claude4Client
        
        # Test with development model (cheap)
        client = Claude4Client(use_production_model=False)
        print(f"✅ Successfully initialized Claude4Client with model: {client.model}")
        
        # Test file upload
        test_file = Path(__file__)
        file_id = client.upload_file(test_file)
        print(f"✅ Successfully uploaded test file: {file_id}")
        
        # Test basic message
        message = client.create_analysis_message(
            "Please provide a brief analysis of this Python file.",
            file_references=[file_id]
        )
        print(f"✅ Successfully created analysis message")
        print(f"Response preview: {str(message.content)[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def main():
    """Main setup and test function"""
    if setup_project():
        if test_basic_functionality():
            print("\n🎉 Setup complete! You can now run:")
            print("poetry run python -m src.claude4_autonomous_code_review.main . --goals 'Test optimization'")
        else:
            print("\n❌ Setup incomplete - please check your API key")
    else:
        print("\n❌ Setup failed")

if __name__ == "__main__":
    main()
