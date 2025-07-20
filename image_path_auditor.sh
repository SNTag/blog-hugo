#!/bin/bash
# Hugo Image Path Auditor - TagOS Blog Maintenance
# Scans content for image references and standardizes paths

# Set colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "TagOS Blog Image Path Auditor"
echo "============================="

# Check if we're in a Hugo project
if [ ! -f "config.toml" ] && [ ! -f "config.yaml" ] && [ ! -f "hugo.toml" ]; then
    echo -e "${RED}Error: Not in a Hugo project directory${NC}"
    exit 1
fi

# Create directories if they don't exist
mkdir -p static/images
mkdir -p content/photos

echo -e "${YELLOW}Scanning for image references...${NC}"

# Find all markdown files and check for image patterns
find content/ -name "*.md" -exec grep -l "\!\[.*\](" {} \; | while read file; do
    echo -e "\n${GREEN}Checking: $file${NC}"
    
    # Look for different image reference patterns
    grep -n "\!\[.*\](" "$file" | while IFS=: read line_num image_ref; do
        echo "  Line $line_num: $image_ref"
        
        # Check if image starts with relative paths that might be broken
        if echo "$image_ref" | grep -q "\.\./"; then
            echo -e "    ${RED}⚠ Contains relative path - may be broken${NC}"
        fi
        
        # Check if image starts with /images/ (our standard)
        if echo "$image_ref" | grep -q "](/images/"; then
            echo -e "    ${GREEN}✓ Uses standard /images/ path${NC}"
        fi
        
        # Check if image starts with /photos/ 
        if echo "$image_ref" | grep -q "](/photos/"; then
            echo -e "    ${YELLOW}~ Uses /photos/ path - consider standardizing${NC}"
        fi
    done
done

echo -e "\n${YELLOW}Checking static directory structure...${NC}"

# Check what's in static/
if [ -d "static" ]; then
    echo "Static directory contents:"
    ls -la static/
    
    if [ -d "static/images" ]; then
        echo -e "${GREEN}✓ /images/ directory exists${NC}"
        echo "Image count: $(find static/images -type f | wc -l)"
    else
        echo -e "${YELLOW}⚠ /images/ directory missing${NC}"
    fi
    
    if [ -d "static/photos" ]; then
        echo -e "${GREEN}✓ /photos/ directory exists${NC}"
        echo "Photo count: $(find static/photos -type f | wc -l)"
    fi
else
    echo -e "${RED}⚠ Static directory missing${NC}"
fi

echo -e "\n${YELLOW}Recommendations:${NC}"
echo "1. Standardize all images to use /images/ path"
echo "2. Move any /photos/ content to /images/ if needed"
echo "3. Update markdown files to use consistent paths"
echo "4. Consider using Hugo's image processing features"

echo -e "\n${GREEN}Scan complete!${NC}"