# Secure Lock Solutions - Complete Deployment & Configuration Guide

## Project Overview
**Website:** Secure Lock Solutions - Professional Locksmith Services  
**Domain:** securelocksmithsolution.com  
**Business Address:** 1100 Synergy, Irvine, CA 92614  
**Phone:** (714) 341-9244  
**Email:** securelocksmithsolution@gmail.com  
**Service Area:** Orange County, California  

---

## AWS Infrastructure Setup

### 1. AWS Account Details
- **AWS Account ID:** 863355752090
- **Region:** us-east-1 (N. Virginia)
- **CloudFront Distribution ID:** E1V93XZ8OKOUBS
- **CloudFront Domain:** dmcj253yfhn83.cloudfront.net
- **S3 Bucket Name:** secure-lock

### 2. S3 Bucket Configuration
**Bucket Name:** `secure-lock`  
**Region:** us-east-1  
**Versioning:** Disabled  
**Static Website Hosting:** Enabled (via CloudFront)

#### Bucket Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::secure-lock/*"
    }
  ]
}
```

**Applied:** Yes ✓

### 3. CloudFront Distribution
**Distribution ID:** E1V93XZ8OKOUBS  
**Domain Name:** dmcj253yfhn83.cloudfront.net  
**Status:** Deployed  
**Default Root Object:** index.html  
**Viewer Protocol Policy:** redirect-to-https  

#### Origin Configuration
- **Origin Domain:** secure-lock.s3.us-east-1.amazonaws.com
- **Origin Type:** S3
- **S3 Origin Config:** Custom Origin

#### Cache Behavior
- **Viewer Protocol Policy:** Redirect HTTP to HTTPS
- **Allowed Methods:** GET, HEAD
- **Cache Policy:** Default (Managed by CloudFront)

### 4. ACM Certificate
**Certificate ARN:** arn:aws:acm:us-east-1:863355752090:certificate/64bff34a-2d0d-4e33-a1bd-6d084317b635  
**Domain Name:** securelocksmithsolution.com  
**Status:** ISSUED ✓  
**Renewal:** Auto-renewal enabled

### 5. Route 53 Hosted Zone
**Hosted Zone ID:** Z09785141CQW36SLO2F3C  
**Domain:** securelocksmithsolution.com  

#### DNS Records
| Name | Type | Value | TTL |
|------|------|-------|-----|
| securelocksmithsolution.com | A | dmcj253yfhn83.cloudfront.net | 300 |
| securelocksmithsolution.com | AAAA | dmcj253yfhn83.cloudfront.net | 300 |

---

## Local Development Setup

### Prerequisites
- macOS (Zsh terminal)
- AWS CLI v2.15.59 or higher
- Python 3.11.8 or higher
- Text editor (VS Code recommended)

### Project Directory Structure
```
/Users/israelvaday/gothamwebstudio/secure_upd/
├── index.html                          # Main homepage
├── thank_you.html                      # Thank you/confirmation page
├── serv_form.html                      # Service request form
├── sitemap.xml                         # XML sitemap
├── Robots.txt                          # robots.txt file
├── assets/
│   ├── css/
│   │   ├── main.css
│   │   ├── images.css
│   │   └── fontawesome-all.min.css
│   ├── js/
│   │   ├── main.js
│   │   ├── jquery.min.js
│   │   ├── breakpoints.min.js
│   │   └── util.js
│   ├── sass/
│   │   └── main.scss
│   └── webfonts/
├── images/
│   ├── icons/
│   ├── banners/
│   └── cities/
├── DEPLOYMENT_GUIDE.md                # This file
└── [60+ service area pages]            # City/service pages

```

### AWS CLI Configuration
1. Install AWS CLI:
   ```bash
   aws --version  # Should show v2.15.59+
   ```

2. Configure credentials:
   ```bash
   aws configure
   ```
   When prompted, enter:
   - AWS Access Key ID: [Your access key]
   - AWS Secret Access Key: [Your secret key]
   - Default region: us-east-1
   - Default output format: json

3. Verify setup:
   ```bash
   aws s3 ls
   # Should output: 2025-12-31 17:13:17 secure-lock
   ```

---

## Deployment Process

### Manual Deployment Steps

#### 1. Sync Files to S3
```bash
cd /Users/israelvaday/gothamwebstudio/secure_upd
aws s3 sync . s3://secure-lock/ --exclude ".DS_Store" --exclude ".git*"
```

#### 2. Verify Files in S3
```bash
aws s3 ls s3://secure-lock/
# Should show all HTML files and assets directories
```

#### 3. Invalidate CloudFront Cache
```bash
aws cloudfront create-invalidation \
  --distribution-id E1V93XZ8OKOUBS \
  --paths "/*"
