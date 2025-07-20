#!/bin/bash
# Migration script from Lightbox2 to GLightbox for TagOS Blog

echo "TagOS Blog: Migrating from Lightbox2 to GLightbox"
echo "================================================="

# Backup content directory
echo "Creating backup..."
cp -r content content_backup_$(date +%Y%m%d_%H%M%S)

# Find and replace lightbox2 references
echo "Updating shortcode references..."

# Replace gallery2 shortcode with glightbox-gallery
find content/ -name "*.md" -type f -exec sed -i 's/{{< gallery2 /{{< glightbox-gallery /g' {} \;

# Replace figure shortcode with glightbox-figure (if you were using custom figure)
find content/ -name "*.md" -type f -exec sed -i 's/{{< figure /{{< glightbox-figure /g' {} \;

# Update data-lightbox attributes to class="glightbox" in any manual HTML
find content/ -name "*.md" -type f -exec sed -i 's/data-lightbox="[^"]*"/class="glightbox"/g' {} \;

echo "Checking for manual lightbox2 references..."
grep -r "data-lightbox" content/ || echo "No manual lightbox2 references found"

echo "Checking for old gallery2 shortcodes..."
grep -r "gallery2" content/ || echo "No gallery2 shortcodes found"

echo ""
echo "Migration complete!"
echo ""
echo "Next steps:"
echo "1. Remove old lightbox2 CSS/JS from your layout files"
echo "2. Add GLightbox setup to your layouts/partials/head.html"
echo "3. Test your galleries: hugo server -D"
echo "4. Update any custom CSS classes if needed"
echo ""
echo "Backup created at: content_backup_$(date +%Y%m%d_%H%M%S)"