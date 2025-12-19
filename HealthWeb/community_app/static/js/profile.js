// Profile page specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize profile tabs
    initProfileTabs();

    // Initialize journey timeline
    initJourneyTimeline();

    // Initialize profile image upload
    initProfileImageUpload();

    // Initialize form toggles
    initFormToggles();
});

// Profile tabs functionality
function initProfileTabs() {
    const tabs = document.querySelectorAll('.profile-tab');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetId = this.getAttribute('data-tab');

            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked tab
            this.classList.add('active');

            // Show corresponding content
            const targetContent = document.getElementById(`${targetId}-content`);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
}

// Journey timeline functionality
function initJourneyTimeline() {
    const timelineItems = document.querySelectorAll('.timeline-item');

    timelineItems.forEach((item, index) => {
        // Add timeline connector
        if (index < timelineItems.length - 1) {
            const connector = document.createElement('div');
            connector.className = 'timeline-connector';
            item.appendChild(connector);
        }

        // Add expand/collapse functionality for journey details
        const toggleBtn = item.querySelector('.timeline-toggle');
        const details = item.querySelector('.timeline-details');

        if (toggleBtn && details) {
            toggleBtn.addEventListener('click', function() {
                details.classList.toggle('expanded');

                const icon = this.querySelector('i');
                if (details.classList.contains('expanded')) {
                    icon.classList.remove('fa-chevron-down');
                    icon.classList.add('fa-chevron-up');
                } else {
                    icon.classList.remove('fa-chevron-up');
                    icon.classList.add('fa-chevron-down');
                }
            });
        }
    });
}

// Profile image upload functionality
function initProfileImageUpload() {
    const uploadInput = document.getElementById('profile-picture-input');
    const uploadBtn = document.getElementById('profile-picture-btn');
    const previewImage = document.getElementById('profile-preview');
    const defaultIcon = document.querySelector('.profile-avatar-icon');

    if (uploadInput && uploadBtn) {
        // Trigger file input when button is clicked
        uploadBtn.addEventListener('click', function() {
            uploadInput.click();
        });

        // Handle file selection
        uploadInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                // Validate file type
                const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
                if (!validTypes.includes(file.type)) {
                    alert('Please select a valid image file (JPEG, PNG, or GIF).');
                    return;
                }

                // Validate file size (max 5MB)
                if (file.size > 5 * 1024 * 1024) {
                    alert('Image must be less than 5MB.');
                    return;
                }

                // Preview image
                const reader = new FileReader();
                reader.onload = function(e) {
                    if (previewImage) {
                        previewImage.src = e.target.result;
                        previewImage.style.display = 'block';
                    }
                    if (defaultIcon) {
                        defaultIcon.style.display = 'none';
                    }
                };
                reader.readAsDataURL(file);

                // Auto-submit the form if it exists
                const form = uploadInput.closest('form');
                if (form) {
                    form.submit();
                }
            }
        });
    }
}

// Form toggle functionality (show/hide forms)
function initFormToggles() {
    const toggleButtons = document.querySelectorAll('[data-toggle-form]');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-toggle-form');
            const targetForm = document.getElementById(targetId);

            if (targetForm) {
                const isHidden = targetForm.style.display === 'none' ||
                                targetForm.classList.contains('hidden');

                if (isHidden) {
                    // Show form
                    targetForm.style.display = 'block';
                    targetForm.classList.remove('hidden');
                    this.innerHTML = '<i class="fas fa-times"></i> Cancel';

                    // Scroll to form
                    setTimeout(() => {
                        targetForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }, 100);
                } else {
                    // Hide form
                    targetForm.style.display = 'none';
                    targetForm.classList.add('hidden');
                    this.innerHTML = '<i class="fas fa-edit"></i> Edit';
                }
            }
        });
    });
}

// Health stats calculation
function calculateHealthStats(journeys) {
    const stats = {
        totalEntries: journeys.length,
        symptomsTracked: 0,
        testsDone: 0,
        doctorsConsulted: 0,
        treatmentsUndergone: 0
    };

    journeys.forEach(journey => {
        if (journey.symptom) stats.symptomsTracked++;
        if (journey.test) stats.testsDone++;
        if (journey.doctor) stats.doctorsConsulted++;
        if (journey.treatment) stats.treatmentsUndergone++;
    });

    return stats;
}

// Update health stats display
function updateHealthStats() {
    const journeyElements = document.querySelectorAll('.journey-item');
    const journeys = Array.from(journeyElements).map(el => {
        return {
            symptom: el.querySelector('.symptom-text')?.textContent,
            test: el.querySelector('.test-text')?.textContent,
            doctor: el.querySelector('.doctor-text')?.textContent,
            treatment: el.querySelector('.treatment-text')?.textContent
        };
    });

    const stats = calculateHealthStats(journeys);

    // Update DOM elements
    document.getElementById('total-entries').textContent = stats.totalEntries;
    document.getElementById('symptoms-tracked').textContent = stats.symptomsTracked;
    document.getElementById('tests-done').textContent = stats.testsDone;
    document.getElementById('doctors-consulted').textContent = stats.doctorsConsulted;
    document.getElementById('treatments-undergone').textContent = stats.treatmentsUndergone;
}

// Export journey data
function exportJourneyData() {
    const journeyElements = document.querySelectorAll('.journey-item');
    const journeyData = [];

    journeyElements.forEach(el => {
        journeyData.push({
            title: el.querySelector('.journey-title')?.textContent,
            date: el.querySelector('.journey-date')?.textContent,
            symptom: el.querySelector('.symptom-text')?.textContent,
            test: el.querySelector('.test-text')?.textContent,
            doctor: el.querySelector('.doctor-text')?.textContent,
            treatment: el.querySelector('.treatment-text')?.textContent,
            notes: el.querySelector('.notes-text')?.textContent
        });
    });

    // Create JSON blob
    const dataStr = JSON.stringify(journeyData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });

    // Create download link
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(dataBlob);
    downloadLink.download = 'health-journey-data.json';

    // Trigger download
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// Print journey report
function printJourneyReport() {
    const printContent = document.getElementById('journeys-content').innerHTML;
    const originalContent = document.body.innerHTML;

    document.body.innerHTML = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Health Journey Report</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                h1, h2, h3 { color: #333; }
                .journey-item { margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; }
                @media print {
                    .no-print { display: none; }
                }
            </style>
        </head>
        <body>
            <h1>Health Journey Report</h1>
            <p>Generated on ${new Date().toLocaleDateString()}</p>
            ${printContent}
            <button class="no-print" onclick="window.location.reload()">Back</button>
        </body>
        </html>
    `;

    window.print();
    document.body.innerHTML = originalContent;
}

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initProfileTabs);
} else {
    initProfileTabs();
}