```

#### 4. Verify Deployment
```bash
# Check CloudFront status
aws cloudfront get-distribution \
  --id E1V93XZ8OKOUBS \
  --query 'Distribution.Status'
# Should output: Deployed

# Check distribution is enabled
aws cloudfront get-distribution \
  --id E1V93XZ8OKOUBS \
  --query 'Distribution.DistributionConfig.Enabled'
# Should output: True
```

### Automated Deployment (Optional)
Create a script `deploy.sh`:
```bash
#!/bin/bash
set -e

echo "🚀 Starting deployment..."

cd /Users/israelvaday/gothamwebstudio/secure_upd

echo "📦 Syncing files to S3..."
aws s3 sync . s3://secure-lock/ \
  --exclude ".DS_Store" \
  --exclude ".git*" \
  --delete

echo "🔄 Invalidating CloudFront cache..."
INVALIDATION_ID=$(aws cloudfront create-invalidation \
  --distribution-id E1V93XZ8OKOUBS \
  --paths "/*" \
  --query 'Invalidation.Id' \
  --output text)

echo "✅ Deployment complete!"
echo "Invalidation ID: $INVALIDATION_ID"
echo "Website: https://securelocksmithsolution.com"
```

Make executable:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## Business Information

### Contact Details
- **Primary Phone:** (714) 341-9244
- **Email:** securelocksmithsolution@gmail.com
- **Address:** 1100 Synergy, Irvine, CA 92614

### Operating Hours
- **Hours:** 24/7 (24 Hours / 7 Days a Week)
- **Emergency Service:** Always Available

### Service Categories
1. **Residential Services**
   - Emergency lockouts
   - Lock changes
   - Key duplication
   - Rekeying
   - Smart locks

2. **Commercial Services**
   - Access control systems
   - Master key systems
   - Door hardware
   - High-security locks

3. **Automotive Services**
   - Car lockouts
   - Key replacement
   - Ignition repair

4. **Mobile Locksmith Service**
   - Available throughout Orange County
   - Response time: 15-30 minutes
   - Fully equipped mobile units

### Service Areas (60+ Cities)
Anaheim, Irvine, Santa Ana, Huntington Beach, Costa Mesa, Fullerton, Newport Beach, Orange, and 52+ other Orange County cities. See `service-areas.html` for complete list.

---

## Website Features & Content

### Main Pages
1. **index.html** - Homepage with service overview, mobile locksmith section, shop location
2. **residential.html** - Residential locksmith services
3. **commercial.html** - Commercial security solutions
4. **automotive.html** - Automotive locksmith services
5. **service-areas.html** - Service area overview
6. **gallery.html** - Portfolio of completed work
7. **serv_form.html** - Service request form
8. **thank_you.html** - Confirmation page

### Key Sections Added
1. **Mobile Locksmith Service Section** (index.html)
   - Location: Before footer
   - Features:
     - Left side: Mobile service benefits and call button
     - Right side: Shop location with Google Maps
   - Height: Matched for visual balance

2. **Shop Location Section** (index.html)
   - Google Maps embed: 1100 Synergy, Irvine, CA 92614
   - Contact information displayed
   - Directions button

3. **Footer Updates**
   - Address added: 1100 Synergy, Irvine, CA 92614
   - Contact information
   - Hours: 24/7
   - Phone and email links

### Design Elements
- **Color Scheme:** Gold (#D4AF37) accents on professional background
- **Font Awesome Icons:** Used throughout for visual enhancement
- **Responsive Design:** Mobile-first approach with breakpoints for tablets/desktop
- **CSS Framework:** Custom CSS with Bootstrap grid system

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. 403 Forbidden / Access Denied
**Symptoms:** Website shows AccessDenied error, favicon.ico returns 403

**Causes & Solutions:**
```bash
# Check S3 bucket policy
aws s3api get-bucket-policy --bucket secure-lock

# Verify public access is allowed
aws s3api get-public-access-block --bucket secure-lock

