// Dynamic district filtering based on province selection
document.addEventListener('DOMContentLoaded', function() {
    const provinceField = document.getElementById('id_province');
    const districtField = document.getElementById('id_district');
    
    // Province-District mapping
    const provinceDistricts = {
        'Kigali City': ['Gasabo', 'Kicukiro', 'Nyarugenge'],
        'Northern Province': ['Burera', 'Gakenke', 'Gicumbi', 'Musanze', 'Rulindo'],
        'Southern Province': ['Gisagara', 'Huye', 'Kamonyi', 'Muhanga', 'Nyamagabe', 'Nyanza', 'Nyaruguru', 'Ruhango'],
        'Eastern Province': ['Bugesera', 'Gatsibo', 'Kayonza', 'Kirehe', 'Ngoma', 'Nyagatare', 'Rwamagana'],
        'Western Province': ['Karongi', 'Ngororero', 'Nyabihu', 'Nyamasheke', 'Rubavu', 'Rusizi', 'Rutsiro']
    };
    
    function filterDistricts(selectedProvince) {
        // Clear existing district options
        districtField.innerHTML = '<option value="">--- Select District ---</option>';
        
        if (selectedProvince && provinceDistricts[selectedProvince]) {
            // Add districts for selected province
            provinceDistricts[selectedProvince].forEach(function(district) {
                const option = document.createElement('option');
                option.value = district;
                option.textContent = district;
                districtField.appendChild(option);
            });
            
            // Enable district field
            districtField.disabled = false;
        } else {
            // Disable district field if no province selected
            districtField.disabled = true;
        }
    }
    
    // Add event listener to province field
    if (provinceField) {
        provinceField.addEventListener('change', function() {
            filterDistricts(this.value);
        });
        
        // Initialize on page load if province is already selected
        if (provinceField.value) {
            filterDistricts(provinceField.value);
        } else {
            districtField.disabled = true;
        }
    }
});

// Global function for backwards compatibility
function filterDistricts(selectedProvince) {
    const districtField = document.getElementById('id_district');
    
    const provinceDistricts = {
        'Kigali City': ['Gasabo', 'Kicukiro', 'Nyarugenge'],
        'Northern Province': ['Burera', 'Gakenke', 'Gicumbi', 'Musanze', 'Rulindo'],
        'Southern Province': ['Gisagara', 'Huye', 'Kamonyi', 'Muhanga', 'Nyamagabe', 'Nyanza', 'Nyaruguru', 'Ruhango'],
        'Eastern Province': ['Bugesera', 'Gatsibo', 'Kayonza', 'Kirehe', 'Ngoma', 'Nyagatare', 'Rwamagana'],
        'Western Province': ['Karongi', 'Ngororero', 'Nyabihu', 'Nyamasheke', 'Rubavu', 'Rusizi', 'Rutsiro']
    };
    
    if (districtField) {
        // Clear existing district options
        districtField.innerHTML = '<option value="">--- Select District ---</option>';
        
        if (selectedProvince && provinceDistricts[selectedProvince]) {
            // Add districts for selected province
            provinceDistricts[selectedProvince].forEach(function(district) {
                const option = document.createElement('option');
                option.value = district;
                option.textContent = district;
                districtField.appendChild(option);
            });
            
            // Enable district field
            districtField.disabled = false;
        } else {
            // Disable district field if no province selected
            districtField.disabled = true;
        }
    }
}
