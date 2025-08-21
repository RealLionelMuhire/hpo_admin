document.addEventListener('DOMContentLoaded', function() {
    const questionTypeField = document.querySelector('#id_question_type');
    const correctAnswerField = document.querySelector('#id_correct_answer');
    const multipleChoiceSection = document.querySelector('.multiple-choice-options');
    
    function toggleQuestionFields(questionType) {
        if (questionType === 'true_false') {
            // Hide multiple choice options
            if (multipleChoiceSection) {
                multipleChoiceSection.style.display = 'none';
            }
            
            // Convert correct answer to dropdown for true/false
            if (correctAnswerField && correctAnswerField.tagName !== 'SELECT') {
                const currentValue = correctAnswerField.value;
                const selectField = document.createElement('select');
                selectField.id = 'id_correct_answer';
                selectField.name = 'correct_answer';
                selectField.required = correctAnswerField.required;
                
                // Add options
                const emptyOption = document.createElement('option');
                emptyOption.value = '';
                emptyOption.textContent = '--- Select ---';
                selectField.appendChild(emptyOption);
                
                const trueOption = document.createElement('option');
                trueOption.value = 'True';
                trueOption.textContent = 'True';
                if (currentValue === 'True') trueOption.selected = true;
                selectField.appendChild(trueOption);
                
                const falseOption = document.createElement('option');
                falseOption.value = 'False';
                falseOption.textContent = 'False';
                if (currentValue === 'False') falseOption.selected = true;
                selectField.appendChild(falseOption);
                
                correctAnswerField.parentNode.replaceChild(selectField, correctAnswerField);
            }
            
            // Clear multiple choice option fields
            for (let i = 1; i <= 4; i++) {
                const optionField = document.querySelector(`#id_option_${i}`);
                if (optionField) {
                    optionField.value = '';
                }
            }
            
        } else if (questionType === 'multiple_choice') {
            // Show multiple choice options
            if (multipleChoiceSection) {
                multipleChoiceSection.style.display = 'block';
            }
            
            // Convert correct answer back to text field for multiple choice
            const currentCorrectAnswer = document.querySelector('#id_correct_answer');
            if (currentCorrectAnswer && currentCorrectAnswer.tagName === 'SELECT') {
                const currentValue = currentCorrectAnswer.value;
                const textField = document.createElement('input');
                textField.type = 'text';
                textField.id = 'id_correct_answer';
                textField.name = 'correct_answer';
                textField.value = currentValue === 'True' || currentValue === 'False' ? '' : currentValue;
                textField.required = currentCorrectAnswer.required;
                textField.maxLength = 255;
                
                currentCorrectAnswer.parentNode.replaceChild(textField, currentCorrectAnswer);
            }
        }
    }
    
    // Set initial state
    if (questionTypeField) {
        toggleQuestionFields(questionTypeField.value);
        
        // Add event listener for changes
        questionTypeField.addEventListener('change', function() {
            toggleQuestionFields(this.value);
        });
    }
    
    // Make toggleQuestionFields globally available for inline calls
    window.toggleQuestionFields = toggleQuestionFields;
});
