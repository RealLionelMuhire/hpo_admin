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
    // Create main container styled like Django admin fieldset
    const container = document.createElement('div');
    container.className = 'subtopics-dynamic-interface module aligned';
    container.innerHTML = `
        <fieldset class="module aligned">
            <h2>
                <a href="#" class="collapse-toggle" id="subtopics-toggle">
                    Additional Subtopics
                    <span class="toggle-icon">Hide</span>
                </a>
            </h2>
            <div class="fieldset-content" id="subtopics-content">
                <div class="help">
                    Add multiple subtopics with their own information. The main subtopic (above) is automatically included.
                </div>
                <div id="dynamic-subtopics-container"></div>
                <div class="form-row">
                    <div class="field-box">
                        <button type="button" id="add-subtopic-btn" class="add-subtopic-btn default">
                            Add New Subtopic
                        </button>
                    </div>
                </div>
            </div>
        </fieldset>
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
    
    // Setup collapse/expand functionality
    const toggleButton = document.getElementById('subtopics-toggle');
    const content = document.getElementById('subtopics-content');
    const toggleIcon = toggleButton.querySelector('.toggle-icon');
    
    toggleButton.addEventListener('click', function(e) {
        e.preventDefault();
        if (content.style.display === 'none') {
            content.style.display = 'block';
            toggleIcon.textContent = 'Hide';
            toggleButton.classList.remove('collapsed');
        } else {
            content.style.display = 'none';
            toggleIcon.textContent = 'Show';
            toggleButton.classList.add('collapsed');
        }
    });
    
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
            <div class="no-subtopics help">
                No additional subtopics added yet. Click "Add New Subtopic" to add one.
            </div>
        `;
        return;
    }

    subtopicsData.forEach((subtopic, index) => {
        const subtopicDiv = document.createElement('div');
        subtopicDiv.className = 'subtopic-container form-row';
        
        subtopicDiv.innerHTML = `
            <fieldset class="module aligned subtopic-fieldset">
                <h2>
                    Additional Subtopic ${index + 1}
                    <button type="button" class="remove-subtopic-btn" data-index="${index}">
                        Remove
                    </button>
                </h2>
                <div class="form-row field-subtopic-name">
                    <div>
                        <label class="required" for="subtopic-name-${index}">Subtopic Name:</label>
                        <input type="text" 
                               id="subtopic-name-${index}"
                               class="subtopic-input vTextField" 
                               data-field="subtopic" 
                               data-index="${index}"
                               value="${subtopic.subtopic || ''}"
                               placeholder="Enter subtopic name"
                               required="">
                    </div>
                </div>
                <div class="form-row field-subtopic-info">
                    <div>
                        <label for="subtopic-info-${index}">Subtopic Information:</label>
                        <textarea class="subtopic-input vLargeTextField" 
                                  id="subtopic-info-${index}"
                                  data-field="info" 
                                  data-index="${index}"
                                  rows="4"
                                  cols="40"
                                  placeholder="Enter detailed information for this subtopic">${subtopic.info || ''}</textarea>
                        <div class="help">Enter detailed information for this subtopic</div>
                    </div>
                </div>
            </fieldset>
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

// CSS styles to match Django admin and respect themes
const style = document.createElement('style');
style.textContent = `
    .subtopics-dynamic-interface {
        margin-bottom: 20px;
    }
    
    .subtopic-fieldset {
        margin-bottom: 15px;
        background: var(--body-bg, #f8f8f8);
        border: 1px solid var(--border-color, #ddd);
    }
    
    .subtopic-fieldset h2 {
        background: var(--primary, #79aec8);
        color: var(--primary-fg, white);
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 10px 15px;
        margin: 0;
        border-bottom: 1px solid var(--border-color, #ddd);
        position: relative;
    }
    
    .add-subtopic-btn {
        background: var(--primary, #417690);
        color: var(--primary-fg, white);
        border: none;
        padding: 10px 15px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 13px;
        font-weight: normal;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .add-subtopic-btn:hover {
        background: var(--primary-accent, #205067);
    }
    
    .remove-subtopic-btn {
        background: var(--delete-button-bg, #ba2121);
        color: var(--button-fg, white);
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
        cursor: pointer;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
    }
    
    .remove-subtopic-btn:hover {
        background: var(--delete-button-hover-bg, #a41515);
    }
    
    .collapse-toggle {
        color: var(--primary-fg, white) !important;
        text-decoration: none !important;
        display: block;
        position: relative;
    }
    
    .collapse-toggle:hover {
        color: var(--primary-fg, #f0f0f0) !important;
        opacity: 0.9;
    }
    
    .toggle-icon {
        font-size: 11px;
        position: absolute;
        right: 15px;
        top: 50%;
        transform: translateY(-50%);
        font-weight: normal;
    }
    
    .collapse-toggle.collapsed .toggle-icon:before {
        content: "▶ ";
    }
    
    .no-subtopics {
        padding: 15px;
        color: var(--body-quiet-color, #666);
        font-style: italic;
        text-align: center;
        background: var(--body-bg, #f8f8f8);
        border: 1px dashed var(--border-color, #ddd);
        margin-bottom: 15px;
    }
    
    .subtopic-container .form-row {
        margin: 0;
    }
    
    .subtopic-container .form-row > div {
        padding: 10px 15px;
    }
    
    .subtopic-container label {
        font-weight: bold;
        color: var(--body-fg, #333);
        display: block;
        margin-bottom: 5px;
    }
    
    .subtopic-container label.required:after {
        content: " *";
        color: var(--error-fg, #ba2121);
    }
    
    .subtopic-container .help {
        font-size: 11px;
        color: var(--body-quiet-color, #666);
        margin-top: 5px;
    }
    
    /* Ensure inputs respect theme */
    .subtopic-input {
        background: var(--body-bg, white) !important;
        color: var(--body-fg, #333) !important;
        border: 1px solid var(--border-color, #ddd) !important;
    }
    
    .subtopic-input:focus {
        border-color: var(--primary, #79aec8) !important;
        box-shadow: 0 0 0 2px var(--primary-accent, rgba(121, 174, 200, 0.2)) !important;
    }
    
    /* Dark theme specific adjustments */
    @media (prefers-color-scheme: dark) {
        .subtopic-fieldset {
            background: var(--darkened-bg, #2b2b2b);
            border-color: var(--border-color, #464646);
        }
        
        .no-subtopics {
            background: var(--darkened-bg, #2b2b2b);
            border-color: var(--border-color, #464646);
        }
    }
`;
document.head.appendChild(style);
