(function($) {
    'use strict';
    
    console.log('GameContent Admin JS loading...');
    
    let subtopicsData = [];
    
    $(document).ready(function() {
        console.log('DOM ready, starting initialization...');
        // Wait a bit for the admin interface to fully load
        setTimeout(function() {
            console.log('Timeout reached, calling initializeSubtopicsInterface...');
            initializeSubtopicsInterface();
            loadExistingSubtopics();
        }, 500);
    });
    
    function initializeSubtopicsInterface() {
        console.log('initializeSubtopicsInterface called');
        // Find the additional_subtopics field and create the interface
        const $hiddenField = $('#id_additional_subtopics');
        console.log('Hidden field found:', $hiddenField.length > 0, $hiddenField);
        
        if ($hiddenField.length === 0) {
            console.log('Hidden field #id_additional_subtopics not found');
            // Let's see what fields are available
            console.log('Available form fields:', $('input, textarea, select').map(function() { return this.id; }).get());
            return;
        }
        
        // Check if interface already exists
        if ($('.subtopics-wrapper').length > 0) {
            console.log('Interface already exists');
            return;
        }
        
        console.log('Initializing subtopics interface...');
        
        // Create the subtopics interface container
        const $container = $('<div class="subtopics-wrapper">');
        const $header = $('<h3 style="color: #333; margin-bottom: 15px;">Additional Subtopics</h3>');
        const $description = $('<p style="color: #666; margin-bottom: 15px;">Add multiple subtopics with their own information. The main subtopic (above) is automatically included.</p>');
        const $subtopicsContainer = $('<div id="subtopics-container">');
        const $addButton = $('<button type="button" class="add-subtopic-btn">+ Add New Subtopic</button>');
        
        $container.append($header);
        $container.append($description);
        $container.append($subtopicsContainer);
        $container.append($addButton);
        
        // Find the best place to insert the interface
        const $additionalSubtopicsField = $('.field-additional_subtopics');
        if ($additionalSubtopicsField.length > 0) {
            // Insert before the hidden field and hide it
            $additionalSubtopicsField.before($container);
            $additionalSubtopicsField.hide();
        } else {
            // Fallback: insert after the info field
            const $infoField = $('.field-info');
            if ($infoField.length > 0) {
                $infoField.after($container);
            } else {
                // Last resort: append to the form
                $('form').append($container);
            }
        }
        
        // Event handlers
        $addButton.on('click', addSubtopic);
        $(document).on('click', '.remove-subtopic-btn', removeSubtopic);
        $(document).on('input', '.subtopic-input', updateSubtopicsData);
        
        // Form submit handler
        $('form').on('submit', function() {
            updateHiddenField();
        });
        
        console.log('Subtopics interface initialized successfully');
    }
    
    function loadExistingSubtopics() {
        const hiddenFieldValue = $('#id_additional_subtopics').val();
        if (hiddenFieldValue) {
            try {
                subtopicsData = JSON.parse(hiddenFieldValue);
                console.log('Loaded existing subtopics:', subtopicsData);
                renderSubtopics();
            } catch (e) {
                console.error('Error parsing existing subtopics data:', e);
                subtopicsData = [];
            }
        }
    }
    
    function addSubtopic() {
        console.log('Adding new subtopic...');
        const newSubtopic = {
            subtopic: '',
            info: ''
        };
        
        subtopicsData.push(newSubtopic);
        renderSubtopics();
        updateHiddenField();
        
        // Focus on the new subtopic name field
        setTimeout(function() {
            const newIndex = subtopicsData.length - 1;
            $(`#subtopic-name-${newIndex}`).focus();
        }, 100);
    }
    
    function removeSubtopic(e) {
        const index = parseInt($(e.target).data('index'));
        console.log('Removing subtopic at index:', index);
        subtopicsData.splice(index, 1);
        renderSubtopics();
        updateHiddenField();
    }
    
    function renderSubtopics() {
        const $container = $('#subtopics-container');
        $container.empty();
        
        if (subtopicsData.length === 0) {
            $container.append('<div class="no-subtopics">No additional subtopics added yet. Click "Add New Subtopic" to add one.</div>');
            return;
        }
        
        subtopicsData.forEach(function(subtopic, index) {
            const $subtopicDiv = $(`
                <div class="subtopic-container" data-index="${index}">
                    <div class="subtopic-header">
                        <span class="subtopic-title">Additional Subtopic ${index + 1}</span>
                        <button type="button" class="remove-subtopic-btn" data-index="${index}">Remove</button>
                    </div>
                    <div class="subtopic-form-row">
                        <div class="subtopic-name-field">
                            <label>Subtopic Name:</label>
                            <input type="text" 
                                   id="subtopic-name-${index}"
                                   class="subtopic-input form-control" 
                                   data-field="subtopic" 
                                   data-index="${index}"
                                   value="${subtopic.subtopic || ''}"
                                   placeholder="Enter subtopic name">
                        </div>
                        <div class="subtopic-info-field">
                            <label>Subtopic Information:</label>
                            <textarea class="subtopic-input form-control" 
                                      data-field="info" 
                                      data-index="${index}"
                                      rows="3"
                                      placeholder="Enter detailed information for this subtopic">${subtopic.info || ''}</textarea>
                        </div>
                    </div>
                </div>
            `);
            
            $container.append($subtopicDiv);
        });
        
        console.log('Rendered', subtopicsData.length, 'subtopics');
    }
    
    function updateSubtopicsData(e) {
        const $input = $(e.target);
        const index = parseInt($input.data('index'));
        const field = $input.data('field');
        const value = $input.val();
        
        if (subtopicsData[index]) {
            subtopicsData[index][field] = value;
            updateHiddenField();
        }
    }
    
    function updateHiddenField() {
        // Filter out empty subtopics
        const validSubtopics = subtopicsData.filter(function(subtopic) {
            return subtopic.subtopic.trim() !== '' || subtopic.info.trim() !== '';
        });
        
        $('#id_additional_subtopics').val(JSON.stringify(validSubtopics));
        console.log('Updated hidden field with:', validSubtopics);
    }
    
})(django.jQuery);
