// Game Content Form JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const subtopicsInput = document.getElementById('id_subtopics_input');
    
    if (subtopicsInput) {
        // Create preview area
        const previewDiv = document.createElement('div');
        previewDiv.className = 'subtopics-preview';
        previewDiv.innerHTML = '<h4>Subtopics Preview:</h4><div class="preview-content"></div>';
        subtopicsInput.parentNode.appendChild(previewDiv);
        
        const previewContent = previewDiv.querySelector('.preview-content');
        
        // Function to update preview
        function updatePreview() {
            const value = subtopicsInput.value.trim();
            if (value) {
                const subtopics = value.split(',').map(s => s.trim()).filter(s => s);
                if (subtopics.length > 0) {
                    previewContent.innerHTML = subtopics.map(subtopic => 
                        `<span class="subtopic-tag">${subtopic}</span>`
                    ).join('');
                } else {
                    previewContent.innerHTML = '<span class="subtopic-tag empty">No valid subtopics</span>';
                }
            } else {
                previewContent.innerHTML = '<span class="subtopic-tag empty">No subtopics added</span>';
            }
        }
        
        // Update preview on input
        subtopicsInput.addEventListener('input', updatePreview);
        
        // Initial preview update
        updatePreview();
        
        // Add helper text for better UX
        const helpText = document.createElement('div');
        helpText.className = 'help-text';
        helpText.innerHTML = `
            <strong>Tips for adding subtopics:</strong><br>
            • Separate multiple subtopics with commas<br>
            • Example: "Ancient History, Modern History, Independence"<br>
            • Each subtopic should be descriptive and concise<br>
            • Avoid duplicates within the same content item
        `;
        subtopicsInput.parentNode.appendChild(helpText);
    }
    
    // Content type specific styling
    const contentTypeField = document.getElementById('id_content_type');
    if (contentTypeField) {
        function updateContentTypeStyle() {
            const formRows = document.querySelectorAll('.form-row');
            formRows.forEach(row => {
                row.classList.remove('content-type-educational', 'content-type-historical', 
                                  'content-type-cultural', 'content-type-scientific');
            });
            
            const selectedType = contentTypeField.value;
            if (selectedType) {
                formRows.forEach(row => {
                    row.classList.add(`content-type-${selectedType}`);
                });
            }
        }
        
        contentTypeField.addEventListener('change', updateContentTypeStyle);
        updateContentTypeStyle(); // Initial call
    }
    
    // Auto-capitalize topic and subtopics
    const topicField = document.getElementById('id_topic');
    if (topicField) {
        topicField.addEventListener('blur', function() {
            this.value = this.value.replace(/\b\w/g, l => l.toUpperCase());
        });
    }
    
    if (subtopicsInput) {
        subtopicsInput.addEventListener('blur', function() {
            const subtopics = this.value.split(',').map(s => 
                s.trim().replace(/\b\w/g, l => l.toUpperCase())
            ).filter(s => s);
            this.value = subtopics.join(', ');
            updatePreview();
        });
    }
    
    // Form validation before submit
    const form = document.querySelector('form');
    if (form && subtopicsInput) {
        form.addEventListener('submit', function(e) {
            const subtopicsValue = subtopicsInput.value.trim();
            if (subtopicsValue) {
                const subtopics = subtopicsValue.split(',').map(s => s.trim()).filter(s => s);
                const uniqueSubtopics = [...new Set(subtopics)];
                
                if (subtopics.length !== uniqueSubtopics.length) {
                    alert('Warning: You have duplicate subtopics. Duplicates will be removed.');
                    subtopicsInput.value = uniqueSubtopics.join(', ');
                }
                
                // Check for overly long subtopics
                const longSubtopics = subtopics.filter(s => s.length > 50);
                if (longSubtopics.length > 0) {
                    if (!confirm(`Some subtopics are quite long (${longSubtopics.join(', ')}). Continue anyway?`)) {
                        e.preventDefault();
                        return false;
                    }
                }
            }
        });
    }
});
