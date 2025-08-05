# 🔒 Security Checklist for Macro Tracker

## 🚨 Critical: Never Commit Sensitive Data

### ✅ API Keys & Secrets
- [ ] **OpenAI API Key**: Set via environment variable `OPENAI_API_KEY`
- [ ] **Database Credentials**: Use environment variables, never hardcode
- [ ] **JWT Secrets**: Use environment variables for signing keys
- [ ] **Third-party API Keys**: Store in environment variables

### ✅ SSH Keys & Certificates
- [ ] **SSH Private Keys**: Never commit `id_rsa`, `id_ed25519`, etc.
- [ ] **SSH Public Keys**: Only commit if explicitly needed for deployment
- [ ] **SSL Certificates**: Never commit `.crt`, `.pem`, `.p12` files
- [ ] **Keystores**: Never commit `.jks`, `.keystore` files

### ✅ Environment Variables
- [ ] **Development**: Use `.env` files (already in `.gitignore`)
- [ ] **Production**: Use environment variables or secure vaults
- [ ] **Testing**: Use separate test environment variables

## 🔧 Security Setup

### 1. Environment Variables Setup

```bash
# Create a .env file for local development
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env

# Or set in your shell profile
echo 'export OPENAI_API_KEY="sk-your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 2. Pre-commit Checks

Before committing, always check:

```bash
# Check for potential secrets in staged files
git diff --cached | grep -i "sk-"
git diff --cached | grep -i "api_key"
git diff --cached | grep -i "password"
git diff --cached | grep -i "secret"

# Check for SSH keys
git diff --cached | grep -i "BEGIN.*PRIVATE KEY"
git diff --cached | grep -i "ssh-rsa"
```

### 3. Git Hooks (Optional)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Check for potential secrets
if git diff --cached | grep -q -i "sk-"; then
    echo "❌ ERROR: Potential API key found in commit!"
    echo "Please remove any API keys before committing."
    exit 1
fi

if git diff --cached | grep -q -i "BEGIN.*PRIVATE KEY"; then
    echo "❌ ERROR: Potential private key found in commit!"
    echo "Please remove any private keys before committing."
    exit 1
fi

echo "✅ Security check passed"
```

## 🛡️ Protected Files

The following files are now protected by `.gitignore`:

### API Keys & Secrets
- `api-keys.txt`
- `secrets.txt`
- `*.key`
- `*.pem`
- `*secret*`
- `*password*`
- `*credential*`

### SSH Keys
- `id_rsa`
- `id_rsa.pub`
- `id_ed25519`
- `id_ed25519.pub`
- `*.ppk`
- `.ssh/`

### Environment Files
- `.env`
- `.env.*`
- `*.env`

### Configuration Files
- `config.json`
- `secrets.json`
- `credentials.json`
- `service-account.json`

## 🚨 Emergency Procedures

### If You Accidentally Commit Sensitive Data

1. **Immediate Action**:
   ```bash
   # Remove the file from git history
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch path/to/sensitive/file' \
     --prune-empty --tag-name-filter cat -- --all
   ```

2. **Rotate the Exposed Secret**:
   - Generate new API keys
   - Update environment variables
   - Notify team members

3. **Force Push** (if repository is shared):
   ```bash
   git push origin --force
   ```

## 📋 Daily Security Checklist

### Before Committing
- [ ] No API keys in code
- [ ] No passwords in code
- [ ] No private keys in code
- [ ] No database credentials in code
- [ ] No hardcoded URLs with credentials

### Before Pushing
- [ ] Run security checks
- [ ] Review diff for sensitive data
- [ ] Ensure `.env` files are not staged

### Weekly Review
- [ ] Check for any new sensitive files
- [ ] Review access permissions
- [ ] Update security documentation

## 🔍 Security Monitoring

### Automated Checks

Add to your CI/CD pipeline:

```yaml
# Example GitHub Actions security check
- name: Security Check
  run: |
    # Check for API keys
    if grep -r "sk-" . --exclude-dir=.git; then
      echo "❌ API keys found in code"
      exit 1
    fi
    
    # Check for private keys
    if grep -r "BEGIN.*PRIVATE KEY" . --exclude-dir=.git; then
      echo "❌ Private keys found in code"
      exit 1
    fi
```

## 📚 Best Practices

1. **Use Environment Variables**: Always use `process.env` or `System.getenv()`
2. **Use Secret Management**: Consider tools like HashiCorp Vault or AWS Secrets Manager
3. **Regular Audits**: Periodically review code for hardcoded secrets
4. **Team Training**: Ensure all team members understand security practices
5. **Documentation**: Keep security procedures up to date

## 🆘 Emergency Contacts

- **Repository Admin**: [Your Name]
- **Security Team**: [Contact Info]
- **API Provider**: OpenAI Support

---

**Remember**: Once sensitive data is committed and pushed, consider it compromised. Always rotate exposed secrets immediately. 