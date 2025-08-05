#!/bin/bash

echo "🔒 Security Check for Macro Tracker"
echo "==================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check for patterns
check_pattern() {
    local pattern=$1
    local description=$2
    local found=false
    
    # Check staged files
    if git diff --cached | grep -q -i "$pattern"; then
        echo -e "${RED}❌ $description found in staged files${NC}"
        git diff --cached | grep -i "$pattern" | head -5
        found=true
    fi
    
    # Check working directory (exclude documentation and example files)
    if grep -r -i "$pattern" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=target 2>/dev/null | grep -v ".gitignore" | grep -v "SECURITY_CHECKLIST.md" | grep -v "security-check.sh" | grep -v "LANGGRAPH_SETUP.md" | grep -v "setup-api-key.sh" | grep -v "setup-openai.sh" | grep -v "README.md" | grep -v "DEVELOPMENT.md"; then
        echo -e "${YELLOW}⚠️  $description found in working directory${NC}"
        grep -r -i "$pattern" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=target 2>/dev/null | grep -v ".gitignore" | grep -v "SECURITY_CHECKLIST.md" | grep -v "security-check.sh" | grep -v "LANGGRAPH_SETUP.md" | grep -v "setup-api-key.sh" | grep -v "setup-openai.sh" | grep -v "README.md" | grep -v "DEVELOPMENT.md" | head -5
        found=true
    fi
    
    if [ "$found" = false ]; then
        echo -e "${GREEN}✅ No $description found${NC}"
    fi
    
    return $([ "$found" = true ] && echo 1 || echo 0)
}

# Initialize error counter
errors=0

echo ""
echo "🔍 Checking for sensitive data..."

# Check for API keys
check_pattern "sk-[a-zA-Z0-9]{48}" "OpenAI API keys"
if [ $? -eq 1 ]; then ((errors++)); fi

# Check for other API keys (exclude legitimate config patterns)
if grep -r -i "api_key" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=target 2>/dev/null | grep -v "LANGGRAPH_SETUP.md" | grep -v "README.md" | grep -v "DEVELOPMENT.md" | grep -v "SECURITY_CHECKLIST.md" | grep -v "security-check.sh" | grep -v "setup-api-key.sh" | grep -v "setup-openai.sh" | grep -v "\${.*API_KEY" | grep -v "api-key:"; then
    echo -e "${YELLOW}⚠️  API keys found in working directory${NC}"
    grep -r -i "api_key" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=target 2>/dev/null | grep -v "LANGGRAPH_SETUP.md" | grep -v "README.md" | grep -v "DEVELOPMENT.md" | grep -v "SECURITY_CHECKLIST.md" | grep -v "security-check.sh" | grep -v "setup-api-key.sh" | grep -v "setup-openai.sh" | grep -v "\${.*API_KEY" | grep -v "api-key:" | head -3
    ((errors++))
else
    echo -e "${GREEN}✅ No API keys found${NC}"
fi

# Check for passwords (exclude legitimate code patterns)
if grep -r -i "password" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=target 2>/dev/null | grep -v "LANGGRAPH_SETUP.md" | grep -v "README.md" | grep -v "DEVELOPMENT.md" | grep -v "SECURITY_CHECKLIST.md" | grep -v "security-check.sh" | grep -v "setup-api-key.sh" | grep -v "setup-openai.sh" | grep -v "private String password" | grep -v "getPassword" | grep -v "setPassword" | grep -v "password:" | grep -v "password =" | grep -v "String password" | grep -v "*password*"; then
    echo -e "${YELLOW}⚠️  Passwords found in working directory${NC}"
    grep -r -i "password" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=target 2>/dev/null | grep -v "LANGGRAPH_SETUP.md" | grep -v "README.md" | grep -v "DEVELOPMENT.md" | grep -v "SECURITY_CHECKLIST.md" | grep -v "security-check.sh" | grep -v "setup-api-key.sh" | grep -v "setup-openai.sh" | grep -v "private String password" | grep -v "getPassword" | grep -v "setPassword" | grep -v "password:" | grep -v "password =" | grep -v "String password" | grep -v "*password*" | head -3
    ((errors++))
else
    echo -e "${GREEN}✅ No passwords found${NC}"
fi

# Check for secrets
check_pattern "secret" "Secrets"
if [ $? -eq 1 ]; then ((errors++)); fi

