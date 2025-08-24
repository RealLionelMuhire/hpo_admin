// Game Content Admin List JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Add status and language badges
    const statusCells = document.querySelectorAll('td.field-status');
    statusCells.forEach(cell => {
        const status = cell.textContent.trim().toLowerCase();
        cell.innerHTML = `<span class="status-${status}">${cell.textContent}</span>`;
    });
    
    const languageCells = document.querySelectorAll('td.field-language');
    languageCells.forEach(cell => {
        const language = cell.textContent.trim().toLowerCase();
        cell.innerHTML = `<span class="language-${language}">${cell.textContent}</span>`;
    });
    
    // Improve subtopics display
    const subtopicsCells = document.querySelectorAll('td.field-get_subtopics_display');
    subtopicsCells.forEach(cell => {
        const text = cell.textContent.trim();
        if (text && text !== 'No subtopics') {
            const subtopics = text.split(',').map(s => s.trim());
            if (subtopics.length > 2) {
                cell.title = text; // Show full text on hover
                cell.textContent = subtopics.slice(0, 2).join(', ') + ` (+${subtopics.length - 2} more)`;
            }
        }
    });
    
    // Add quick filters
    const changeList = document.querySelector('.change-list');
    if (changeList) {
        const quickFilters = document.createElement('div');
        quickFilters.className = 'quick-filters';
        quickFilters.style.cssText = 'margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 4px;';
        quickFilters.innerHTML = `
            <strong>Quick Filters:</strong>
            <button type="button" onclick="filterByStatus('published')" class="button" style="margin-left: 10px;">Published Only</button>
            <button type="button" onclick="filterByLanguage('english')" class="button">English Only</button>
            <button type="button" onclick="filterByLanguage('kinyarwanda')" class="button">Kinyarwanda Only</button>
            <button type="button" onclick="clearFilters()" class="button default">Clear Filters</button>
        `;
        
        const changeListSearch = document.querySelector('#changelist-search');
        if (changeListSearch) {
            changeListSearch.parentNode.insertBefore(quickFilters, changeListSearch.nextSibling);
        }
    }
});

// Quick filter functions
function filterByStatus(status) {
    const url = new URL(window.location);
    url.searchParams.set('status__exact', status);
    window.location.href = url.toString();
}

function filterByLanguage(language) {
    const url = new URL(window.location);
    url.searchParams.set('language__exact', language);
    window.location.href = url.toString();
}

function clearFilters() {
    const url = new URL(window.location);
    url.searchParams.delete('status__exact');
    url.searchParams.delete('language__exact');
    window.location.href = url.toString();
}
