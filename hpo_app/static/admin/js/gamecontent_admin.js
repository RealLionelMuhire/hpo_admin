(function($) {
    'use strict';
    
    let subtopicsData = [];
    let subtopicCounter = 0;
    
(function($) {
    'use strict';
    
    let subtopicsData = [];
    let subtopicCounter = 0;
    
    $(document).ready(function() {
        // Wait a bit for the admin interface to fully load
        setTimeout(function() {
            initializeSubtopicsInterface();
            loadExistingSubtopics();
        }, 500);
    });
    
    function initializeSubtopicsInterface() {
        // Find the additional_subtopics field and create the interface
        const $hiddenField = $('#id_additional_subtopics');
        if ($hiddenField.length === 0) {
            console.log('Hidden field #id_additional_subtopics not found');
            return;
        }
        
        // Check if interface already exists
        if ($('.subtopics-wrapper').length > 0) {
            return;
        }
        
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
            // Insert before the hidden field
            $additionalSubtopicsField.before($container);
            // Hide the actual field since we're replacing it with our interface
            $additionalSubtopicsField.hide();
        } else {
            // Fallback: insert after the Multiple Subtopics fieldset
            const $multipleSubtopicsFieldset = $('fieldset:contains("Multiple Subtopics")');
            if ($multipleSubtopicsFieldset.length > 0) {
                $multipleSubtopicsFieldset.append($container);
            } else {
                // Last resort: insert after the info field
                const $infoField = $('.field-info');
                if ($infoField.length > 0) {
                    $infoField.after($container);
                }
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
        
        console.log('Subtopics interface initialized');
    }
    
    function loadExistingSubtopics() {
        const hiddenFieldValue = $('#id_additional_subtopics').val();
        if (hiddenFieldValue) {
            try {
                subtopicsData = JSON.parse(hiddenFieldValue);
                renderSubtopics();
            } catch (e) {
                console.error('Error parsing existing subtopics data:', e);
                subtopicsData = [];
            }
        }
    }
    
    function addSubtopic() {
        const newSubtopic = {
            subtopic: '',
            info: ''
        };
        
        subtopicsData.push(newSubtopic);
        renderSubtopics();
        
        // Focus on the new subtopic name field
        setTimeout(function() {
            $(`#subtopic-name-${subtopicsData.length - 1}`).focus();
        }, 100);
    }
    
    function removeSubtopic(e) {
        const index = parseInt($(e.target).data('index'));
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
    }
    
})(django.jQuery);
