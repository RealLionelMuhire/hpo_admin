// Game Content Form JavaScript for Multiple Subtopics and CKEditor Integration

document.addEventListener('DOMContentLoaded', function() {
    // Immediate dialog fix
    injectDialogCloseFix();
    
    // Wait for Django admin to fully load
    setTimeout(function() {
        initializeSubtopicsInterface();
        enhanceCKEditor();
        
        // Apply dialog fix again after CKEditor loads
        setTimeout(injectDialogCloseFix, 2000);
    }, 500);
});

// Inject aggressive dialog close fix
function injectDialogCloseFix() {
    // Override window.confirm immediately
    window.confirm = function() { return true; };
    
    // Create a mutation observer to watch for new dialogs
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1 && (node.classList.contains('cke_dialog') || 
                    node.querySelector && node.querySelector('.cke_dialog'))) {
                    
                    setTimeout(function() {
                        addForceCloseHandlers(node.classList.contains('cke_dialog') ? node : node.querySelector('.cke_dialog'));
                    }, 100);
                }
            });
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Add handlers to existing dialogs
    document.querySelectorAll('.cke_dialog').forEach(addForceCloseHandlers);
}

function addForceCloseHandlers(dialog) {
    if (!dialog || dialog.dataset.forceHandlersAdded) return;
    dialog.dataset.forceHandlersAdded = 'true';
    
    // Find and override all close elements
    const closeElements = dialog.querySelectorAll('.cke_dialog_close_button, .cke_dialog_ui_button_cancel, [title="Close"]');
    
    closeElements.forEach(function(element) {
        // Remove all existing event listeners
        element.onclick = null;
        element.onmousedown = null;
        
        // Add our force close handler
        element.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopImmediatePropagation();
            forceRemoveDialog(dialog);
        }, true);
        
        element.addEventListener('mousedown', function(e) {
            e.preventDefault();
            e.stopImmediatePropagation();
        }, true);
    });
    
    // Add background click handler
    const background = document.querySelector('.cke_dialog_background_cover');
    if (background && !background.dataset.forceHandlerAdded) {
        background.dataset.forceHandlerAdded = 'true';
        background.addEventListener('click', function(e) {
            if (e.target === background) {
                forceRemoveDialog(dialog);
            }
        });
    }
}

function forceRemoveDialog(dialog) {
    try {
        // Method 1: Hide via display
        dialog.style.display = 'none';
        
        // Method 2: Remove from DOM
        setTimeout(function() {
            if (dialog.parentNode) {
                dialog.parentNode.removeChild(dialog);
            }
        }, 10);
        
        // Method 3: Remove background cover
        const background = document.querySelector('.cke_dialog_background_cover');
        if (background) {
            background.style.display = 'none';
            setTimeout(function() {
                if (background.parentNode) {
                    background.parentNode.removeChild(background);
                }
            }, 10);
        }
        
        // Method 4: Reset CKEditor state
        if (typeof CKEDITOR !== 'undefined') {
            for (const instanceName in CKEDITOR.instances) {
                const editor = CKEDITOR.instances[instanceName];
                if (editor) {
                    editor.resetDirty();
                    if (editor._.currentDialog) {
                        editor._.currentDialog = null;
                    }
                }
            }
            
            if (CKEDITOR.dialog) {
                CKEDITOR.dialog._.currentTop = null;
                CKEDITOR.dialog._.currentZIndex = 10000;
            }
        }
        
        console.log('Dialog force removed successfully');
    } catch (e) {
        console.log('Error in forceRemoveDialog:', e);
    }
}

// CKEditor Enhancement Functions
function enhanceCKEditor() {
    // Add a preview button for the main info field
    addPreviewButton();
    
    // Configure CKEditor for better UX
    configureCKEditorSettings();
    
    // Fix dialog closing issues
    fixDialogClosingIssues();
}

