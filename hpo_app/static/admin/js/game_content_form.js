// Game Content Form JavaScript for Multiple Subtopics

document.addEventListener('DOMContentLoaded', function() {
    // Wait for Django admin to fully load
    setTimeout(function() {
        initializeSubtopicsInterface();
    }, 500);
});

let subtopicsData = [];

function initializeSubtopicsInterface() {
    // Find the additional_subtopics hidden field
    const hiddenField = document.getElementById('id_additional_subtopics');
    if (!hiddenField) {
        console.log('Hidden field #id_additional_subtopics not found');
        return;
    }

    // Check if interface already exists
    if (document.querySelector('.subtopics-dynamic-interface')) {
        return;
    }

    // Load existing data
    loadExistingSubtopics();

    // Create the dynamic interface
    createSubtopicsInterface(hiddenField);

    // Setup form submission handler
    setupFormSubmission();
}

function loadExistingSubtopics() {
    const hiddenField = document.getElementById('id_additional_subtopics');
    if (hiddenField && hiddenField.value) {
        try {
            subtopicsData = JSON.parse(hiddenField.value);
        } catch (e) {
            console.error('Error parsing existing subtopics data:', e);
            subtopicsData = [];
        }
    }
}

function createSubtopicsInterface(hiddenField) {
    // Create main container
    const container = document.createElement('div');
    container.className = 'subtopics-dynamic-interface';
    container.innerHTML = `
        <div class="subtopics-header">
            <h3 style="color: #333; margin-bottom: 15px;">Additional Subtopics</h3>
            <p style="color: #666; margin-bottom: 15px;">
                Add multiple subtopics with their own information. The main subtopic (above) is automatically included.
            </p>
        </div>
        <div id="dynamic-subtopics-container"></div>
        <button type="button" id="add-subtopic-btn" class="add-subtopic-btn">
            + Add New Subtopic
        </button>
    `;

    // Find the best place to insert (after the info field or before the hidden field)
    const infoField = document.querySelector('.field-info');
    const hiddenFieldContainer = document.querySelector('.field-additional_subtopics');
    
    if (infoField) {
        infoField.parentNode.insertBefore(container, infoField.nextSibling);
    } else if (hiddenFieldContainer) {
        hiddenFieldContainer.parentNode.insertBefore(container, hiddenFieldContainer);
        hiddenFieldContainer.style.display = 'none'; // Hide the raw field
    } else {
        // Fallback: append to form
        const form = hiddenField.closest('form');
        if (form) {
            form.appendChild(container);
        }
    }

    // Setup event handlers
    document.getElementById('add-subtopic-btn').addEventListener('click', addSubtopic);
    
    // Initial render
    renderSubtopics();
}

function addSubtopic() {
    subtopicsData.push({
        subtopic: '',
        info: ''
    });
    renderSubtopics();
    updateHiddenField();
    
    // Focus on the new subtopic name field
    setTimeout(() => {
        const newIndex = subtopicsData.length - 1;
        const newField = document.getElementById(`subtopic-name-${newIndex}`);
        if (newField) {
            newField.focus();
        }
    }, 100);
}

function removeSubtopic(index) {
    subtopicsData.splice(index, 1);
    renderSubtopics();
    updateHiddenField();
}

function renderSubtopics() {
    const container = document.getElementById('dynamic-subtopics-container');
    if (!container) return;

    container.innerHTML = '';

    if (subtopicsData.length === 0) {
        container.innerHTML = `
            <div class="no-subtopics" style="
                padding: 20px; 
                text-align: center; 
                background: #f9f9f9; 
                border: 1px dashed #ccc; 
                border-radius: 4px; 
                color: #666; 
                font-style: italic;
                margin-bottom: 15px;
            ">
                No additional subtopics added yet. Click "Add New Subtopic" to add one.
            </div>
        `;
        return;
    }

    subtopicsData.forEach((subtopic, index) => {
        const subtopicDiv = document.createElement('div');
        subtopicDiv.className = 'subtopic-container';
        subtopicDiv.style.cssText = `
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: #f9f9f9;
        `;
        
        subtopicDiv.innerHTML = `
            <div class="subtopic-header" style="
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
                margin-bottom: 10px;
            ">
                <span style="font-weight: bold; color: #333;">
                    Additional Subtopic ${index + 1}
                </span>
                <button type="button" class="remove-subtopic-btn" data-index="${index}" style="
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    cursor: pointer;
                    font-size: 12px;
                ">Remove</button>
            </div>
            <div class="subtopic-form-row" style="margin-bottom: 10px;">
                <label style="display: block; margin-bottom: 5px; font-weight: bold;">
                    Subtopic Name:
                </label>
                <input type="text" 
                       id="subtopic-name-${index}"
                       class="subtopic-input" 
                       data-field="subtopic" 
                       data-index="${index}"
                       value="${subtopic.subtopic || ''}"
                       placeholder="Enter subtopic name"
                       style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 3px;">
            </div>
            <div class="subtopic-form-row">
                <label style="display: block; margin-bottom: 5px; font-weight: bold;">
                    Subtopic Information:
                </label>
                <textarea class="subtopic-input" 
                          data-field="info" 
                          data-index="${index}"
                          rows="3"
                          placeholder="Enter detailed information for this subtopic"
                          style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 3px; resize: vertical;">${subtopic.info || ''}</textarea>
            </div>
        `;
        
        container.appendChild(subtopicDiv);
    });

    // Setup event handlers for the rendered elements
    setupSubtopicEventHandlers();
}

function setupSubtopicEventHandlers() {
    // Remove button handlers
    document.querySelectorAll('.remove-subtopic-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const index = parseInt(this.dataset.index);
            removeSubtopic(index);
        });
        
        // Hover effect
        btn.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#c82333';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '#dc3545';
        });
    });

    // Input change handlers
    document.querySelectorAll('.subtopic-input').forEach(input => {
        input.addEventListener('input', function() {
            const index = parseInt(this.dataset.index);
            const field = this.dataset.field;
            const value = this.value;
            
            if (subtopicsData[index]) {
                subtopicsData[index][field] = value;
                updateHiddenField();
            }
        });
    });
}

function updateHiddenField() {
    // Filter out completely empty subtopics
    const validSubtopics = subtopicsData.filter(subtopic => 
        subtopic.subtopic.trim() !== '' || subtopic.info.trim() !== ''
    );
    
    const hiddenField = document.getElementById('id_additional_subtopics');
    if (hiddenField) {
        hiddenField.value = JSON.stringify(validSubtopics);
    }
}

function setupFormSubmission() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function() {
            updateHiddenField();
        });
    }
}

// Add button hover effect
document.addEventListener('click', function(e) {
    if (e.target && e.target.id === 'add-subtopic-btn') {
        e.target.style.transform = 'translateY(-1px)';
        setTimeout(() => {
            e.target.style.transform = 'translateY(0)';
        }, 150);
    }
});

// CSS styles
const style = document.createElement('style');
style.textContent = `
    .add-subtopic-btn {
        background-color: #28a745;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 4px;
        cursor: pointer;
        margin-top: 15px;
        margin-bottom: 15px;
        font-size: 14px;
        font-weight: bold;
        transition: all 0.2s ease;
    }
    
    .add-subtopic-btn:hover {
        background-color: #218838;
        transform: translateY(-1px);
    }
    
    .subtopics-dynamic-interface {
        border: 1px solid #e1e1e1;
        border-radius: 6px;
        padding: 20px;
        margin: 20px 0;
        background-color: #fafafa;
    }
`;
document.head.appendChild(style);