# Check for private keys
check_pattern "BEGIN.*PRIVATE KEY" "Private keys"
if [ $? -eq 1 ]; then ((errors++)); fi

# Check for SSH keys
check_pattern "ssh-rsa" "SSH public keys"
if [ $? -eq 1 ]; then ((errors++)); fi

# Check for database credentials (only in actual config files)
if grep -r -i "jdbc:" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=target 2>/dev/null | grep -v "LANGGRAPH_SETUP.md" | grep -v "README.md" | grep -v "DEVELOPMENT.md" | grep -v "SECURITY_CHECKLIST.md" | grep -v "security-check.sh" | grep -v "setup-api-key.sh" | grep -v "setup-openai.sh" | grep -v "jdbc:h2:mem:" | grep -v "jdbc:h2:file:"; then
    echo -e "${YELLOW}⚠️  Database URLs found in working directory${NC}"
    grep -r -i "jdbc:" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=target 2>/dev/null | grep -v "LANGGRAPH_SETUP.md" | grep -v "README.md" | grep -v "DEVELOPMENT.md" | grep -v "SECURITY_CHECKLIST.md" | grep -v "security-check.sh" | grep -v "setup-api-key.sh" | grep -v "setup-openai.sh" | grep -v "jdbc:h2:mem:" | grep -v "jdbc:h2:file:" | head -3
    ((errors++))
else
    echo -e "${GREEN}✅ No database URLs found${NC}"
fi

# Check for hardcoded credentials (only in actual code/config)
if grep -r -i "username.*password\|password.*username" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=target 2>/dev/null | grep -v "LANGGRAPH_SETUP.md" | grep -v "README.md" | grep -v "DEVELOPMENT.md" | grep -v "SECURITY_CHECKLIST.md" | grep -v "security-check.sh" | grep -v "setup-api-key.sh" | grep -v "setup-openai.sh" | grep -v "String username.*String password" | grep -v "String password.*String username"; then
    echo -e "${YELLOW}⚠️  Hardcoded credentials found in working directory${NC}"
    grep -r -i "username.*password\|password.*username" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=target 2>/dev/null | grep -v "LANGGRAPH_SETUP.md" | grep -v "README.md" | grep -v "DEVELOPMENT.md" | grep -v "SECURITY_CHECKLIST.md" | grep -v "security-check.sh" | grep -v "setup-api-key.sh" | grep -v "setup-openai.sh" | grep -v "String username.*String password" | grep -v "String password.*String username" | head -3
    ((errors++))
else
    echo -e "${GREEN}✅ No hardcoded credentials found${NC}"
fi

echo ""
echo "📁 Checking for sensitive files..."

# Check for .env files in staging
if git diff --cached --name-only | grep -q "\.env"; then
    echo -e "${RED}❌ .env files found in staging area${NC}"
    git diff --cached --name-only | grep "\.env"
    ((errors++))
else
    echo -e "${GREEN}✅ No .env files in staging area${NC}"
fi

# Check for key files
if git diff --cached --name-only | grep -E "\.(key|pem|p12|pfx|crt|cert|cer)$"; then
    echo -e "${RED}❌ Certificate/key files found in staging area${NC}"
    git diff --cached --name-only | grep -E "\.(key|pem|p12|pfx|crt|cert|cer)$"
    ((errors++))
else
    echo -e "${GREEN}✅ No certificate/key files in staging area${NC}"
fi

echo ""
echo "🔧 Environment Check..."

# Check if OPENAI_API_KEY is set
if [ -n "$OPENAI_API_KEY" ]; then
    echo -e "${GREEN}✅ OPENAI_API_KEY is set${NC}"
else
    echo -e "${YELLOW}⚠️  OPENAI_API_KEY is not set${NC}"
    echo "   Run: export OPENAI_API_KEY='sk-your-api-key-here'"
fi

# Check for .env file
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ .env file exists${NC}"
else
    echo -e "${YELLOW}⚠️  No .env file found${NC}"
    echo "   Consider creating one for local development"
fi

echo ""
echo "📊 Summary:"

if [ $errors -eq 0 ]; then
    echo -e "${GREEN}✅ Security check passed! Safe to commit.${NC}"
    exit 0
else
    echo -e "${RED}❌ Security check failed! Found $errors potential issues.${NC}"
    echo ""
    echo "🚨 Please fix the issues above before committing."
    echo "📖 See SECURITY_CHECKLIST.md for more information."
    exit 1
fi 