# Check CloudFront default root object
aws cloudfront get-distribution \
  --id E1V93XZ8OKOUBS \
  --query 'DistributionConfig.DefaultRootObject'
# Must be: index.html
```

**Fix:**
```bash
# 1. Ensure bucket policy allows public read access
aws s3api put-bucket-policy --bucket secure-lock --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::secure-lock/*"
  }]
}'

# 2. Ensure CloudFront has default root object
aws cloudfront update-distribution \
  --id E1V93XZ8OKOUBS \
  --distribution-config file:///path/to/config.json \
  --if-match [ETAG]

# 3. Invalidate cache
aws cloudfront create-invalidation \
  --distribution-id E1V93XZ8OKOUBS \
  --paths "/*"
```

#### 2. Changes Not Appearing on Website
**Symptoms:** Updated files but changes not visible

**Solution:**
```bash
# Full cache invalidation
aws cloudfront create-invalidation \
  --distribution-id E1V93XZ8OKOUBS \
  --paths "/*"

# Also try hard browser refresh (Cmd+Shift+R or Ctrl+Shift+R)
```

#### 3. S3 Bucket Inaccessible
**Symptoms:** Can't list or sync files to S3

**Solution:**
```bash
# Check AWS credentials
aws sts get-caller-identity

# Test S3 access
aws s3 ls s3://secure-lock/

# If error, reconfigure AWS CLI
aws configure
```

#### 4. SSL/Certificate Issues
**Symptoms:** "Not Secure" warning or SSL errors

**Solution:**
```bash
# Check certificate status
aws acm list-certificates \
  --region us-east-1 \
  --query 'CertificateSummaryList[?DomainName==`securelocksmithsolution.com`]'

# Certificate should show Status: ISSUED
# Auto-renewal is enabled

# Check CloudFront viewer certificate
aws cloudfront get-distribution \
  --id E1V93XZ8OKOUBS \
  --query 'DistributionConfig.ViewerCertificate'
```

#### 5. DNS/Domain Not Resolving
**Symptoms:** Domain not accessible, "Could not find host"

**Solution:**
```bash
# Check Route 53 records
aws route53 list-resource-record-sets \
  --hosted-zone-id Z09785141CQW36SLO2F3C

# Both A and AAAA records should point to CloudFront domain:
# dmcj253yfhn83.cloudfront.net

# DNS propagation can take up to 48 hours for changes
```

---

## Performance & Optimization

### CloudFront Caching
- **Default TTL:** 86400 seconds (24 hours)
- **Invalidation:** Done after each deployment
- **Cache Statistics:** Available in AWS Console

### S3 Optimization
- **Storage Class:** Standard (suitable for website hosting)
- **Versioning:** Disabled (enable if needed for rollback)
- **Lifecycle Policies:** None configured

### Future Optimizations
1. Enable S3 versioning for rollback capability
2. Add CloudFront Lambda@Edge for advanced caching
3. Enable S3 Transfer Acceleration if needed
4. Set up CloudWatch monitoring and alarms
5. Implement WAF (Web Application Firewall)

---

## Security Considerations

### Current Security Measures
✅ HTTPS/SSL enabled via ACM certificate  
✅ S3 bucket not publicly writable (read-only)  
✅ CloudFront acts as CDN/security layer  
✅ No direct S3 website endpoint used  

### Recommended Additional Security
1. **Enable S3 versioning** - For data protection
2. **Enable CloudTrail logging** - Audit AWS API calls
3. **Set up AWS WAF** - Protect against common web exploits
4. **Enable MFA** - For AWS account access
5. **Use IAM roles** - Restrict S3 access permissions
6. **Enable S3 encryption** - Server-side encryption (SSE-S3)

### Access Control
- **S3 Bucket Policy:** Public read-only
- **CloudFront Origin Access:** Direct S3 access
- **Route 53:** Publicly accessible DNS
- **ACM Certificate:** Valid for securelocksmithsolution.com

---

## Monitoring & Maintenance

### Regular Checks
```bash
# Check CloudFront distribution status (monthly)
aws cloudfront get-distribution --id E1V93XZ8OKOUBS

# Check S3 bucket size (monthly)
aws s3 ls s3://secure-lock/ --recursive --summarize

# Check SSL certificate expiration (quarterly)
aws acm list-certificates --region us-east-1

# Check DNS records (quarterly)
aws route53 list-resource-record-sets --hosted-zone-id Z09785141CQW36SLO2F3C
```

### CloudFront Metrics
- **Requests:** Monitor in AWS Console
- **Bytes Downloaded:** Check bandwidth usage
- **Cache Hit Rate:** Should be >80%
- **4xx Errors:** Should be near 0% (excluding 403 for non-existent files)
- **5xx Errors:** Should be 0%

### S3 Metrics
- **Storage Used:** Monitor for cost
- **Request Rate:** High volume expected
- **HTTP 200:** Successful requests
- **HTTP 403:** Access denied (should be none with current policy)
- **HTTP 404:** Not found (check for broken links)

---

## Environment Variables & Secrets

### AWS CLI Environment Variables
```bash
export AWS_REGION=us-east-1
export AWS_PROFILE=default
export AWS_PAGER=""  # Disable pager for easier scripting
```

### Important IDs (Do Not Commit)
- **AWS Account ID:** 863355752090
- **CloudFront ID:** E1V93XZ8OKOUBS
- **S3 Bucket:** secure-lock
- **Hosted Zone ID:** Z09785141CQW36SLO2F3C
- **ACM Certificate ARN:** arn:aws:acm:us-east-1:863355752090:certificate/64bff34a-2d0d-4e33-a1bd-6d084317b635

### Business Variables (Used in Site Content)
```
BUSINESS_NAME=Secure Lock Solutions
PHONE=(714) 341-9244
EMAIL=securelocksmithsolution@gmail.com
ADDRESS=1100 Synergy, Irvine, CA 92614
DOMAIN=securelocksmithsolution.com
SERVICE_AREA=Orange County, California
HOURS=24/7 (24 Hours / 7 Days a Week)
EMERGENCY_SERVICE=Always Available
RESPONSE_TIME=15-30 minutes
```

---

## Future Development

### Potential Enhancements
1. **Contact Form Backend**
   - Integrate with email service (SES)
   - Add database for lead tracking
   - Implement form validation

2. **Blog System**
   - Migrate from static HTML to CMS
   - Add categories and tags
   - Enable comments

3. **Booking System**
   - Calendar integration
   - Real-time availability
   - Automated confirmations

4. **Mobile App**
   - iOS and Android apps
   - Push notifications
   - Location-based services

5. **SEO Enhancements**
   - Add structured data (Schema.org)
   - Improve internal linking
   - Add meta descriptions
   - Create XML sitemaps for each service

### Migration Path
- **Current:** Static HTML site on CloudFront + S3
- **Next:** Add backend with Lambda + API Gateway
- **Future:** Full CMS integration with headless architecture

---

## Quick Reference Commands

```bash
# Deploy changes
cd /Users/israelvaday/gothamwebstudio/secure_upd
aws s3 sync . s3://secure-lock/ --exclude ".DS_Store" --exclude ".git*"
aws cloudfront create-invalidation --distribution-id E1V93XZ8OKOUBS --paths "/*"

# Check status
aws cloudfront get-distribution --id E1V93XZ8OKOUBS --query 'Distribution.Status'
aws s3api head-bucket --bucket secure-lock

# View CloudFront cache statistics
aws cloudfront get-distribution-statistics --id E1V93XZ8OKOUBS

# Check recent invalidations
aws cloudfront list-invalidations --distribution-id E1V93XZ8OKOUBS --max-items 5

# View S3 bucket contents
aws s3 ls s3://secure-lock/ --recursive

# Test DNS resolution
nslookup securelocksmithsolution.com
```

---

## Support & Escalation

### Common Contact Points
1. **AWS Support:** https://console.aws.amazon.com/support
2. **Domain Registrar:** [Where domain is registered]
3. **Email Support:** securelocksmithsolution@gmail.com
4. **Phone Support:** (714) 341-9244

### Documentation Links
- [AWS CloudFront Documentation](https://docs.aws.amazon.com/cloudfront/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS Route 53 Documentation](https://docs.aws.amazon.com/route53/)
- [AWS ACM Documentation](https://docs.aws.amazon.com/acm/)

---

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-12-31 | 1.0 | Initial documentation, CloudFront + S3 setup | GitHub Copilot |
| | | Mobile locksmith service section added | |
| | | Shop location with Google Maps integration | |
| | | Address (1100 Synergy) added to footer | |

---

**Last Updated:** December 31, 2025  
**Website:** https://securelocksmithsolution.com  
**Status:** ✅ Live and Operational
