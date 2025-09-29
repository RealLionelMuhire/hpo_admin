# CKEditor Image Editing Guide

## Overview
Your GameContent model now has enhanced CKEditor integration with comprehensive image editing capabilities. Users can add, edit, resize, and style images directly within the content editor.

## Image Editing Features ✨

### 1. **Adding Images** 📷
- **Upload Button**: Click the "Image" button in the toolbar
- **Drag & Drop**: Drag images directly into the editor
- **Paste**: Copy and paste images from clipboard
- **Browse**: Upload from your computer via file browser

### 2. **Image Editing While Writing** ✏️
- **Double-click** any image to open the Image Properties dialog
- **Right-click** images for context menu with editing options
- **Hover** over images to see resize handles
- **Select** and use toolbar buttons for formatting

### 3. **Image Styling Options** 🎨

#### **Alignment**
- `image-left`: Float image to the left with text wrapping
- `image-center`: Center image with block display
- `image-right`: Float image to the right with text wrapping

#### **Size Controls**
- **Drag corners** to resize proportionally
- **Set exact dimensions** in Image Properties dialog
- **Responsive**: Images automatically scale on mobile

#### **Advanced Properties**
- **Alt text** for accessibility
- **Title tooltips** for additional information
- **CSS classes** for custom styling
- **Border and spacing** controls

### 4. **Upload Locations** 📁
Images are automatically saved to:
```
media/
├── uploads/           # CKEditor uploads
│   ├── 2025/09/29/   # Date-organized folders
│   └── thumbnails/   # Auto-generated thumbnails
└── images/           # Additional image storage
```

### 5. **Supported Formats** 📋
- **JPEG/JPG** - Photos and complex images
- **PNG** - Images with transparency
- **GIF** - Animated images (basic support)
- **WebP** - Modern web format
- **SVG** - Vector graphics (with restrictions)

## How to Use Image Editing

### **Basic Workflow:**
1. **Add Content**: Start typing your game content
2. **Insert Image**: Click Image button or drag/drop
3. **Edit Inline**: Double-click image to modify properties
4. **Resize**: Drag corners to adjust size
5. **Align**: Use alignment classes or toolbar buttons
6. **Continue Writing**: Keep editing text around images

### **Advanced Editing:**
1. **Image Properties Dialog**:
   - URL/Source path
   - Alternative text
   - Width/Height dimensions
   - CSS classes
   - Margins and spacing

2. **Context Menu** (Right-click):
   - Cut/Copy/Paste
   - Image Properties
   - Remove Image
   - Alignment options

3. **Keyboard Shortcuts**:
   - `Ctrl+C` - Copy selected image
   - `Ctrl+V` - Paste image
   - `Delete` - Remove selected image
   - `Ctrl+Z` - Undo image changes

## CSS Classes Available

### **Alignment Classes:**
```css
.image-left     /* Float left with text wrap */
.image-center   /* Center with block display */
.image-right    /* Float right with text wrap */
```

### **Caption Support:**
```css
.image-captioned    /* Enables figure/figcaption */
```

### **Custom Styling:**
Images automatically get hover effects and responsive behavior.

## Example Usage

### **Educational Content with Images:**
```html
<h2>Rwanda's Geography</h2>
<p>Rwanda is known as the "Land of a Thousand Hills"...</p>

<img src="/media/uploads/2025/09/29/rwanda-hills.jpg" 
     alt="Beautiful hills of Rwanda" 
     class="image-center"
     style="width: 80%; max-width: 600px;">

<p>The mountainous terrain creates...</p>
```

### **Image with Caption:**
```html
<figure class="image-captioned">
    <img src="/media/uploads/wildlife.jpg" alt="Mountain Gorilla">
    <figcaption>Mountain Gorillas in Volcanoes National Park</figcaption>
</figure>
```

## Technical Details

### **Upload Configuration:**
- **Max file size**: 10MB (configurable)
- **Storage path**: `media/uploads/`
- **URL pattern**: `/media/uploads/filename.jpg`
- **Thumbnail generation**: Automatic with Pillow

### **Security Features:**
- File type validation
- Size limits
- Malicious file detection
- Secure filename generation

### **Performance:**
- Automatic image optimization
- Responsive image serving
- CDN-ready URLs
- Efficient storage organization

## Troubleshooting

### **Common Issues:**

1. **"Upload failed"**
   - Check file size (< 10MB)
   - Verify file format is supported
   - Ensure media directory permissions

2. **"Image not displaying"**
   - Run `python manage.py collectstatic`
   - Check MEDIA_URL configuration
   - Verify image file exists

3. **"Resize not working"**
   - Clear browser cache
   - Check if JavaScript is enabled
   - Verify CKEditor plugins are loaded

### **Admin Actions:**
```bash
# Collect static files (includes CKEditor assets)
python manage.py collectstatic

# Check media directory permissions
ls -la media/uploads/

# View uploaded files
find media/uploads/ -name "*.jpg" -o -name "*.png"
```

## Best Practices 🏆

1. **Image Optimization**:
   - Use appropriate file formats
   - Compress images before upload
   - Consider WebP for better performance

2. **Accessibility**:
   - Always add alt text
   - Use descriptive filenames
   - Provide captions when helpful

3. **Content Organization**:
   - Use consistent image sizes
   - Align images appropriately
   - Balance text and images

4. **Mobile Responsiveness**:
   - Test on different screen sizes
   - Use percentage widths
   - Avoid fixed pixel dimensions

## Summary
✅ **Upload images** directly in the editor  
✅ **Edit properties** while writing content  
✅ **Resize and align** with visual controls  
✅ **Style with CSS classes** for consistency  
✅ **Responsive design** for all devices  
✅ **Secure file handling** with validation  

Your GameContent now supports rich, image-enhanced educational content that can be edited seamlessly while writing! 🎓📚
