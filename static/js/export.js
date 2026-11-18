
document.addEventListener('DOMContentLoaded', () => {
    
    const exportBtn = document.getElementById('exportBtn');
    const exportMenu = document.getElementById('exportMenu');

    // Toggle menu visibility when Export is clicked
    exportBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isHidden = exportMenu.style.display === 'none' || exportMenu.style.display === '';
        exportMenu.style.display = isHidden ? 'flex' : 'none';
    });

    // Capture the selected format
    document.querySelectorAll('.export-opt').forEach(button => {
       
        button.addEventListener('click', (e) => {
            const format = e.target.dataset.format;
            const noteId = e.target.dataset.id;
            console.log('id' , noteId);
            console.log('format' , format);
            exportMenu.style.display = 'none';
            
            // Your custom logic goes here
            handleExport(format , noteId);
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', () => {
        exportMenu.style.display = 'none';
    });
});

async function handleExport(format , noteId) {
    try {
            const response = await axios.post("/export", 
                { format: format, noteId: noteId },
                { responseType: 'blob' } // CRITICAL: Tells Axios to expect binary file data
            );
        
           
            // Create a blob URL from the binary response
            const blob = new Blob([response.data], { type: `application/${format}` });
            const downloadUrl = window.URL.createObjectURL(blob);

            // Create a hidden link and trigger click
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.setAttribute('download', `note.${format}`); // Sets the file name
            document.body.appendChild(link);
            link.click();

            // Cleanup
            link.remove();
            window.URL.revokeObjectURL(downloadUrl);
        } catch (error) {
            console.error("Export failed:", error);
        }
    }