function fixDialogClosingIssues() {
    // More aggressive dialog closing fix
    let dialogCloseInProgress = false;
    
    // Override window.confirm to always return true for CKEditor dialogs
    const originalConfirm = window.confirm;
    window.confirm = function(message) {
        if (message && (message.includes('changed some options') || 
                       message.includes('close the dialog') ||
                       message.includes('Are you sure'))) {
            return true; // Always confirm dialog closing
        }
        return originalConfirm.call(this, message);
    };
    
    // Force close dialogs using multiple methods
    function forceCloseDialog() {
        if (dialogCloseInProgress) return;
        dialogCloseInProgress = true;
        
        try {
            // Method 1: Close via CKEditor API
            if (typeof CKEDITOR !== 'undefined') {
                for (const instanceName in CKEDITOR.instances) {
                    const editor = CKEDITOR.instances[instanceName];
                    if (editor && editor._.currentDialog) {
                        editor._.currentDialog.hide();
                    }
                }
            }
            
            // Method 2: Remove dialog DOM elements directly
            const dialogs = document.querySelectorAll('.cke_dialog');
            dialogs.forEach(function(dialog) {
                dialog.style.display = 'none';
                dialog.remove();
            });
            
            // Method 3: Remove dialog background covers
            const covers = document.querySelectorAll('.cke_dialog_background_cover');
            covers.forEach(function(cover) {
                cover.style.display = 'none';
                cover.remove();
            });
            
            // Method 4: Reset CKEditor dialog state
            if (typeof CKEDITOR !== 'undefined' && CKEDITOR.dialog) {
                CKEDITOR.dialog._.currentTop = null;
                CKEDITOR.dialog._.currentZIndex = null;
            }
            
        } catch (e) {
            console.log('Dialog force close error:', e);
        } finally {
            setTimeout(function() {
                dialogCloseInProgress = false;
            }, 500);
        }
    }
    
    // Handle all possible close triggers
    document.addEventListener('click', function(e) {
        if (e.target.closest('.cke_dialog_close_button') || 
            e.target.closest('.cke_dialog_ui_button_cancel') ||
            e.target.classList.contains('cke_dialog_background_cover')) {
            
            e.preventDefault();
            e.stopPropagation();
            forceCloseDialog();
        }
    }, true); // Use capture phase
    
    // Handle ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && document.querySelector('.cke_dialog')) {
            e.preventDefault();
            e.stopPropagation();
            forceCloseDialog();
        }
    }, true);
    
    // Monitor for dialog state changes and force close if needed
    setInterval(function() {
        const dialogs = document.querySelectorAll('.cke_dialog');
        if (dialogs.length > 0 && !dialogCloseInProgress) {
            // Check if dialog has been hanging around too long
            dialogs.forEach(function(dialog) {
                if (!dialog.dataset.openTime) {
                    dialog.dataset.openTime = Date.now();
                } else if (Date.now() - dialog.dataset.openTime > 30000) { // 30 seconds
                    console.log('Force closing hanging dialog');
                    forceCloseDialog();
                }
            });
        }
    }, 1000);
}

function addPreviewButton() {
    const infoField = document.querySelector('.field-info');
    if (infoField) {
        const previewBtn = document.createElement('button');
        previewBtn.type = 'button';
        previewBtn.className = 'preview-content-btn';
        previewBtn.innerHTML = '👁️ Preview Content';
        previewBtn.onclick = function() {
            previewContent();
        };
        
        const helpText = infoField.querySelector('.help');
        if (helpText) {
            helpText.appendChild(previewBtn);
        }
    }
}

function previewContent() {
    // Get content from CKEditor
    let content = '';
    try {
        if (typeof CKEDITOR !== 'undefined' && CKEDITOR.instances.id_info) {
            content = CKEDITOR.instances.id_info.getData();
        } else {
            // Fallback to textarea value
            const textarea = document.getElementById('id_info');
            content = textarea ? textarea.value : '';
        }
    } catch (e) {
        console.error('Error getting CKEditor content:', e);
        const textarea = document.getElementById('id_info');
        content = textarea ? textarea.value : '';
    }
    
    if (!content.trim()) {
        alert('No content to preview. Please add some content first.');
        return;
    }
    
    // Create and show preview modal
    showPreviewModal(content);
}

function showPreviewModal(content) {
    // Remove existing modal if present
    const existingModal = document.querySelector('.content-preview-modal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Create modal
    const modal = document.createElement('div');
    modal.className = 'content-preview-modal';
    modal.style.display = 'block';
    
    modal.innerHTML = `
        <div class="content-preview-content">
            <span class="close-preview">&times;</span>
            <h2>Content Preview</h2>
            <div class="preview-body">
                ${content}
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Add close functionality
    const closeBtn = modal.querySelector('.close-preview');
    closeBtn.onclick = function() {
        modal.remove();
    };
    
    // Close on outside click
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.remove();
        }
    };
}

function configureCKEditorSettings() {
    // Wait for CKEditor to be ready
    if (typeof CKEDITOR !== 'undefined') {
        CKEDITOR.on('instanceReady', function(ev) {
            const editor = ev.editor;
            
            // Fix dialog closing issues
            editor.on('dialogShow', function(evt) {
                const dialog = evt.data;
                
                // Override the dialog's onCancel method to prevent confirmation
                const originalOnCancel = dialog.definition.onCancel;
                dialog.definition.onCancel = function() {
                    // Force close without confirmation
                    dialog.hide();
                    return false;
                };
                
                // Add ESC key handler
                dialog.on('key', function(evt) {
                    if (evt.data.keyCode === 27) { // ESC key
                        evt.cancel();
                        dialog.hide();
                    }
                });
                
                // Override the dirty state check
                dialog.on('ok', function(evt) {
                    // Clear dirty state to prevent confirmation
                    if (dialog._.editor) {
                        dialog._.editor.resetDirty();
                    }
                });
            });
            
            // Enhanced image editing functionality
            editor.on('contentDom', function() {
                const editable = editor.editable();
                
                // Double-click to edit images
                editable.attachListener(editable, 'dblclick', function(evt) {
                    const element = evt.data.getTarget();
                    if (element.is('img')) {
                        editor.execCommand('image2');
                    }
                });
                
                // Add helpful styling to the editor content
                editable.attachListener(editable, 'keyup', function() {
                    // Auto-save or other functionality can be added here
                });
            });
            
            // Image upload progress handling
            editor.on('fileUploadRequest', function(evt) {
                showUploadProgress('Uploading image...');
            });
            
            editor.on('fileUploadResponse', function(evt) {
                hideUploadProgress();
                const response = evt.data.fileLoader.responseData;
                if (response.error) {
                    alert('Image upload failed: ' + response.error.message);
                }
            });
            
            // Context menu enhancements for images
            editor.addMenuGroup('imageGroup');
            editor.addMenuItem('imageProperties', {
                label: 'Image Properties',
                command: 'image2',
                group: 'imageGroup'
            });
            
            // Custom image alignment commands
            editor.addCommand('alignImageLeft', {
                exec: function(editor) {
                    const selection = editor.getSelection();
                    const element = selection.getStartElement();
                    if (element && element.is('img')) {
                        element.removeClass('image-center image-right');
                        element.addClass('image-left');
                    }
                }
            });
            
            editor.addCommand('alignImageCenter', {
                exec: function(editor) {
                    const selection = editor.getSelection();
                    const element = selection.getStartElement();
                    if (element && element.is('img')) {
                        element.removeClass('image-left image-right');
                        element.addClass('image-center');
                    }
                }
            });
            
            editor.addCommand('alignImageRight', {
                exec: function(editor) {
                    const selection = editor.getSelection();
                    const element = selection.getStartElement();
                    if (element && element.is('img')) {
                        element.removeClass('image-left image-center');
                        element.addClass('image-right');
                    }
                }
            });
        });
        
        // Global CKEditor configuration for image handling
        CKEDITOR.config.image2_captionedClass = 'image-captioned';
        CKEDITOR.config.image2_alignClasses = ['image-left', 'image-center', 'image-right'];
        
        // Completely disable all dialog confirmations
        CKEDITOR.config.dialog_noConfirmCancel = true;
        
        // Override the entire dialog system
        if (CKEDITOR.dialog) {
            const originalAdd = CKEDITOR.dialog.add;
            CKEDITOR.dialog.add = function(name, definition) {
                // Force override all dialog behaviors
                if (typeof definition === 'function') {
                    const originalDefinition = definition;
                    definition = function(editor) {
                        const def = originalDefinition.call(this, editor);
                        return overrideDialogDefinition(def);
                    };
                } else {
                    definition = overrideDialogDefinition(definition);
                }
                return originalAdd.call(this, name, definition);
            };
        }
        
        function overrideDialogDefinition(def) {
            // Override onCancel to never show confirmation
            def.onCancel = function() {
                this.hide();
                return false;
            };
            
            // Override onHide to clean up state
            const originalOnHide = def.onHide;
            def.onHide = function() {
                try {
                    if (this._.editor) {
                        this._.editor.resetDirty();
                        this._.editor.fire('saveSnapshot');
                    }
                } catch(e) {}
                
                if (originalOnHide) {
                    originalOnHide.call(this);
                }
            };
            
            // Override all buttons
            if (def.buttons) {
                def.buttons.forEach(function(button) {
                    if (button.id === 'cancel' || button.type === 'button') {
                        button.onClick = function(evt) {
                            evt.data.dialog.hide();
                            return false;
                        };
                    }
                });
            }
            
            return def;
        }
        
        // Override dialog manager globally
        CKEDITOR.on('dialogDefinition', function(ev) {
            ev.data.definition = overrideDialogDefinition(ev.data.definition);
        });
        
        // Override the dialog prototype methods
        if (CKEDITOR.dialog && CKEDITOR.dialog.prototype) {
            const originalHide = CKEDITOR.dialog.prototype.hide;
            CKEDITOR.dialog.prototype.hide = function() {
                // Force hide without confirmation
                this._.editor.resetDirty();
                return originalHide.call(this);
            };
        }
    }
}

// Upload progress functions
function showUploadProgress(message) {
    const progressDiv = document.createElement('div');
    progressDiv.id = 'upload-progress';
    progressDiv.className = 'upload-progress-indicator';
    progressDiv.innerHTML = `
        <div class="progress-content">
            <div class="spinner"></div>
            <span>${message}</span>
        </div>
    `;
    
    // Add CSS for the progress indicator
    const style = document.createElement('style');
    style.textContent = `
        .upload-progress-indicator {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 124, 186, 0.9);
            color: white;
            padding: 20px 30px;
            border-radius: 8px;
            z-index: 10000;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .progress-content {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .spinner {
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-top: 2px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(progressDiv);
}

function hideUploadProgress() {
    const progressDiv = document.getElementById('upload-progress');
    if (progressDiv) {
        progressDiv.remove();
    }
}

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
